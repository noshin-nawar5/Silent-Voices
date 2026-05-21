# 🤙 হস্তচিহ্ন — Bangla Sign Language Recognizer

> Recognize **47 Bangla hand signs** — digits (০–৯), vowels (অ–ঔ), and consonants (ক–য) — from a single photo using MobileNetV2 transfer learning.

![ML](https://img.shields.io/badge/ML-TensorFlow%20%7C%20MobileNetV2-ff69b4?style=flat-square)
![Classes](https://img.shields.io/badge/Classes-47%20(10%20digits%20%2B%2037%20alphabets)-c084fc?style=flat-square)
![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-f43f5e?style=flat-square)
![Backend](https://img.shields.io/badge/Backend-Flask-a855f7?style=flat-square)
![Deploy FE](https://img.shields.io/badge/Deploy-Vercel-000?style=flat-square&logo=vercel)
![Deploy BE](https://img.shields.io/badge/Deploy-Render-46e3b7?style=flat-square)

---

## 📋 Classes — 47 Total

| Type | Count | Signs |
|------|-------|-------|
| 🔢 Digits | 10 | ০ ১ ২ ৩ ৪ ৫ ৬ ৭ ৮ ৯ |
| 🌸 Vowels (স্বরবর্ণ) | 11 | অ আ ই ঈ উ ঊ ঋ এ ঐ ও ঔ |
| ✦ Consonants (ব্যঞ্জনবর্ণ) | 26 | ক খ গ ঘ ঙ চ ছ জ ঝ ঞ ট ঠ ড ঢ ণ ত থ দ ধ ন প ফ ব ভ ম য |

---

## 📁 Project Structure

```
bangla-sign-lang/
├── dataset/                                        ← your raw dataset (not committed)
│   ├── Bangla Sign Language Dataset - Sign Digits/
│   │   └── User XX (Gender, Age)/
│   │       └── Sign N/
│   │           └── Input Images/
│   │               └── Sign N - Sample (k).jpg
│   └── Bangla Sign Language Dataset - Sign Alphabets/
│       └── User XX - Gender, Age/
│           └── sign NN/
│               └── Input Images - sign NN/
│                   └── Sign NN - Sample (k).jpg
│
├── ml/
│   ├── train_model.ipynb     ← full training pipeline
│   └── requirements.txt
│
├── backend/
│   ├── app.py                ← Flask REST API (47 classes)
│   ├── labels.json           ← class → Bangla char mapping
│   ├── requirements.txt
│   └── render.yaml           ← Render deploy config
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx           ← main UI (upload + result + reference)
│   │   ├── App.css           ← girly theme
│   │   ├── labels.js         ← mirrored label map for UI
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── vercel.json
│   └── .env.example
│
├── .gitignore
└── README.md
```

---

## 🚀 Step-by-Step Build Guide

### Step 1 — Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/bangla-sign-lang.git
cd bangla-sign-lang
```

### Step 2 — Add Your Dataset

Place the raw dataset folders inside a `dataset/` folder at the project root:

```
dataset/
├── Bangla Sign Language Dataset - Sign Digits/
└── Bangla Sign Language Dataset - Sign Alphabets/
```

The `dataset/` folder is gitignored — it stays local.

---

### Step 3 — Train the Model

```bash
cd ml
pip install -r requirements.txt
jupyter notebook train_model.ipynb
```

**Run all cells in order.** The notebook will:

1. Flatten and merge both raw datasets into `ml/processed_dataset/`  
   — 10 digit folders (`digit_0` … `digit_9`)  
   — 37 alphabet folders (`alpha_00` … `alpha_36`)  
2. Show a class distribution bar chart
3. Show a sample image grid for all 47 classes
4. Apply data augmentation
5. Train MobileNetV2 in **2 phases**:
   - Phase 1: Only the custom head (base frozen) — faster convergence
   - Phase 2: Fine-tune last 40 base layers — higher accuracy
6. Plot training curves and confusion matrix (47×47)
7. Export `bangla_sign_model.h5` + `class_indices.json` → auto-copied to `backend/`

> 💡 **Tip**: On free Google Colab GPU this takes ~30–60 min. Locally on CPU: ~2–4 hours.  
> Expected accuracy: **90–96%** depending on dataset size per class.

---

### Step 4 — Run Backend Locally

```bash
cd backend
pip install -r requirements.txt
python app.py
# → http://localhost:5000
```

Test the health endpoint:
```bash
curl http://localhost:5000/
```

Test prediction:
```bash
curl -X POST http://localhost:5000/predict \
  -F "file=@/path/to/hand_sign.jpg"
```

---

### Step 5 — Run Frontend Locally

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local → VITE_API_URL=http://localhost:5000
npm run dev
# → http://localhost:5173
```

---

### Step 6 — Deploy Backend on Render

> ⚠️ **Model file handling**: `.h5` files are too large for git. Use one of:
>
> **Option A — Git LFS** (simplest):
> ```bash
> git lfs install
> git lfs track "*.h5"
> git add .gitattributes backend/bangla_sign_model.h5 backend/class_indices.json
> git commit -m "add model via LFS"
> git push
> ```
>
> **Option B — HuggingFace Hub** (recommended for free Render tier):
> 1. Upload your `.h5` to [huggingface.co](https://huggingface.co) (free, unlimited model hosting)
> 2. Add to `backend/app.py` before `model = load_model(...)`:
> ```python
> from huggingface_hub import hf_hub_download
> import os
> if not os.path.exists(MODEL_PATH):
>     hf_hub_download(
>         repo_id="YOUR_HF_USERNAME/bangla-sign-model",
>         filename="bangla_sign_model.h5",
>         local_dir=BASE_DIR
>     )
> ```
> 3. Add `huggingface_hub==0.23.4` to `backend/requirements.txt`

**Deploy steps on Render:**
1. Push your repo to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect GitHub repo → select `backend/` as root directory
4. Render auto-reads `render.yaml`
5. Click **Deploy** — note your URL (e.g. `https://bangla-sign-backend.onrender.com`)

---

### Step 7 — Deploy Frontend on Vercel

1. Go to [vercel.com](https://vercel.com) → **New Project**
2. Import your GitHub repo
3. Set **Root Directory** → `frontend`
4. Add Environment Variable:
   - Key: `VITE_API_URL`
   - Value: `https://bangla-sign-backend.onrender.com`
5. Click **Deploy** 🎉

---

## 🧠 Model Details

| Property | Value |
|----------|-------|
| Base Model | MobileNetV2 (ImageNet pretrained) |
| Input Size | 224 × 224 × 3 |
| Total Classes | 47 |
| Digits | 10 (sign_0 – sign_9) |
| Vowels | 11 (alpha_00 – alpha_10) |
| Consonants | 26 (alpha_11 – alpha_36) |
| Head Architecture | GAP → BN → Dense(512) → Dropout(0.45) → Dense(256) → Dropout(0.35) → Softmax(47) |
| Phase 1 LR | 1e-3 (head only) |
| Phase 2 LR | 1e-5 (last 40 base layers unfrozen) |
| Augmentation | rotation ±12°, shift ±8%, zoom ±12%, brightness ±15% |

---

## 🌸 API Reference

### `GET /`
Health check + class count.

### `GET /labels`
Returns the full label map for all 47 classes.

### `POST /predict`

**Input** (choose one):
- Multipart form: `file` = image file
- JSON: `{ "image": "<base64 data URL>" }`

**Response:**
```json
{
  "prediction": {
    "class":      "alpha_11",
    "display":    "ক",
    "roman":      "ko",
    "name":       "ক",
    "type":       "consonant",
    "confidence": 94.71
  },
  "top5": [ ... ],
  "all_scores": {
    "alpha_00": { "display": "অ", "type": "vowel",     "confidence": 0.02 },
    "alpha_11": { "display": "ক", "type": "consonant", "confidence": 94.71 },
    ...
  }
}
```

---

## 🗄️ Dataset Info

| Dataset | Signs | Users | Samples/sign/user | Total est. |
|---------|-------|-------|-------------------|------------|
| Sign Digits | 10 (০–৯) | 10 | ~100 | ~10,000 |
| Sign Alphabets | 37 (অ–য) | 10 | ~90 | ~33,300 |
| **Combined** | **47** | **10** | — | **~43,300** |

---

## 📦 Dependencies

**ML (Python 3.9+):** `tensorflow`, `pillow`, `numpy`, `matplotlib`, `scikit-learn`, `seaborn`  
**Backend:** `flask`, `flask-cors`, `tensorflow`, `pillow`, `numpy`, `gunicorn`  
**Frontend:** `react`, `framer-motion`, `axios`, `react-dropzone`

---

## 📄 License
MIT — free to use and adapt.

---

Made with 💗 for Bangla Sign Language accessibility.
