const { app, BrowserWindow } = require('electron');
const path = require('path');
const { createConnection } = require('./ipc');

const createWindow = () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  const client = createConnection('127.0.0.1', 8080);

  win.loadURL('http://localhost:3000');
  win.webContents.openDevTools();
};

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
