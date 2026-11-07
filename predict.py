"""CLI:  python predict.py <url> [<url> ...]"""
import sys
import joblib
import pandas as pd
from features import extract_features, FEATURE_NAMES

_model = None


def check_url(url: str) -> dict:
    global _model
    if _model is None:
        _model = joblib.load("models/phishguard.joblib")
    X = pd.DataFrame([extract_features(url)], columns=FEATURE_NAMES)
    p = float(_model.predict_proba(X)[0][1])
    return {"url": url, "phishing_probability": round(p, 3),
            "verdict": "PHISHING" if p >= 0.5 else "SAFE"}


if __name__ == "__main__":
    for u in sys.argv[1:]:
        r = check_url(u)
        print(f"{r['verdict']:9s} {r['phishing_probability']:.2f}  {r['url']}")
