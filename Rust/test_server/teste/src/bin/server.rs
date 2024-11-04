use std::collections::HashMap;
use std::fs::{self, File};
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::{Arc, Mutex};
use std::thread;
use chrono::Local;

const HOST: &str = "127.0.0.1";
const PORT: u16 = 12346;
const DIRECTORY: &str = "files";

type ClientMap = Arc<Mutex<HashMap<String, TcpStream>>>;
type MessageList = Arc<Mutex<Vec<String>>>;

fn handle_client(mut stream: TcpStream, clients: ClientMap, messages: MessageList) {
    let addr = stream.peer_addr().unwrap().to_string();
    println!("Cliente conectado: {}", addr);

    let _ = stream.write(b"Conectado ao servidor!\n");

    clients.lock().unwrap().insert(addr.clone(), stream.try_clone().unwrap());

    let mut buffer = [0; 1024];
    while let Ok(size) = stream.read(&mut buffer) {
        if size == 0 { break; }

        let data = String::from_utf8_lossy(&buffer[..size]).to_string();
        let parts: Vec<&str> = data.split('|').collect();
        let command = parts[0].to_uppercase();

        match command.as_str() {
            "UPLOAD" => {
                if parts.len() < 3 {
                    let _ = stream.write(b"Erro: Formato de comando UPLOAD incorreto.\n");
                    continue;
                }
                let filename = parts[1];
                let content = parts[2];
                let filepath = format!("{}/{}", DIRECTORY, filename);

                if let Err(_) = fs::write(&filepath, content) {
                    let _ = stream.write(format!("Erro ao enviar o arquivo {}.\n", filename).as_bytes());
                } else {
                    let _ = stream.write(format!("Arquivo {} enviado com sucesso!\n", filename).as_bytes());
                }
            },
            "DOWNLOAD" => {
                if parts.len() < 2 {
                    let _ = stream.write(b"Erro: Formato de comando DOWNLOAD incorreto.\n");
                    continue;
                }
                let filename = parts[1];
                let filepath = format!("{}/{}", DIRECTORY, filename);

                match fs::read_to_string(&filepath) {
                    Ok(content) => {
                        let _ = stream.write(format!("DOWNLOAD|{}|{}\n", filename, content).as_bytes());
                    },
                    Err(_) => {
                        let _ = stream.write(format!("Erro: Arquivo {} não encontrado.\n", filename).as_bytes());
                    }
                }
            },
            "LIST" => {
                match fs::read_dir(DIRECTORY) {
                    Ok(entries) => {
                        let files: Vec<String> = entries
                            .filter_map(Result::ok)
                            .filter_map(|entry| entry.file_name().into_string().ok())
                            .collect();
                        let file_list = if files.is_empty() {
                            "Nenhum arquivo disponível".to_string()
                        } else {
                            files.join(", ")
                        };
                        let _ = stream.write(format!("Arquivos disponíveis: {}\n", file_list).as_bytes());
                    },
                    Err(_) => {
                        let _ = stream.write(b"Erro ao listar arquivos.\n");
                    }
                }
            },
            "MESSAGE" => {
                if parts.len() < 3 {
                    let _ = stream.write(b"Erro: Formato de comando MESSAGE incorreto.\n");
                    continue;
                }
                let recipient_addr = parts[1].to_string();
                let message = parts[2];
                let time = Local::now().format("%H:%M:%S").to_string();

                if let Some(mut recipient) = clients.lock().unwrap().get(&recipient_addr) {
                    let msg_with_time = format!("MESSAGE from {} at {}: {}", addr, time, message);
                    let _ = recipient.write(msg_with_time.as_bytes());
                    let _ = stream.write(format!("Mensagem enviada para {}\n", recipient_addr).as_bytes());

                    messages.lock().unwrap().push(msg_with_time);
                } else {
                    let _ = stream.write(format!("Erro: Nó {} não encontrado.\n", recipient_addr).as_bytes());
                }
            },
            "LIST MESSAGES" => {
                let messages = messages.lock().unwrap();
                let message_list = if messages.is_empty() {
                    "Nenhuma mensagem disponível.".to_string()
                } else {
                    messages.join("\n")
                };
                let _ = stream.write(format!("Mensagens:\n{}\n", message_list).as_bytes());
            },
            _ => {
                let _ = stream.write(b"Comando inv\xE1lido!\n");
            }
        }
    }

    clients.lock().unwrap().remove(&addr);
    println!("Cliente desconectado: {}", addr);
}

fn main() {
    if !fs::metadata(DIRECTORY).is_ok() {
        let _ = fs::create_dir(DIRECTORY);
    }

    let listener = TcpListener::bind((HOST, PORT)).expect("Não foi possível iniciar o servidor");
    let clients: ClientMap = Arc::new(Mutex::new(HashMap::new()));
    let messages: MessageList = Arc::new(Mutex::new(Vec::new()));

    println!("Servidor iniciado em {}:{}", HOST, PORT);

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                let clients = Arc::clone(&clients);
                let messages = Arc::clone(&messages);
                thread::spawn(move || handle_client(stream, clients, messages));
            }
            Err(e) => {
                eprintln!("Erro ao aceitar conexão: {}", e);
            }
        }
    }
}


