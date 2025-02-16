import json
from fpdf import FPDF


def json_to_pdf(json_string):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    data = json.loads(json_string)
    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=1)

    return pdf


def convert_json_to_pdf(json_file_path, pdf_file_path):
    """
    Converts a JSON file to a PDF file.

    Args:
        json_file_path (str): Path to the JSON file.
        pdf_file_path (str): Path to save the generated PDF file.
    """
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
         print(f"Error: JSON file not found at '{json_file_path}'")
         return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_file_path}'")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=1)

    pdf.output(pdf_file_path)
    print(f"Successfully converted '{json_file_path}' to '{pdf_file_path}'")

if __name__ == "__main__":
    json_file = 'recipe_output.json'
    pdf_file = 'recipe_output.pdf'
    
    convert_json_to_pdf(json_file, pdf_file)