const { ipcRenderer } = require('electron');

document.getElementById('chooseFileBtn').addEventListener('click', () => {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', (e) => {
    const fileName = e.target.files[0] ? e.target.files[0].name : 'No file chosen';
    document.getElementById('fileNameDisplay').textContent = fileName;
});

document.getElementById('submitBtn').addEventListener('click', (e) => {
    e.preventDefault();
    
    const inputFile = document.getElementById('fileInput').files[0];
    const labels = document.getElementById('labelsInput').value.split('\n').filter(label => label.trim() !== '');
    const color = document.getElementById('colorInput').value;

    if (!inputFile) {
        alert('Please select a PDF file');
        return;
    }

    const statusElement = document.getElementById('status');
    statusElement.textContent = 'Processing...';

    ipcRenderer.send('start-redaction', {
        inputPath: inputFile.path,
        labels: labels,
        color: color
    });
});

ipcRenderer.on('redaction-complete', (event, outputPath) => {
    const statusElement = document.getElementById('status');
    statusElement.textContent = `Redaction complete! Saved to: ${outputPath}`;
});

ipcRenderer.on('redaction-error', (event, error) => {
    const statusElement = document.getElementById('status');
    statusElement.textContent = `Error: ${error}`;
});