# 🛡️ PhishGuard

A basic machine-learning phishing URL detector.

**How it works:** each URL is converted into 17 lexical features (length, dots, hyphens,
IP-as-host, `@` symbol, suspicious keywords, risky TLDs, HTTPS, etc.) and classified by a
Random Forest model. No network requests are made to the URL being checked.

## Run it
```bash
pip install -r requirements.txt
python generate_data.py      # creates demo dataset (skip if you have a real one)
python train.py              # trains + prints metrics, saves models/phishguard.joblib
python predict.py http://paypal-verify-account.xyz/login https://www.google.com
python app.py                # web demo at http://127.0.0.1:5000
```

## Using a real dataset
Replace `data/urls.csv` with a CSV with columns `url,label` (1 = phishing, 0 = legitimate),
e.g. Kaggle "Phishing Site URLs" or PhishTank (phishing) + Tranco (legitimate), then re-run `python train.py`.

## Structure
- `features.py` – URL feature extraction
- `generate_data.py` – synthetic demo data
- `train.py` – training + evaluation
- `predict.py` – CLI / `check_url()` function
- `app.py`, `templates/` – Flask web demo

## Future work
Domain age / WHOIS, page-content features, browser extension, deep-learning (char-CNN) model.
