# Simple Medical Hallucination Detector

A basic tool to check medical summaries for potential hallucinations using simple keyword matching.

## Files

- `claim_verification.py` - Simple claim verification
- `claim_scoring.py` - Basic scoring system
- `streamlit_app.py` - Web interface
- `full_pipeline_demo.py` - Command-line demo

## How to Run

### Web App
```bash
python -m streamlit run streamlit_app.py
```

### Command Line
```bash
python full_pipeline_demo.py
```

**Test claim verification:**
```bash
python claim_verification.py
```

**Test claim scoring:**
```bash
python claim_scoring.py
```

---

## 📊 What the System Does

### Step 1: Decomposition
Splits medical summary into atomic claims

### Step 2: Verification
Checks each claim:
- ✅ Numeric plausibility (dosages, vitals, lab values)
- ✅ Known factual contradictions (COVID-19 transmission, etc.)
- ✅ Evidence matching from knowledge base

### Step 3: Scoring
Assigns reliability score 0-100 and risk level:
- 🟢 **LOW** (75-100): Factually reliable
- 🟡 **MEDIUM** (50-74): Partially supported
- 🔴 **HIGH** (25-49): Unverified
- 🔴 **CRITICAL** (0-24): Contradicts evidence

### Step 4: Correction Suggestions
Proposes specific corrections for hallucinated claims

---

## 📋 Verification Verdicts

| Verdict | Meaning |
|---------|---------|
| **SUPPORTED** | Claim matches evidence, confident |
| **PARTIALLY_SUPPORTED** | Claim relates to known topics, limited external evidence |
| **UNVERIFIED** | No matching evidence in knowledge base |
| **CONTRADICTED** | Claim contradicts medical evidence |

---

## 🔧 Example Usage

**Input Summary:**
```
The patient was treated with 5000 mg aspirin daily. 
COVID-19 is transmitted through contaminated water. 
Metformin 500-2000 mg per day was prescribed for diabetes.
```

**Output:**
```
Claim 1: "The patient was treated with 5000 mg aspirin daily"
  Verdict: CONTRADICTED
  Score: 11/100 (CRITICAL)
  Issue: Dose 5000 mg exceeds known maximum (4000 mg/day)
  Correction: Revise to at most 4000 mg/day

Claim 2: "COVID-19 is transmitted through contaminated water"
  Verdict: CONTRADICTED
  Score: 11/100 (CRITICAL)
  Issue: COVID-19 spreads via respiratory droplets/aerosols
  Correction: COVID-19 spreads through respiratory droplets and aerosols

Claim 3: "Metformin 500-2000 mg per day was prescribed for diabetes"
  Verdict: PARTIALLY_SUPPORTED
  Score: 61/100 (MEDIUM)
  Correction: Add external evidence/references

Document Score: 37/100 — HIGH RISK
Hallucination Rate: 100.0%
```

---

## 🛠️ Tech Stack

- **Python** - Core language
- **Streamlit** - Web UI
- **spaCy** - NLP (for sentence splitting)
- **BioBERT/PubMedBERT** - Ready for integration

---

## 📝 Notes

- The knowledge base (`MEDICAL_EVIDENCE_DB`) is built-in with dosages, diseases, lab values
- All verdicts and scoring are explainable with breakdowns
- System detects 4 verdict types: SUPPORTED, PARTIALLY_SUPPORTED, UNVERIFIED, CONTRADICTED
- Risk levels weighted: CONTRADICTED claims pull score down harder

---

**Status:** ✅ Fully operational - both claim verification and scoring modules integrated
