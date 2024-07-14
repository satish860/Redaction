import sys
from PyQt6.QtWidgets import QApplication
from src.pdf_redaction_app import PDFRedactionApp

def main():
    app = QApplication(sys.argv)
    ex = PDFRedactionApp()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()