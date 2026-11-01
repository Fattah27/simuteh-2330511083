"""praproses.py: rangkaian praproses SIMUTEH (dipakai ulang mulai P5)."""
import json
import cv2
import numpy as np

PARAM_BAWAAN = {
    "lebar": 640,        # sampling: lebar citra kerja (piksel)
    "gamma": 1.0,        # < 1 mencerahkan, > 1 menggelapkan
    "clahe_clip": 2.0,   # 0 berarti CLAHE tidak dipakai
    "clahe_tile": 8,
    "penapis": "median", # "none", "rerata", "gaussian", "median"
    "kernel": 3,
    "sigma": 1.0,
    "tajam_k": 0.0,      # 0 berarti tanpa penajaman
}

def praproses(img_bgr, p=None):
    """Urutan: ubah ukuran -> gamma -> CLAHE kanal V -> redam derau -> tajamkan."""
    p = {**PARAM_BAWAAN, **(p or {})}

    # 1. Ubah ukuran: lebar = p["lebar"], rasio aspek tetap, INTER_AREA
    h, w = img_bgr.shape[:2]
    tinggi = int(round(h * p["lebar"] / w))
    img = cv2.resize(img_bgr, (p["lebar"], tinggi), interpolation=cv2.INTER_AREA)

    # 2. Koreksi gamma lewat tabel LUT (hanya bila gamma != 1)
    if p["gamma"] != 1:
        lut = np.array([255 * (i / 255) ** p["gamma"] for i in range(256)])
        img = cv2.LUT(img, lut.clip(0, 255).astype(np.uint8))

    # 3. CLAHE hanya pada kanal V (HSV), lalu kembali ke BGR
    if p["clahe_clip"] > 0:
        clahe = cv2.createCLAHE(clipLimit=p["clahe_clip"],
                                tileGridSize=(p["clahe_tile"], p["clahe_tile"]))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = clahe.apply(hsv[:, :, 2])
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # 4. Redam derau (ukuran kernel harus ganjil)
    k = int(p["kernel"])
    if p["penapis"] == "rerata":
        img = cv2.blur(img, (k, k))
    elif p["penapis"] == "gaussian":
        img = cv2.GaussianBlur(img, (k, k), p["sigma"])
    elif p["penapis"] == "median":
        img = cv2.medianBlur(img, k)
    # "none": tidak melakukan apa-apa

    # 5. Unsharp masking: citra + k * (citra - blur)
    if p["tajam_k"] > 0:
        blur = cv2.GaussianBlur(img, (5, 5), 1.0)
        img = cv2.addWeighted(img, 1 + p["tajam_k"], blur, -p["tajam_k"], 0)

    return img

def simpan_param(p, path="../hasil/param_praproses.json"):
    with open(path, "w") as f:
        json.dump({**PARAM_BAWAAN, **p}, f, indent=2)