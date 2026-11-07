"""Train the PhishGuard model:  python train.py [path/to/urls.csv]"""
import sys
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from features import extract_features, FEATURE_NAMES

path = sys.argv[1] if len(sys.argv) > 1 else "data/urls.csv"
df = pd.read_csv(path).dropna(subset=["url", "label"])
X = pd.DataFrame([extract_features(u) for u in df["url"]], columns=FEATURE_NAMES)
y = df["label"].astype(int)

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
model.fit(X_tr, y_tr)

pred = model.predict(X_te)
print(classification_report(y_te, pred, target_names=["legitimate", "phishing"]))
print("Confusion matrix:\n", confusion_matrix(y_te, pred))
print("\nTop features:")
for n, i in sorted(zip(FEATURE_NAMES, model.feature_importances_), key=lambda t: -t[1])[:6]:
    print(f"  {n:24s}{i:.3f}")

joblib.dump(model, "models/phishguard.joblib")
print("\nSaved models/phishguard.joblib")
