import re
import spacy

class PHIDeidentifier:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_lg")
        except OSError:
            print("Downloading spaCy model 'en_core_web_lg'...")
            from spacy.cli import download
            download("en_core_web_lg")
            self.nlp = spacy.load("en_core_web_lg")

        self.patterns = {
            "SSN": r'\b\d{3}-\d{2}-\d{4}\b',
            "MRN": r'MRN:\s*(\b\d{5,10})\b',
            "Accession": r'Accession\s*(?:Number|No|#)\s*[:.]?\s*([\w\-\.]+)',
            "Email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}',
            "PhoneNo": r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})|(\b\d{3}[-.\s]\d{2,4}[-.\s]\d{2,4}\b)',
            "Date": r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{1,2}-[A-Za-z]{3}-\d{4}\b',
            "Address": r'\b(?:Room|Unit|Address)[:\-]?\s*[\w\d\s,#\-\.]+\b',
            "Doctor": r'(?:Doctor[:\s]|Dr\.|attending physician was)\s*([A-Z][a-z]+\s[A-Z][a-z]+(?:,\s*M\.D\.)?)',
        }
        
        # New, more specific age pattern to be handled by regex
        self.age_pattern = r'Age\s*[:\s]*(\d{1,3})'

        self.placeholders = {
            "Name": "[Deid: Name]",
            "Date": "[Deid: Date]",
            "Email": "[Deid: Email]",
            "PhoneNo": "[Deid: PhoneNo]",
            "SSN": "[Deid: SSN]",
            "MRN": "[Deid: MRN]",
            "Accession": "[Deid: Accession]",
            "Age": "[Deid: Age]",
            "Address": "[Deid: Address]",
            "Doctor": "[Deid: Doctor]"
        }

    def deidentify(self, text: str):
        deid_entities = {key: [] for key in self.placeholders.keys()}
        replacements = []
        
        # Step 1: Pre-process with highly specific regex for Age
        age_match = re.search(self.age_pattern, text, flags=re.IGNORECASE)
        if age_match:
            age_text = age_match.group(1)
            replacements.append({
                "text": age_match.group(0),
                "start": age_match.start(),
                "end": age_match.end(),
                "type": "Age"
            })
            deid_entities["Age"].append(age_text)

        # Step 2: Apply other structured regex patterns
        for entity_type, pattern in self.patterns.items():
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                is_overlap = any(match.start() < r['end'] and match.end() > r['start'] for r in replacements)
                if not is_overlap:
                    matched_text = match.group(1) if match.lastindex else match.group(0)
                    replacements.append({
                        "text": match.group(0),
                        "start": match.start(),
                        "end": match.end(),
                        "type": entity_type
                    })
                    deid_entities[entity_type].append(matched_text)

        # Step 3: Use spaCy NER for PERSON entities, avoiding overlaps
        doc = self.nlp(text)
        for ent in doc.ents:
            is_overlap = any(ent.start_char < r['end'] and ent.end_char > r['start'] for r in replacements)
            
            if not is_overlap:
                if ent.label_ == "PERSON":
                    context_start = max(0, ent.start_char - 25)
                    context_end = min(len(text), ent.end_char + 25)
                    context = text[context_start:context_end]
                    
                    is_doctor = bool(re.search(r'\b(Dr\.|M\.D\.|physician|attending)\b', context, re.IGNORECASE))
                    entity_type = "Doctor" if is_doctor else "Name"
                    
                    replacements.append({
                        "text": ent.text,
                        "start": ent.start_char,
                        "end": ent.end_char,
                        "type": entity_type
                    })
                    deid_entities[entity_type].append(ent.text)

        # Step 4: Apply replacements in reverse order
        replacements.sort(key=lambda x: x['start'], reverse=True)
        deid_report = text
        for r in replacements:
            deid_report = deid_report[:r['start']] + self.placeholders[r['type']] + deid_report[r['end']:]

        for k in deid_entities:
            deid_entities[k] = list(set(deid_entities[k]))

        return deid_report, deid_entities