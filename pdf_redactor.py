import sys
import subprocess
import importlib.util

def install_and_import(package, import_name=None):
    if import_name is None:
        import_name = package
    try:
        importlib.import_module(import_name)
    except ImportError:
        print(f"{package} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[import_name] = importlib.import_module(import_name)

# Install and import required packages
install_and_import('argparse')
install_and_import('pdfplumber')
install_and_import('PyMuPDF', 'fitz')
install_and_import('gliner')

# Now we can use these modules
import argparse
import pdfplumber
import fitz  # PyMuPDF
from gliner import GLiNER

def split_into_chunks(text, chunk_size=50):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i+chunk_size])

def redact_pdf(input_pdf, output_pdf, redaction_dict):
    doc = fitz.open(input_pdf)
    
    for page in doc:
        for entity, label in redaction_dict.items():
            areas = page.search_for(entity)
            for rect in areas:
                page.add_redact_annot(rect, fill=(0, 0, 0))  # Black fill
        
        page.apply_redactions()
    
    doc.save(output_pdf)
    doc.close()

def main():
    parser = argparse.ArgumentParser(description="Redact sensitive information from a PDF file.")
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    parser.add_argument("output_pdf", help="Path to save the redacted PDF file")
    parser.add_argument("--labels", nargs="+", default=[
        "Identifier",         
    "Location",          
    "Person",               
    "Organization",         
    "Date",  
    "Name", 
    ], help="List of labels to identify for redaction")
    
    args = parser.parse_args()

    # Initialize GLiNER with the base model
    model = GLiNER.from_pretrained("urchade/gliner_mediumv2.1")

    redaction_dict = {}
    with pdfplumber.open(args.input_pdf) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            print(f"Processing Page {page_number}")
            page_text = page.extract_text()
            
            for chunk_number, chunk in enumerate(split_into_chunks(page_text), start=1):
                print(f"  Processing Chunk {chunk_number}")
                
                # Perform entity prediction
                entities = model.predict_entities(chunk, args.labels, threshold=0.5)
                
                # Add entities to redaction dictionary
                for entity in entities:
                    entity_text = entity["text"]
                    label = entity['label']
                    redaction_dict[entity_text] = label

    # Redact the PDF
    redact_pdf(args.input_pdf, args.output_pdf, redaction_dict)
    print(f"Redacted PDF has been saved as '{args.output_pdf}'")
    print(f"\nSummary:")
    print(f"Total entities redacted: {len(redaction_dict)}")
    print("Redaction completed successfully.")

if __name__ == "__main__":
    main()