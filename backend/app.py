import os, io, json, base64, traceback
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
IMG_SIZE    = (96, 96)

# ── Lazy globals ──────────────────────────────────────────────────────────
_model       = None
_idx_to_cls  = None
_label_map   = None
_num_classes = None


def download_model():
    from huggingface_hub import hf_hub_download
    REPO = "noshin-nawar/silent-voices-model"
    if not os.path.exists(MODEL_PATH):
        print("Downloading model...")
        hf_hub_download(repo_id=REPO, filename="bangla_sign_model.h5", local_dir=BASE_DIR)
        print("✅ Model downloaded.")
    if not os.path.exists(CI_PATH):
        print("Downloading class_indices.json...")
        hf_hub_download(repo_id=REPO, filename="class_indices.json", local_dir=BASE_DIR)
        print("✅ class_indices.json downloaded.")


def load_everything():
    global _model, _idx_to_cls, _label_map, _num_classes

    if _model is not None:
        return True  # already loaded

    try:
        import tensorflow as tf
        from tensorflow.keras.models import load_model as tf_load

        download_model()

        print("Loading model...")
        _model = tf_load(MODEL_PATH)
        print("✅ Model loaded.")

        with open(CI_PATH,     encoding="utf-8") as f:
            ci = json.load(f)
        with open(LABELS_PATH, encoding="utf-8") as f:
            labels_raw = json.load(f)

        _label_map   = {**labels_raw["digits"], **labels_raw["alphabets"]}
        _idx_to_cls  = {v: k for k, v in ci.items()}
        _num_classes = len(ci)
        print(f"✅ {_num_classes} classes ready.")
        return True

    except Exception as e:
        print(f"❌ load_everything failed: {e}")
        print(traceback.format_exc())
        # Reset so next request tries again
        _model = None
        return False


def preprocess(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, 0)


def enrich(cls_name, confidence):
    info = _label_map.get(cls_name, {})
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
    return jsonify({"status": "ok", "message": "Silent Voices API 🤙"})


@app.route("/labels", methods=["GET"])
def get_labels():
    if not load_everything():
        return jsonify({"error": "Model failed to load. Check logs."}), 500
    return jsonify(_label_map)


@app.route("/predict", methods=["POST"])
def predict():
    # Load model — return clear error if it fails
    if not load_everything():
        return jsonify({"error": "Model not loaded. Check Render logs."}), 503

    # Parse image from request
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

    # Run prediction
    try:
        preds    = _model.predict(preprocess(img_bytes), verbose=0)[0]
        top5_idx = np.argsort(preds)[::-1][:5]

        prediction = enrich(_idx_to_cls[top5_idx[0]], float(preds[top5_idx[0]]))
        top5       = [enrich(_idx_to_cls[i], float(preds[i])) for i in top5_idx]

        all_scores = {
            _idx_to_cls[i]: {
                "confidence": round(float(preds[i]) * 100, 2),
                **{k: _label_map.get(_idx_to_cls[i], {}).get(k, "")
                   for k in ("display", "type", "name")}
            }
            for i in range(_num_classes)
        }

        return jsonify({"prediction": prediction, "top5": top5, "all_scores": all_scores})

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)