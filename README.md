# 🛡️ PHI De-Identification Service

A Python + Flask based API to **de-identify Protected Health Information (PHI)** from unstructured medical reports.  
The service automatically replaces sensitive entities such as patient names, MRNs, SSNs, phone numbers, emails, dates, and addresses with placeholders.

---

## ✨ Features
- ✅ Detects **10 PHI entities**:
  - Patient Name → `[Deid: Name]`
  - Address → `[Deid: Address]`
  - Email → `[Deid: Email]`
  - Phone Number → `[Deid: PhoneNo]`
  - SSN → `[Deid: SSN]`
  - MRN (Medical Record Number) → `[Deid: MRN]`
  - Accession Number → `[Deid: Accession]`
  - Age → `[Deid: Age]`
  - Date (admission, discharge, DOB, etc.) → `[Deid: Date]`
  - Doctor’s Name → `[Deid: Doctor]`
- ✅ **Hybrid approach**:  
  - Regex patterns for structured data (MRN, SSN, Dates, Accession, etc.)  
  - spaCy Named Entity Recognition (NER) for free-text names/doctors.  
- ✅ REST API endpoint using Flask.  
- ✅ Configurable placeholders.  
- ✅ Easy integration into existing healthcare workflows.

---

## ⚙️ Installation

Clone the repo:

```bash
git clone https://github.com/VenkateshManohar022/Protected-Health-Information-Extraction-NLP.git
cd Protected-Health-Information-Extraction-NLP


Create a conda environment (recommended):
conda create -n manuh_env python=3.10 -y
conda activate manuh_env


Install dependencies:

pip install -r requirements.txt

### Anyway AUtodownlaod in Code,
This is for Reference

python -m spacy download en_core_web_lg


🚀 Usage

Run Flask API

python app.py

python app.py


Example CURL:

curl -X POST http://127.0.0.1:5000/deidentify \
-H "Content-Type: application/json" \
-d '{
  "report_text": "Patient John Doe visited on 12-Jan-2020. MRN: 123-45-678, Email: john.doe@example.com. Doctor: Jane Smith, M.D."
}'


{
  "deid_report": "Patient [Deid: Name] visited on [Deid: Date]. MRN: [Deid: MRN], Email: [Deid: Email]. Doctor: [Deid: Doctor].",
  "deid_entities": {
    "Name": ["John Doe"],
    "Date": ["12-Jan-2020"],
    "MRN": ["123-45-678"],
    "Email": ["john.doe@example.com"],
    "Doctor": ["Jane Smith, M.D."],
    "SSN": [],
    "PhoneNo": [],
    "Accession": [],
    "Age": [],
    "Address": []
  }
}


📂 Project Structure:


phi_deid_service/
│── __pycache__/                     # Python cache files
│── developer_inputs/                # 🔹 Synthetic PHI reports (6 samples for testing)
│   ├── 2.txt
│   ├── 3.txt
│   ├── 4.txt
│   ├── 5.txt
│   └── 6.txt
│── sample_inputs/                   # 🔹 Sample inputs (ready-to-test reports)
│── Protected-Health-Information-Extraction-NLP/  # Linked GitHub repo
│── app.py                           # Flask API entry point
│── deid_service.py                  # Core PHI DeIdentifier service
│── requirements.txt                 # Python dependencies
│── README.md                        # Project documentation
│── assignment.ipynb                 # Notebook (assignment work)
│── assignment.md                    # Assignment documentation
│── cmd_used.txt                     # Commands used during development
│── script-based-execution.py        # Script for running PHI de-id directly
│── test.ipynb                       # Jupyter notebook for testing


🔒 PHI Entities & Placeholders

| Entity Type           | Placeholder         |
|-----------------------|--------------------|
| Patient Name          | `[Deid: Name]`     |
| Address               | `[Deid: Address]`  |
| Email                 | `[Deid: Email]`    |
| Phone Number          | `[Deid: PhoneNo]`  |
| SSN                   | `[Deid: SSN]`      |
| MRN (Medical Record Number) | `[Deid: MRN]` |
| Accession Number      | `[Deid: Accession]`|
| Age                   | `[Deid: Age]`      |
| Any Date              | `[Deid: Date]`     |
| Doctor’s Name         | `[Deid: Doctor]`   |


📖 Notes
	•	Regex is used for structured PHI (MRN, SSN, Dates, Emails, etc.).
	•	spaCy NER is used to detect Names & Doctors in free text.
	•	The system is extensible — you can add new regex rules or swap in ML models for more accuracy.