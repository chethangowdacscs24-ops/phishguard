"""Generates a SYNTHETIC demo dataset (data/urls.csv).
For the real project, replace data/urls.csv with a real dataset
(columns: url,label  where label 1 = phishing, 0 = legitimate),
e.g. from Kaggle 'Phishing Site URLs' or PhishTank + Tranco top sites."""
import random
import pandas as pd

random.seed(42)
legit_domains = ["google.com", "wikipedia.org", "github.com", "amazon.in", "flipkart.com",
                 "youtube.com", "microsoft.com", "apple.com", "stackoverflow.com", "bbc.com",
                 "linkedin.com", "nytimes.com", "irctc.co.in", "sbi.co.in", "hdfcbank.com"]
legit_paths = ["", "/", "/about", "/products/item123", "/search?q=python", "/docs/intro",
               "/news/2024/story", "/help", "/contact", "/watch?v=abc123"]
brands = ["paypal", "sbi", "hdfc", "amazon", "netflix", "microsoft", "apple", "icici", "google"]
words = ["login", "verify", "secure", "account", "update", "confirm", "signin", "password"]
bad_tlds = [".xyz", ".top", ".tk", ".ml", ".click", ".work", ".com", ".net", ".info"]


def legit():
    return random.choice(["https://", "https://www.", "http://www."]) + \
        random.choice(legit_domains) + random.choice(legit_paths)


def phish():
    k = random.randint(0, 4)
    b, w1, w2 = random.choice(brands), random.choice(words), random.choice(words)
    tld = random.choice(bad_tlds)
    scheme = random.choice(["http://", "http://", "https://"])
    if k == 0:
        ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
        return f"http://{ip}/{b}/{w1}.php?id={random.randint(1000, 99999)}"
    if k == 1:
        return f"{scheme}{b}-{w1}-{w2}{tld}/{w2}/index.html"
    if k == 2:
        return f"{scheme}{w1}.{b}.{random.choice(['secure','portal','app'])}-{w2}{tld}/{w1}?session={random.randint(10**6, 10**9)}"
    if k == 3:
        return f"{scheme}{b}.com@{random.choice(['evil','free-bonus','x1y2z3'])}{tld}/{w1}"
    return f"{random.choice(['http://bit.ly/','http://tinyurl.com/'])}{random.randint(10**4,10**6)}"


rows = [(legit(), 0) for _ in range(1500)] + [(phish(), 1) for _ in range(1500)]
random.shuffle(rows)
pd.DataFrame(rows, columns=["url", "label"]).to_csv("data/urls.csv", index=False)
print("Wrote data/urls.csv with", len(rows), "rows")
