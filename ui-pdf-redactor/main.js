const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadFile('index.html');
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

ipcMain.on('start-redaction', (event, args) => {
    const outputPath = path.join(path.dirname(args.inputPath), 'redacted_' + path.basename(args.inputPath));
    
    const pythonProcess = spawn('python', [
        'redactor.py',
        args.inputPath,
        outputPath,
        '--labels',
        ...args.labels
    ]);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python script output: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python script error: ${data}`);
        event.reply('redaction-error', data.toString());
    });

    pythonProcess.on('close', (code) => {
        if (code === 0) {
            event.reply('redaction-complete', outputPath);
        } else {
            event.reply('redaction-error', `Process exited with code ${code}`);
        }
    });
});