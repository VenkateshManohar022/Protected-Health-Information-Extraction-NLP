# PHI De-Identification Service

## Objective
Build a **PHI De-Identification Service** using **Python** and **Flask**.

The service will expose a **POST API endpoint** that accepts a patient’s medical report text and returns:

1. **De-identified report text** with placeholders for sensitive information.
2. **A list of detected and de-identified entities** (e.g., names, dates, addresses).

---

## PHI Entities to De-identify
The service should detect and replace the following with placeholders in the format **`[Deid: TYPE]`**:

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

---

## API Specification

### Endpoint

POST /deid


### Request Body (JSON)
```json
{
  "report_text": "Patient John Doe visited on 12-Jan-2020..."
} 
```

Response Body (JSON)
```json
{
  "deid_report": "Patient [Deid: Name] visited on [Deid: Date]...",
  "deid_entities": {
    "Name": ["John Doe"],
    "Date": ["12-Jan-2020"]
  }
}
```
## Implementation Details
- Use **Python 3.8+** and **Flask**.
- You may use **regex**, **NLP libraries** (e.g., spaCy, Stanza), or a combination.
- No database is required — process input text on the fly.
- Code should be **modular** and **readable**.
- The API should always return JSON.
- Handle multiple occurrences and edge cases.

---

## Submission Format
Submit a `.zip` file containing:
1. **Source code**
2. `requirements.txt` — list of dependencies
3. `README.md` — containing:
   - Steps to create a virtual environment
   - Steps to install dependencies
   - Steps to run the Flask app
   - Example request/response