# Assuming you have the PHIDeidentifier class in a file named deid_service.py
from deid_service import PHIDeidentifier
import os

# Create an instance of the deidentifier
deidentifier = PHIDeidentifier()

# Define the path to your input file
# Replace 'record_2.txt' with your file name if it's different
file_path = './developer_inputs/2.txt'
# file_path = './sample_inputs/record_2.txt'

# Check if the file exists
if not os.path.exists(file_path):
    print(f"Error: The file '{file_path}' was not found.")
else:
    # Load the text from the file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            report_text = f.read()

        # De-identify the loaded text
        deid_report, deid_entities = deidentifier.deidentify(report_text)

        # Print the results
        print("Original Report:")
        print("----------------")
        print(report_text)
        print("\n" + "="*50 + "\n")
        print("De-identified Report:")
        print("--------------------")
        print(deid_report)
        print("\n" + "="*50 + "\n")
        print("De-identified Entities:")
        print("-----------------------")
        for entity_type, entities in deid_entities.items():
            if entities:
                print(f"{entity_type}: {', '.join(entities)}")

    except Exception as e:
        print(f"An error occurred during de-identification: {e}")