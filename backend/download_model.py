import requests, os

BASE = "https://huggingface.co/noshin-nawar/silent-voices-model/resolve/main"
DIR  = os.path.dirname(os.path.abspath(__file__))

for name in ["bangla_sign_model.h5", "class_indices.json"]:
    dest = os.path.join(DIR, name)
    if os.path.exists(dest):
        print(f"✅ {name} already exists")
        continue
    print(f"⬇️  Downloading {name} ...")
    r = requests.get(f"{BASE}/{name}", stream=True, timeout=300)
    r.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
    print(f"✅ {name} done ({os.path.getsize(dest)/1024/1024:.1f} MB)")