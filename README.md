<div align="center">

# 🤙 Silent Voices
### Bangla Sign Language Recognition System

*Bridging the communication gap through AI-powered hand sign recognition*

<br/>

[![Live Demo](https://img.shields.io/badge/🌸_Live_Demo-Visit_Site-f43f5e?style=for-the-badge)](https://silent-voices-three.vercel.app)
[![API Status](https://img.shields.io/badge/API-Render-46e3b7?style=for-the-badge&logo=render)](https://silent-voices-1.onrender.com)
[![HuggingFace](https://img.shields.io/badge/🤗_Model-HuggingFace-ffcc00?style=for-the-badge)](https://huggingface.co/noshin-nawar/silent-voices-model)
[![License](https://img.shields.io/badge/License-MIT-a855f7?style=for-the-badge)](LICENSE)

<br/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-000000?style=flat-square&logo=vercel&logoColor=white)
![Render](https://img.shields.io/badge/Render-Deployed-46e3b7?style=flat-square)

<br/>

> 🌐 **Live:** [silent-voices-three.vercel.app](https://silent-voices-three.vercel.app)
>
> 🔌 **API:** [silent-voices-1.onrender.com](https://silent-voices-1.onrender.com)

</div>

---

## 📌 Overview

**Silent Voices** is an AI-powered web application that recognizes **47 Bangla Sign Language signs** from a hand photo — covering the full digit set and alphabet.

Upload any hand-sign image and the model instantly identifies the corresponding Bangla character with confidence scores.

| Category | Count | Signs |
|----------|-------|-------|
| 🔢 Digits | 10 | ০ ১ ২ ৩ ৪ ৫ ৬ ৭ ৮ ৯ |
| 🌸 Vowels (স্বরবর্ণ) | 11 | অ আ ই ঈ উ ঊ ঋ এ ঐ ও ঔ |
| ✦ Consonants (ব্যঞ্জনবর্ণ) | 26 | ক খ গ ঘ ঙ চ ছ জ ঝ ঞ ট ঠ ড ঢ ণ ত থ দ ধ ন প ফ ব ভ ম য |

---

## ✨ Features

- 🖼️ **Drag & drop** image upload
- ⚡ **Instant prediction** with confidence score
- 📊 **Bar chart** showing all 47 class scores
- 🏆 **Top 5 predictions** ranked by confidence
- 📖 **Interactive reference panel** — browse all signs by type
- 🌸 **Girly glassmorphism UI** — pink & lilac theme
- 📱 **Fully responsive** — works on mobile and desktop
- 🔌 **REST API** — integrate into any application

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| ML Model | MobileNetV2 Transfer Learning (TensorFlow 2.15) |
| Backend | Python · Flask · Gunicorn |
| Frontend | React 18 · Vite · Framer Motion |
| Model Hosting | HuggingFace Hub |
| Deployment (FE) | Vercel |
| Deployment (BE) | Render |

---

## 📁 Project Structure

```
Silent-Voices-/
├── 📓 ml/
│   ├── train_model.ipynb     # MobileNetV2 training pipeline (47 classes)
│   └── requirements.txt
├── 🐍 backend/
│   ├── app.py                # Flask REST API (lazy model loading)
│   ├── labels.json           # 47 class → Bangla character map
│   ├── requirements.txt
│   └── render.yaml
├── ⚛️ frontend/
│   ├── src/
│   │   ├── App.jsx           # Main UI
│   │   ├── App.css           # Girly pink/lilac theme
│   │   ├── labels.js         # Frontend label map
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── vercel.json
├── LICENSE
├── README.md
└── .gitignore
```

---

## 🚀 Local Setup

### Prerequisites
- Python 3.11+
- Node.js 18+

### 1. Clone
```bash
git clone https://github.com/noshin-nawar5/Silent-Voices-.git
cd Silent-Voices-
```

### 2. Backend
```bash
cd backend
pip install -r requirements.txt
# Download model from https://huggingface.co/noshin-nawar/silent-voices-model
# Place bangla_sign_model.h5 and class_indices.json in backend/
python app.py
# → http://localhost:5000
```

### 3. Frontend
```bash
cd frontend
npm install
cp .env.example .env.local
# Set VITE_API_URL=http://localhost:5000
npm run dev
# → http://localhost:5173
```

---

## 🧠 Model

| Property | Value |
|----------|-------|
| Architecture | MobileNetV2 + custom head |
| Input Size | 96 × 96 × 3 |
| Output | Softmax — 47 classes |
| Phase 1 | Head only, LR=1e-3, base frozen, 5 epochs |
| Phase 2 | Last 40 layers unfrozen, LR=1e-5, 5 epochs |
| Augmentation | Rotation, zoom, shift, brightness |
| Dataset | ~43,000 images · 10 users |

> 📦 **Pre-trained model:** [huggingface.co/noshin-nawar/silent-voices-model](https://huggingface.co/noshin-nawar/silent-voices-model)

---

## 🌐 API Reference

**Base URL:** `https://silent-voices-1.onrender.com`

> ⚠️ First request may take ~30s — Render free tier spins down after inactivity.

### `GET /`
```json
{ "status": "ok", "message": "Silent Voices API 🤙" }
```

### `GET /labels`
Returns full label map for all 47 classes.

### `POST /predict`

**Form data:** `file: <image>`  
**OR JSON:** `{ "image": "data:image/jpeg;base64,..." }`

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
  "all_scores": { ... }
}
```

---

## 📊 Dataset

| Dataset | Signs | Users | Est. Images |
|---------|-------|-------|-------------|
| Sign Digits | 10 (০–৯) | 10 | ~10,000 |
| Sign Alphabets | 37 (অ–য) | 10 | ~33,300 |
| **Combined** | **47** | **10** | **~43,300** |

> The dataset is not included in this repo — kept local for training only.

---

## 🚢 Deployment

### Frontend → [Vercel](https://silent-voices-three.vercel.app)
- Root directory: `frontend`
- Env var: `VITE_API_URL=https://silent-voices-1.onrender.com`

### Backend → [Render](https://silent-voices-1.onrender.com)
- Root directory: `backend`
- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1`
- Model auto-downloads from HuggingFace on first request

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m 'feat: your feature'`
4. Push and open a Pull Request

---

## 📄 License

MIT — see [LICENSE](LICENSE)

---

<div align="center">

Made with 💗 by **Noshin Nawar**

[![GitHub](https://img.shields.io/badge/GitHub-noshin--nawar5-181717?style=flat-square&logo=github)](https://github.com/noshin-nawar5)
[![HuggingFace](https://img.shields.io/badge/🤗-noshin--nawar-ffcc00?style=flat-square)](https://huggingface.co/noshin-nawar)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-noshin--nawar5-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/noshin-nawar5)

<sub>Built for Bangla Sign Language accessibility 🤙</sub>

</div>
