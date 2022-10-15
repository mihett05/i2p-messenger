const { getIpcRenderer, ipcOnce } = window.electronApi;

/*
import { Store } from 'tauri-plugin-store-api';
const store = new Store('.settings.dat');
await store.set('some-key', { value: 5 });
const val = await store.get('some-key');
assert(val, { value: 5 });
*/

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
