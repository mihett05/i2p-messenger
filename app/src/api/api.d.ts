import { IpcRenderer } from 'electron';

interface ElectronApi {
  getIpcRenderer: () => IpcRenderer;
  ipcOnce: (channel: string, cb: (...args: any[]) => any) => any;
}

// @ts-ignore
declare global {
  interface Window {
    electronApi: ElectronApi;
  }
}
