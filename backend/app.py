import os, io, json, base64
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image

app = Flask(__name__)
CORS(app, origins=["*"])

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH  = os.path.join(BASE_DIR, "bangla_sign_model.h5")
CI_PATH     = os.path.join(BASE_DIR, "class_indices.json")
LABELS_PATH = os.path.join(BASE_DIR, "labels.json")
IMG_SIZE    = (96,96)   # must match training size

# ── Lazy globals (loaded on first request) ────────────────────────────────
model         = None
class_indices = None
LABEL_MAP     = None
IDX_TO_CLS    = None
NUM_CLASSES   = None


def download_model():
    """Download model files from HuggingFace if not present."""
    from huggingface_hub import hf_hub_download
    REPO = "noshin-nawar/silent-voices-model"

    if not os.path.exists(MODEL_PATH):
        print("⬇️  Downloading model from HuggingFace...")
        hf_hub_download(repo_id=REPO, filename="bangla_sign_model.h5",  local_dir=BASE_DIR)
        print("✅ Model downloaded.")

    if not os.path.exists(CI_PATH):
        print("⬇️  Downloading class_indices.json...")
        hf_hub_download(repo_id=REPO, filename="class_indices.json", local_dir=BASE_DIR)
        print("✅ class_indices.json downloaded.")


def load_everything():
    """Load model + labels into globals. Called once on first request."""
    global model, class_indices, LABEL_MAP, IDX_TO_CLS, NUM_CLASSES

    if model is not None:
        return  # already loaded

    import tensorflow as tf
    from tensorflow.keras.models import load_model as tf_load

    download_model()

    print("Loading model…")
    model = tf_load(MODEL_PATH)
    print("✅ Model loaded.")

    with open(CI_PATH,     encoding="utf-8") as f: class_indices = json.load(f)
    with open(LABELS_PATH, encoding="utf-8") as f: labels_raw    = json.load(f)

    LABEL_MAP   = {**labels_raw["digits"], **labels_raw["alphabets"]}
    IDX_TO_CLS  = {v: k for k, v in class_indices.items()}
    NUM_CLASSES = len(class_indices)
    print(f"✅ {NUM_CLASSES} classes ready.")


def preprocess(img_bytes: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, 0)


def enrich(cls_name: str, confidence: float) -> dict:
    info = LABEL_MAP.get(cls_name, {})
    return {
        "class":      cls_name,
        "display":    info.get("display", cls_name),
        "roman":      info.get("roman", ""),
        "name":       info.get("name", cls_name),
        "type":       info.get("type", "unknown"),
        "confidence": round(confidence * 100, 2),
    }


# ── Routes ────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def health():
    """Health check — responds instantly without loading the model."""
    return jsonify({"status": "ok", "message": "Silent Voices API 🤙"})


@app.route("/labels", methods=["GET"])
def get_labels():
    load_everything()
    return jsonify(LABEL_MAP)


@app.route("/predict", methods=["POST"])
def predict():
    load_everything()

    if "file" in request.files:
        f = request.files["file"]
        if f.filename == "":
            return jsonify({"error": "No file selected"}), 400
        img_bytes = f.read()
    elif request.is_json:
        data = request.get_json()
        if "image" not in data:
            return jsonify({"error": "JSON must have 'image' key (base64)"}), 400
        img_bytes = base64.b64decode(data["image"].split(",")[-1])
    else:
        return jsonify({"error": "Send multipart/form-data 'file' or JSON 'image'"}), 400

    try:
        preds    = model.predict(preprocess(img_bytes), verbose=0)[0]
        top5_idx = np.argsort(preds)[::-1][:5]

        prediction = enrich(IDX_TO_CLS[top5_idx[0]], float(preds[top5_idx[0]]))
        top5       = [enrich(IDX_TO_CLS[i], float(preds[i])) for i in top5_idx]

        all_scores = {
            IDX_TO_CLS[i]: {
                "confidence": round(float(preds[i]) * 100, 2),
                **{k: LABEL_MAP.get(IDX_TO_CLS[i], {}).get(k, "")
                   for k in ("display", "type", "name")}
            }
            for i in range(NUM_CLASSES)
        }

        return jsonify({"prediction": prediction, "top5": top5, "all_scores": all_scores})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)