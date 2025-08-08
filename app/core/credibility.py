from math import sqrt

from .config import get_settings


def wilson_lower_bound(upvotes: int, downvotes: int, z: float = 1.96) -> float:
    n = upvotes + downvotes
    if n == 0:
        return 0.0
    p_hat = upvotes / n
    denominator = 1 + z**2 / n
    centre_adj = p_hat + z**2 / (2 * n)
    adjusted_std = z * sqrt((p_hat * (1 - p_hat) + z**2 / (4 * n)) / n)
    lower_bound = (centre_adj - adjusted_std) / denominator
    return max(0.0, min(1.0, lower_bound))


def compute_credibility(upvotes: int, downvotes: int, source_score: float) -> tuple[float, str]:
    settings = get_settings()
    wilson = wilson_lower_bound(upvotes, downvotes)
    # Weighted combination
    score = settings.credibility_wilson_weight * wilson + settings.credibility_source_weight * source_score

    if score >= settings.credibility_confirmed_threshold:
        tag = "Confirmed"
    elif score <= settings.credibility_rumor_threshold:
        tag = "Rumor"
    else:
        tag = "Pending"
    return score, tag


