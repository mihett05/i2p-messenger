use std::str;

use tauri::Manager;
use tokio::io::{AsyncReadExt};
use tokio::net::{TcpStream, ToSocketAddrs};


#[derive(Clone, serde::Serialize)]
pub struct ServerMessage {
    pub message: String,
}

pub struct Connection {
    pub stream: TcpStream,
}

impl Connection {
    fn from(stream: TcpStream) -> Connection {
        Connection { stream, }
    }

    pub async fn connect<A: ToSocketAddrs>(addr: A) -> Connection {
        let stream = TcpStream::connect(addr).await.expect("Failed to negotiate connection: {}");
        Connection::from(stream)
    }

    pub async fn run(&mut self, app: &mut tauri::App) {
        let mut buffer = [0 as u8; 8192];
        loop {
            self.stream.read_exact(&mut buffer).await;
            let text = String::from(str::from_utf8(&buffer).expect("Failed to decode utf-8: {}"));
            app.emit_all("server_message", ServerMessage { message: text });
        }
    }
}
