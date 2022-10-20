// import { Store } from 'tauri-plugin-store-api';
//
// const store = new Store('.storage.dat');
// await store.set('some-key', { value: 5 });
// const val = await store.get('some-key');

import Database from 'tauri-plugin-sql-api';

// sqlite. The path is relative to `tauri::api::path::BaseDirectory::App`.
const db = await Database.load('sqlite:storage.db');
