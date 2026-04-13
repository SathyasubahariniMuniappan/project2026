"""
Simple Claim Verification
Basic verification using keyword matching.
"""

from typing import List, Dict, Any


# Simple medical knowledge base
MEDICAL_KNOWLEDGE = {
    "metformin": "diabetes medication, 500-2000 mg/day",
    "aspirin": "pain reliever, 75-325 mg/day",
    "lisinopril": "blood pressure medication, 5-40 mg/day",
    "diabetes": "blood sugar disorder",
    "hypertension": "high blood pressure",
    "covid": "viral respiratory illness",
}

# Known wrong facts
KNOWN_CONTRADICTIONS = [
    ("covid", "water"),  # COVID doesn't spread through water
    ("covid", "bacterium"),  # COVID is viral, not bacterial
]


def verify_claim_simple(claim: str) -> Dict[str, Any]:
    """
    Simple verification: check if claim contains known medical terms and contradictions.
    """
    claim_lower = claim.lower()
    matched_topics = []

    for topic, info in MEDICAL_KNOWLEDGE.items():
        if topic in claim_lower:
            matched_topics.append(topic)

    # Check for known contradictions
    is_contradicted = False
    for topic, wrong_term in KNOWN_CONTRADICTIONS:
        if topic in claim_lower and wrong_term in claim_lower:
            is_contradicted = True
            break

    # Simple dosage check for aspirin
    if "aspirin" in claim_lower:
        import re
        numbers = re.findall(r'(\d+)', claim)
        if numbers and int(numbers[0]) > 1000:  # Rough check for high dose
            is_contradicted = True

    if is_contradicted:
        verdict = "CONTRADICTED"
        confidence = 0.9
        explanation = "Contains known medical contradiction or implausible dosage"
    elif matched_topics:
        verdict = "SUPPORTED"
        confidence = 0.8
        explanation = f"Contains known medical terms: {', '.join(matched_topics)}"
    else:
        verdict = "UNVERIFIED"
        confidence = 0.3
        explanation = "No known medical terms found"

    return {
        "claim": claim,
        "verdict": verdict,
        "confidence": confidence,
        "explanation": explanation,
        "evidence_used": matched_topics,
        "is_hallucinated": verdict in ["CONTRADICTED", "UNVERIFIED"]
    }


def verify_all_claims_simple(claims: List[str]) -> List[Dict[str, Any]]:
    """
    Verify a list of claims using simple matching.
    """
    results = []
    for claim in claims:
        result = verify_claim_simple(claim)
        results.append(result)
    return results


# Keep old function names for compatibility
def verify_claim(claim: str, retrieved_evidence: List[str] = None) -> Dict[str, Any]:
    return verify_claim_simple(claim)


def verify_all_claims(claims: List[str], retrieved_evidence_map: Dict[str, List[str]] = None) -> List[Dict[str, Any]]:
    return verify_all_claims_simple(claims)
