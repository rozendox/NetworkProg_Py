use std::io::{self, Write, Read};
use std::net::TcpStream;

const HOST: &str = "127.0.0.1";
const PORT: u16 = 12346;

fn main() -> io::Result<()> {
    let mut client = TcpStream::connect((HOST, PORT))?;
    let mut buffer = [0; 1024];

    client.read(&mut buffer)?;
    println!("{}", String::from_utf8_lossy(&buffer));

    loop {
        let mut command = String::new();
        println!("Digite o comando (UPLOAD, DOWNLOAD, LIST, MESSAGE, LIST MESSAGES): ");
        io::stdin().read_line(&mut command)?;
        let command = command.trim();

        let message = match command.to_uppercase().as_str() {
            "UPLOAD" => {
                let mut filename = String::new();
                let mut file_content = String::new();
                println!("Nome do arquivo: ");
                io::stdin().read_line(&mut filename)?;
                println!("Conteúdo do arquivo: ");
                io::stdin().read_line(&mut file_content)?;
                format!("UPLOAD|{}|{}", filename.trim(), file_content.trim())
            }
            "DOWNLOAD" => {
                let mut filename = String::new();
                println!("Nome do arquivo: ");
                io::stdin().read_line(&mut filename)?;
                format!("DOWNLOAD|{}", filename.trim())
            }
            "LIST" => "LIST".to_string(),
            "MESSAGE" => {
                let mut recipient = String::new();
                let mut msg_content = String::new();
                println!("Digite o IP e porta do nó destinatário (exemplo: '127.0.0.1:63324'): ");
                io::stdin().read_line(&mut recipient)?;
                println!("Digite a mensagem: ");
                io::stdin().read_line(&mut msg_content)?;
                format!("MESSAGE|{}|{}", recipient.trim(), msg_content.trim())
            }
            "LIST MESSAGES" => "LIST MESSAGES".to_string(),
            _ => {
                println!("Comando inválido!");
                continue;
            }
        };

        client.write(message.as_bytes())?;
        let response_size = client.read(&mut buffer)?;
        println!("Resposta do servidor: {}", String::from_utf8_lossy(&buffer[..response_size]));
    }
}
