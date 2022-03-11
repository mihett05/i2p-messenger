const { getIpcRenderer, ipcOnce } = window.electronApi;

const Storage = {
  getItem: (key: string): string | null => {
    return getIpcRenderer().sendSync('storage-get', key);
  },
  setItem: (key: string, value: string) => {
    getIpcRenderer().send('storage-set', key, value);
  },
  removeItem: (key: string) => {
    getIpcRenderer().send('storage-remove', key);
  },
};

export default Storage;
