# Changelog

All notable changes to Silent Voices are documented here.

---

## [1.0.0] — 2026-05-21

### 🎉 Initial Release

#### Added
- MobileNetV2 transfer learning model — 47 class Bangla Sign Language recognition
- Digits dataset support (০–৯, Signs 0–9)
- Alphabets dataset support (অ–য, Signs 00–36) — 11 vowels + 26 consonants
- 2-phase training pipeline in Jupyter Notebook (frozen head → fine-tune)
- Flask REST API with `/predict` and `/labels` endpoints
- React + Vite frontend with girly glassmorphism theme
- Drag & drop image upload with preview
- Confidence bar chart for all 47 classes
- Top 5 predictions panel
- Interactive sign reference panel with 3 tabs (Digits / Vowels / Consonants)
- Vercel deployment config for frontend
- Render deployment config for backend
- Full README with setup guide, API docs, dataset info
- MIT License

---

[1.0.0]: https://github.com/YOUR_USERNAME/Silent-Voices-/releases/tag/v1.0.0
