"""Two opposing Reviewer Agents that must reach consensus before Writer finalises."""
from __future__ import annotations

import logging
from dataclasses import dataclass

from src.config import settings

_log = logging.getLogger("debate_reviewer")

SYSTEM_DL = (
    "You are the Deep Learning Expert Reviewer. "
    "Focus on model architecture, training stability, and empirical evidence. "
    "Be sceptical of claims not backed by ablations or baselines."
)
SYSTEM_NLP = (
    "You are the NLP & Linguistics Expert Reviewer. "
    "Focus on language quality, HebrewRTL correctness, citation accuracy, "
    "and clarity of explanation for non-ML readers."
)
SYSTEM_ARBITER = (
    "You are a neutral Arbiter. Given two reviews, produce a single merged "
    "review that addresses all valid concerns from both sides."
)


@dataclass
class ReviewResult:
    dl_review: str
    nlp_review: str
    consensus: str
    rounds: int
    agreed: bool


def _call(system: str, user: str) -> str:
    from src.agents.base import gatekeeper  # lazy: avoids import at module load
    msg = gatekeeper.call(
        model=settings.MODEL_NAME,
        max_tokens=512,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return msg.content[0].text.strip()


def _cosine_sim_approx(a: str, b: str) -> float:
    sa, sb = set(a.lower().split()), set(b.lower().split())
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / (len(sa | sb) + 1e-9)


def review(draft: str, max_rounds: int = 3,
           consensus_threshold: float = 0.55) -> ReviewResult:
    """Run DL-Expert vs NLP-Expert debate; return consensus or arbiter ruling."""
    dl_rev = nlp_rev = ""
    agreed = False

    for rnd in range(1, max_rounds + 1):
        _log.info("Debate round %d/%d", rnd, max_rounds)
        prior_nlp = nlp_rev or "none"
        prompt = f"Review this draft:\n\n{draft}\n\nPrior NLP review: {prior_nlp}"
        dl_rev = _call(SYSTEM_DL, prompt)

        prior_dl = dl_rev or "none"
        prompt = f"Review this draft:\n\n{draft}\n\nPrior DL review: {prior_dl}"
        nlp_rev = _call(SYSTEM_NLP, prompt)

        sim = _cosine_sim_approx(dl_rev, nlp_rev)
        _log.info("Round %d sim=%.3f thresh=%.2f", rnd, sim, consensus_threshold)
        if sim >= consensus_threshold:
            agreed = True
            consensus = f"[Round {rnd} consensus]\n{dl_rev}\n\n---\n{nlp_rev}"
            break
    else:
        _log.warning("No consensus after %d rounds; invoking Arbiter.", max_rounds)
        arbiter_prompt = (
            f"DL review:\n{dl_rev}\n\nNLP review:\n{nlp_rev}\n\n"
            f"Draft:\n{draft[:800]}"
        )
        consensus = _call(SYSTEM_ARBITER, arbiter_prompt)

    return ReviewResult(
        dl_review=dl_rev,
        nlp_review=nlp_rev,
        consensus=consensus,
        rounds=rnd,
        agreed=agreed,
    )
