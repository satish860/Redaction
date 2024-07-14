from setuptools import setup, find_packages

setup(
    name="gliner_pdf_redaction",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.5.0",
        "gliner",
        "pdfplumber==0.9.0",
        "PyMuPDF==1.22.3",
        "python-docx==0.8.11",
    ],
    entry_points={
        "console_scripts": [
            "gliner_pdf_redaction=src.main:main",
        ],
    },
)
