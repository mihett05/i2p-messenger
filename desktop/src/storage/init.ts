import Database from 'tauri-plugin-sql-api';

const createTables = async (db: Database) => {
  await db.execute(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username VARCHAR(512) NOT NULL,
    server_hash VARCHAR(32) NOT NULL
  )
  `);
  await db.execute(`
  CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
  )
  `);
};
