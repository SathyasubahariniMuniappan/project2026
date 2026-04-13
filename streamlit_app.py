"""
Simple Medical Hallucination Detector
Basic Streamlit app for checking medical claims.
"""

import streamlit as st
import re

from claim_verification import verify_all_claims_simple
from claim_scoring import run_scoring_pipeline


st.title("Medical Hallucination Detector")

st.write("Paste a medical summary to check for hallucinations.")

summary = st.text_area("Medical Summary", height=200)

if st.button("Check Summary"):
    if summary.strip():
        # Split into claims
        sentences = re.split(r'(?<=[.!?])\s+', summary.strip())
        claims = [s.strip() for s in sentences if len(s.strip()) > 10]

        st.write(f"Found {len(claims)} claims:")

        # Verify claims
        verification_results = verify_all_claims_simple(claims)

        # Score claims
        scored_claims, document_report = run_scoring_pipeline(verification_results)

        # Show document summary
        st.subheader("Document Summary")
        st.write(f"Overall Score: {document_report['overall_score']}/100")
        st.write(f"Risk Level: {document_report['overall_risk']}")
        st.write(f"Hallucination Rate: {document_report['hallucination_rate']:.1%}")

        # Show per-claim results
        st.subheader("Claim Results")
        for i, (vr, sc) in enumerate(zip(verification_results, scored_claims), 1):
            with st.expander(f"Claim {i}: {vr['claim'][:50]}..."):
                st.write(f"**Verdict:** {vr['verdict']}")
                st.write(f"**Confidence:** {vr['confidence']:.1%}")
                st.write(f"**Score:** {sc['final_score']}/100")
                st.write(f"**Risk:** {sc['risk_level']}")
                st.write(f"**Explanation:** {vr['explanation']}")
    else:
        st.error("Please enter a medical summary.")
