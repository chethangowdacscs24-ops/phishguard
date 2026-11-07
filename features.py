"""URL feature extraction for PhishGuard (lexical features only, no network calls)."""
import re
from urllib.parse import urlparse

SUSPICIOUS_WORDS = ["login", "verify", "secure", "account", "update", "bank", "signin",
                    "confirm", "password", "paypal", "wallet", "free", "bonus", "suspend"]
SHORTENERS = ["bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd", "cutt.ly"]
RISKY_TLDS = [".xyz", ".top", ".tk", ".ml", ".ga", ".cf", ".click", ".work", ".zip"]

FEATURE_NAMES = [
    "url_length", "hostname_length", "path_length", "num_dots", "num_hyphens",
    "num_digits", "num_special_chars", "num_subdomains", "has_ip", "has_at_symbol",
    "uses_https", "has_port", "suspicious_word_count", "is_shortener", "risky_tld",
    "digit_ratio", "double_slash_in_path",
]


def extract_features(url: str) -> list:
    url = url.strip()
    parsed = urlparse(url if "://" in url else "http://" + url)
    host = parsed.hostname or ""
    path = parsed.path or ""
    low = url.lower()

    num_digits = sum(c.isdigit() for c in url)
    parts = host.split(".")
    return [
        len(url),
        len(host),
        len(path),
        url.count("."),
        url.count("-"),
        num_digits,
        len(re.findall(r"[^A-Za-z0-9]", url)),
        max(len(parts) - 2, 0),
        int(bool(re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host))),
        int("@" in url),
        int(parsed.scheme == "https"),
        int(parsed.port is not None),
        sum(w in low for w in SUSPICIOUS_WORDS),
        int(any(s in host for s in SHORTENERS)),
        int(any(host.endswith(t) for t in RISKY_TLDS)),
        num_digits / max(len(url), 1),
        int("//" in path),
    ]
