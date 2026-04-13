"""
Simple Claim Scoring
Basic scoring based on verification verdict.
"""

from typing import List, Dict, Any, Tuple


# Simple scoring
VERDICT_SCORES = {
    "SUPPORTED": 80,
    "PARTIALLY_SUPPORTED": 50,
    "UNVERIFIED": 30,
    "CONTRADICTED": 10,
}

VERDICT_RISKS = {
    "SUPPORTED": "LOW",
    "PARTIALLY_SUPPORTED": "MEDIUM",
    "UNVERIFIED": "HIGH",
    "CONTRADICTED": "CRITICAL",
}


def score_single_claim(verification_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simple scoring based on verdict.
    """
    verdict = verification_result.get("verdict", "UNVERIFIED")
    score = VERDICT_SCORES.get(verdict, 30)
    risk = VERDICT_RISKS.get(verdict, "HIGH")

    return {
        "claim": verification_result.get("claim", ""),
        "verdict": verdict,
        "final_score": score,
        "risk_level": risk,
        "recommendation": f"Risk: {risk}"
    }


def score_all_claims(verification_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [score_single_claim(vr) for vr in verification_results]


def compute_document_score(scored_claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Simple document score: average of all claim scores.
    """
    if not scored_claims:
        return {
            "overall_score": 100,
            "overall_risk": "LOW",
            "total_claims": 0,
            "summary": "No claims to evaluate.",
            "hallucination_rate": 0.0,
        }

    scores = [c["final_score"] for c in scored_claims]
    overall_score = int(sum(scores) / len(scores))

    # Simple risk based on average
    if overall_score >= 70:
        overall_risk = "LOW"
    elif overall_score >= 50:
        overall_risk = "MEDIUM"
    elif overall_score >= 30:
        overall_risk = "HIGH"
    else:
        overall_risk = "CRITICAL"

    hallucination_rate = sum(1 for c in scored_claims if c["verdict"] != "SUPPORTED") / len(scored_claims)

    summary = f"Document Score: {overall_score}/100 - Risk: {overall_risk}"

    return {
        "overall_score": overall_score,
        "overall_risk": overall_risk,
        "total_claims": len(scored_claims),
        "summary": summary,
        "hallucination_rate": hallucination_rate,
    }


def run_scoring_pipeline(verification_results: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    scored_claims = score_all_claims(verification_results)
    document_report = compute_document_score(scored_claims)
    return scored_claims, document_report
