import re
import hashlib

_re_ws = re.compile(r"\s+")
_re_punct = re.compile(r"[^a-z0-9\s]")

STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "of",
    "to",
    "in",
    "on",
    "for",
    "with",
    "from",
    "by",
}


def normalize_title(title: str) -> str:
    text = title.lower()
    text = _re_punct.sub(" ", text)
    tokens = [t for t in _re_ws.split(text) if t and t not in STOPWORDS]
    return " ".join(tokens)


def dedup_fingerprint(title: str) -> str:
    norm = normalize_title(title)
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


