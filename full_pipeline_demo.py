"""
Simple Pipeline Demo
Basic demo of the hallucination detection pipeline.
"""

from claim_verification import verify_all_claims_simple
from claim_scoring import run_scoring_pipeline
import re


def main():
    print("Medical Hallucination Detection Demo")
    print("=" * 50)

    # Sample medical summary
    medical_summary = """
    Patient has diabetes. Metformin is prescribed at 500 mg per day.
    Aspirin should be given at 5000 mg per day for heart protection.
    COVID-19 spreads through water.
    """

    # Split into claims
    sentences = re.split(r'(?<=[.!?])\s+', medical_summary.strip())
    claims = [s.strip() for s in sentences if len(s.strip()) > 5]

    print(f"Found {len(claims)} claims:")
    for i, claim in enumerate(claims, 1):
        print(f"  {i}. {claim}")

    # Verify claims
    print("\nVerifying claims...")
    verification_results = verify_all_claims_simple(claims)

    # Score claims
    print("\nScoring claims...")
    scored_claims, document_report = run_scoring_pipeline(verification_results)

    # Show results
    print("\nResults:")
    for i, (vr, sc) in enumerate(zip(verification_results, scored_claims), 1):
        print(f"\nClaim {i}: {vr['claim']}")
        print(f"  Verdict: {vr['verdict']} (confidence: {vr['confidence']:.1%})")
        print(f"  Score: {sc['final_score']}/100 (risk: {sc['risk_level']})")

    print(f"\nDocument Summary:")
    print(f"  Overall Score: {document_report['overall_score']}/100")
    print(f"  Risk Level: {document_report['overall_risk']}")
    print(f"  Hallucination Rate: {document_report['hallucination_rate']:.1%}")


if __name__ == "__main__":
    main()
