#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use std::sync::Mutex;

use tauri::Manager;
use tauri_plugin_store;

mod commands;
mod connection;

use connection::Connection;

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_store::PluginBuilder::default().build())
        .setup(|app| {
            let app_handle = app.handle();
            tauri::async_runtime::spawn(async move {
                let mut conn = Connection::connect("127.0.0.1:8080").await;
                app_handle.manage(Mutex::new(conn));
            });
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            commands::send_request
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
