from PyQt6.QtCore import QThread, pyqtSignal
import pdfplumber
import fitz  # PyMuPDF

class RedactionWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, input_pdf, output_pdf, model, labels):
        super().__init__()
        self.input_pdf = input_pdf
        self.output_pdf = output_pdf
        self.model = model
        self.labels = labels

    def run(self):
        redaction_dict = {}
        with pdfplumber.open(self.input_pdf) as pdf:
            total_pages = len(pdf.pages)
            for page_number, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()
                
                for chunk_number, chunk in enumerate(self.split_into_chunks(page_text), start=1):
                    entities = self.model.predict_entities(chunk, self.labels, threshold=0.5)
                    
                    for entity in entities:
                        entity_text = entity["text"]
                        label = entity['label']
                        redaction_dict[entity_text] = label
                
                self.progress.emit(int((page_number / total_pages) * 50))

        self.redact_pdf(self.input_pdf, self.output_pdf, redaction_dict)
        self.finished.emit()

    def split_into_chunks(self, text, chunk_size=50):
        words = text.split()
        for i in range(0, len(words), chunk_size):
            yield ' '.join(words[i:i+chunk_size])

    def redact_pdf(self, input_pdf, output_pdf, redaction_dict):
        doc = fitz.open(input_pdf)
        
        for page_number, page in enumerate(doc, start=1):
            for entity, label in redaction_dict.items():
                areas = page.search_for(entity)
                for rect in areas:
                    page.add_redact_annot(rect, fill=(0, 0, 0))  # Black fill
            
            page.apply_redactions()
            self.progress.emit(50 + int((page_number / len(doc)) * 50))
        
        doc.save(output_pdf)
        doc.close()
