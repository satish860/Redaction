# GLiNER PDF Redaction Tool

This application provides a user-friendly interface for redacting sensitive information from PDF files using GLiNER for entity recognition.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/gliner_pdf_redaction.git
   cd gliner_pdf_redaction
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

Run the following command from the project root:

```
python src/main.py
```

## Usage

1. Click "Select PDF" to choose a PDF file for redaction.
2. Click "Redact PDF" to start the redaction process.
3. Choose where to save the redacted PDF file.
4. Wait for the process to complete.

## Note

This application uses GLiNER for entity recognition. The first time you run the application, it will download the pre-trained model, which may take a few moments.
