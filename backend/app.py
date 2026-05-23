import os, io, json, base64, traceback, sys
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

_model       = None
_idx_to_cls  = None
_label_map   = None
_num_classes = None
_load_error  = None   # stores last error message


def download_model():
    """Download via direct requests — more reliable than hf_hub_download on Render."""
    import requests

    files = {
        MODEL_PATH: "https://huggingface.co/noshin-nawar/silent-voices-model/resolve/main/bangla_sign_model.h5",
        CI_PATH:    "https://huggingface.co/noshin-nawar/silent-voices-model/resolve/main/class_indices.json",
    }

    for dest, url in files.items():
        if os.path.exists(dest):
            print(f"✅ Already exists: {os.path.basename(dest)}", flush=True)
            continue
        print(f"⬇️  Downloading {os.path.basename(dest)} from HuggingFace...", flush=True)
        r = requests.get(url, stream=True, timeout=300)
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        size_mb = os.path.getsize(dest) / (1024 * 1024)
        print(f"✅ Downloaded {os.path.basename(dest)} ({size_mb:.1f} MB)", flush=True)


def load_everything():
    global _model, _idx_to_cls, _label_map, _num_classes, _load_error

    if _model is not None:
        return True

    try:
        print("=== load_everything() START ===", flush=True)

        # Step 1 — download files
        download_model()

        # Step 2 — verify files exist
        for path in [MODEL_PATH, CI_PATH, LABELS_PATH]:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Missing file: {path}")
            print(f"✅ File OK: {path}", flush=True)

        # Step 3 — load TF model
        print("Importing TensorFlow...", flush=True)
        import tensorflow as tf
        from tensorflow.keras.models import load_model as tf_load
        print(f"TF version: {tf.__version__}", flush=True)

        print("Loading model...", flush=True)
        _model = tf_load(MODEL_PATH)
        print("✅ Model loaded.", flush=True)

        # Step 4 — load label files
        with open(CI_PATH,     encoding="utf-8") as f: ci         = json.load(f)
        with open(LABELS_PATH, encoding="utf-8") as f: labels_raw = json.load(f)

        _label_map   = {**labels_raw["digits"], **labels_raw["alphabets"]}
        _idx_to_cls  = {v: k for k, v in ci.items()}
        _num_classes = len(ci)
        _load_error  = None
        print(f"✅ {_num_classes} classes ready.", flush=True)
        print("=== load_everything() DONE ===", flush=True)
        return True

    except Exception as e:
        _load_error = str(e)
        _model = None
        print(f"❌ load_everything FAILED: {e}", flush=True)
        print(traceback.format_exc(), flush=True)
        sys.stdout.flush()
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


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Silent Voices API 🤙"})


@app.route("/labels", methods=["GET"])
def get_labels():
    if not load_everything():
        return jsonify({"error": "Model failed to load", "detail": _load_error}), 503
    return jsonify(_label_map)


@app.route("/predict", methods=["POST"])
def predict():
    if not load_everything():
        return jsonify({"error": "Model failed to load", "detail": _load_error}), 503

    if "file" in request.files:
        f = request.files["file"]
        if f.filename == "":
            return jsonify({"error": "No file selected"}), 400
        img_bytes = f.read()
    elif request.is_json:
        data = request.get_json()
        if "image" not in data:
            return jsonify({"error": "JSON must have 'image' key"}), 400
        img_bytes = base64.b64decode(data["image"].split(",")[-1])
    else:
        return jsonify({"error": "Send file or base64 image"}), 400

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