const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronApi', {
  getIpcRenderer: () => ipcRenderer,
  ipcOnce: (channel, cb) => ipcRenderer.once(channel, cb),
});
