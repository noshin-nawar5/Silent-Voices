<div align="center">

<img src="https://raw.githubusercontent.com/noshin-nawar5/Silent-Voices-/main/assets/banner.png" alt="Silent Voices Banner" width="100%"/>

# 🤙 Silent Voices
### Bangla Sign Language Recognition System

*Bridging the communication gap through AI-powered hand sign recognition*

<br/>

[![Live Demo](https://img.shields.io/badge/🌸_Live_Demo-Visit_Site-f43f5e?style=for-the-badge)](https://silent-voices.vercel.app)
[![API Status](https://img.shields.io/badge/API-Render-46e3b7?style=for-the-badge&logo=render)](https://silent-voices-api.onrender.com)
[![License](https://img.shields.io/badge/License-MIT-a855f7?style=for-the-badge)](LICENSE)

<br/>

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.16-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-000000?style=flat-square&logo=vercel&logoColor=white)
![Render](https://img.shields.io/badge/Render-Deployed-46e3b7?style=flat-square)

<br/>

</div>

---

## 📌 Overview

**Silent Voices** is an AI-powered web application that recognizes **47 Bangla Sign Language signs** from a hand photo — covering the full alphabet and digit set.

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
| ML Model | MobileNetV2 (Transfer Learning, TensorFlow 2.16) |
| Backend | Python · Flask · Gunicorn |
| Frontend | React 18 · Vite · Framer Motion |
| Deployment (FE) | Vercel |
| Deployment (BE) | Render |
| Model Hosting | HuggingFace Hub |

---

## 📁 Project Structure

```
Silent-Voices-/
├── 📓 ml/
│   ├── train_model.ipynb     # MobileNetV2 training pipeline (47 classes)
│   └── requirements.txt
├── 🐍 backend/
│   ├── app.py                # Flask REST API
│   ├── labels.json           # 47 class → Bangla char map
│   ├── requirements.txt
│   └── render.yaml           # Render deploy config
├── ⚛️ frontend/
│   ├── src/
│   │   ├── App.jsx           # Main UI
│   │   ├── App.css           # Girly theme
│   │   ├── labels.js         # Frontend label map
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── vercel.json
├── 📄 LICENSE
├── 📄 README.md
└── 📄 .gitignore
```

---

## 🚀 Local Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/Silent-Voices-.git
cd Silent-Voices-
```

### 2. Backend

```bash
cd backend
pip install -r requirements.txt

# Download model files from HuggingFace (see Model section below)
# Place bangla_sign_model.h5 and class_indices.json in backend/

python app.py
# → http://localhost:5000
```

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local → VITE_API_URL=http://localhost:5000
npm run dev
# → http://localhost:5173
```

---

## 🧠 Model

| Property | Value |
|----------|-------|
| Architecture | MobileNetV2 + custom head |
| Input | 224 × 224 × 3 |
| Output | Softmax over 47 classes |
| Training | 2-phase transfer learning |
| Phase 1 | Head only, LR=1e-3, base frozen |
| Phase 2 | Last 40 layers unfrozen, LR=1e-5 |
| Augmentation | Rotation, zoom, shift, brightness |
| Dataset | ~43,000 images across 10 users |

> 📦 **Pre-trained model** available on HuggingFace Hub:
> [`YOUR_HF_USERNAME/silent-voices-model`](https://huggingface.co/YOUR_HF_USERNAME/silent-voices-model)

---

## 🌐 API Reference

**Base URL:** `https://silent-voices-api.onrender.com`

### `GET /`
Health check.
```json
{ "status": "ok", "classes": 47 }
```

### `GET /labels`
Returns full label map for all 47 classes.

### `POST /predict`

**Request** — multipart form:
```
file: <image file>
```

**Request** — JSON (base64):
```json
{ "image": "data:image/jpeg;base64,..." }
```

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
| Bangla Sign Language Dataset — Sign Digits | 10 | 10 | ~10,000 |
| Bangla Sign Language Dataset — Sign Alphabets | 37 | 10 | ~33,300 |
| **Combined** | **47** | **10** | **~43,300** |

> ⚠️ The dataset is **not included** in this repository. It is kept local for training only.

---

## 🚢 Deployment

### Frontend → Vercel

1. Import repo on [vercel.com](https://vercel.com)
2. Set root directory → `frontend`
3. Add env var: `VITE_API_URL=https://your-backend.onrender.com`
4. Deploy

### Backend → Render

1. Import repo on [render.com](https://render.com)
2. Set root directory → `backend`
3. Render auto-reads `render.yaml`
4. Deploy

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m 'feat: add your feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 👩‍💻 Author

Made with 💗 by **Noshin Nawar**

[![GitHub](https://img.shields.io/badge/GitHub-noshin-nawar5-181717?style=flat-square&logo=github)](https://github.com/noshin-nawar5)

---

<div align="center">
<sub>Built for Bangla Sign Language accessibility 🤙</sub>
</div>
