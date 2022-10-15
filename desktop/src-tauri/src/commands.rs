use std::sync::Mutex;

use tauri;
use tokio::io::AsyncWriteExt;

use crate::connection::Connection;


#[tauri::command]
pub async fn send_request(data: String, connection: tauri::State<'_, Mutex<Connection>>) -> Result<(), ()> {
    connection.lock().unwrap().stream.write(data.as_bytes());
    Ok(())
}
