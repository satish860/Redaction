import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QPushButton, QVBoxLayout, 
                             QFileDialog, QLabel, QProgressBar)
from PyQt6.QtCore import Qt
from gliner import GLiNER
from src.redaction_worker import RedactionWorker

class PDFRedactionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.model = GLiNER.from_pretrained("urchade/gliner_mediumv2.1")
        self.labels = ["Identifier", "Location", "Person", "Organization", "Date", "Name"]

    def initUI(self):
        self.setWindowTitle('PDF Redaction Tool')
        self.setGeometry(300, 300, 400, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.fileLabel = QLabel('No file selected', self)
        layout.addWidget(self.fileLabel)

        fileButton = QPushButton('Select PDF', self)
        fileButton.clicked.connect(self.selectFile)
        layout.addWidget(fileButton)

        self.redactButton = QPushButton('Redact PDF', self)
        self.redactButton.clicked.connect(self.redactPDF)
        self.redactButton.setEnabled(False)
        layout.addWidget(self.redactButton)

        self.progressBar = QProgressBar(self)
        self.progressBar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.progressBar)

        self.statusLabel = QLabel('', self)
        layout.addWidget(self.statusLabel)

    def selectFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)")
        if fileName:
            self.fileLabel.setText(f"Selected file: {os.path.basename(fileName)}")
            self.selectedFile = fileName
            self.redactButton.setEnabled(True)

    def redactPDF(self):
        if hasattr(self, 'selectedFile'):
            outputFile, _ = QFileDialog.getSaveFileName(self, "Save Redacted PDF", "", "PDF Files (*.pdf)")
            if outputFile:
                self.redactButton.setEnabled(False)
                self.statusLabel.setText("Redaction in progress...")
                self.worker = RedactionWorker(self.selectedFile, outputFile, self.model, self.labels)
                self.worker.progress.connect(self.updateProgress)
                self.worker.finished.connect(self.onRedactionFinished)
                self.worker.start()

    def updateProgress(self, value):
        self.progressBar.setValue(value)

    def onRedactionFinished(self):
        self.progressBar.setValue(100)
        self.redactButton.setEnabled(True)
        self.fileLabel.setText('No file selected')
        self.statusLabel.setText("Redaction completed successfully!")
