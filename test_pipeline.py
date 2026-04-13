"""
Integration test: Module 5 (Claim Verification) -> Module 6 (Claim Scoring)
Run with:  python test_pipeline.py
"""
from claim_verification import verify_all_claims
from claim_scoring import run_scoring_pipeline

claims = [
    "Metformin is used to treat type 2 diabetes at a dose of 500-2000 mg per day.",
    "Aspirin should be given at 5000 mg per day for pain management.",
    "Fasting blood glucose of 130 mg/dL indicates diabetes.",
    "COVID-19 is caused by a bacterium.",
    "The patient may have hypertension requiring further evaluation.",
    "Lisinopril is an ACE inhibitor used for hypertension.",
    "Normal hemoglobin for males is 13.5-17.5 g/dL.",
]

print("=" * 70)
print("END-TO-END PIPELINE TEST  (Module 5 + Module 6)")
print("=" * 70)

# Module 5: Verify all claims
verifications = verify_all_claims(claims)

# Module 6: Score all claims + document report
scored_claims, doc_report = run_scoring_pipeline(verifications)

print("\n-- Per-Claim Results --\n")
for sc, vr in zip(scored_claims, verifications):
    print(f"Claim   : {sc['claim']}")
    print(f"Verdict : {vr['verdict']:20s} | Score: {sc['final_score']:3d}/100 | Risk: {sc['risk_level']}")
    print(f"Action  : {sc['recommendation']}")
    print()

print("=" * 70)
print("DOCUMENT SUMMARY")
print("=" * 70)
print(doc_report["summary"])
print()
print("INTEGRATION TEST PASSED!")
