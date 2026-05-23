import requests, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = "https://huggingface.co/noshin-nawar/silent-voices-model/resolve/main"

files = {
    "bangla_sign_model.h5": f"{REPO}/bangla_sign_model.h5",
    "class_indices.json":   f"{REPO}/class_indices.json",
}

for filename, url in files.items():
    dest = os.path.join(BASE_DIR, filename)
    if os.path.exists(dest):
        print(f"✅ {filename} already exists")
        continue
    print(f"⬇️  Downloading {filename}...")
    r = requests.get(url, stream=True, timeout=300)
    r.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    mb = os.path.getsize(dest) / 1024 / 1024
    print(f"✅ {filename} downloaded ({mb:.1f} MB)")