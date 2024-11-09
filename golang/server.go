package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
	"sync"
	"time"
)

const (
	HOST      = "127.0.0.1"
	PORT      = "12345"
	DIRECTORY = "files"
)

var (
	clients  = make(map[string]net.Conn)
	messages []string
	mu       sync.Mutex
)

// Função para lidar com cada cliente
func handleClient(conn net.Conn) {
	defer conn.Close()
	addr := conn.RemoteAddr().String()
	fmt.Println("Cliente conectado:", addr)

	clients[addr] = conn
	conn.Write([]byte("Conectado ao servidor!\n"))

	scanner := bufio.NewScanner(conn)
	for scanner.Scan() {
		data := scanner.Text()
		command := strings.Split(data, "|")[0]

		switch strings.ToUpper(command) {
		case "UPLOAD":
			handleUpload(conn, data)
		case "DOWNLOAD":
			handleDownload(conn, data)
		case "LIST":
			handleList(conn)
		case "MESSAGE":
			handleMessage(conn, data)
		case "LIST MESSAGES":
			handleListMessages(conn)
		default:
			conn.Write([]byte("Comando inválido!\n"))
		}
	}

	mu.Lock()
	delete(clients, addr)
	mu.Unlock()
	fmt.Println("Cliente desconectado:", addr)
}

// Função para gerenciar uploads
func handleUpload(conn net.Conn, data string) {
	parts := strings.Split(data, "|")
	if len(parts) < 3 {
		conn.Write([]byte("Erro: Formato de comando UPLOAD incorreto.\n"))
		return
	}

	filename, fileContent := parts[1], parts[2]
	err := os.WriteFile(DIRECTORY+"/"+filename, []byte(fileContent), 0644)
	if err != nil {
		conn.Write([]byte("Erro ao enviar o arquivo " + filename + ".\n"))
		return
	}
	conn.Write([]byte("Arquivo " + filename + " enviado com sucesso!\n"))
}

// Função para gerenciar downloads
func handleDownload(conn net.Conn, data string) {
	parts := strings.Split(data, "|")
	if len(parts) < 2 {
		conn.Write([]byte("Erro: Formato de comando DOWNLOAD incorreto.\n"))
		return
	}

	filename := parts[1]
	fileContent, err := os.ReadFile(DIRECTORY + "/" + filename)
	if err != nil {
		conn.Write([]byte("Erro: Arquivo " + filename + " não encontrado.\n"))
		return
	}
	conn.Write([]byte("DOWNLOAD|" + filename + "|" + string(fileContent) + "\n"))
}

// Função para listar arquivos
func handleList(conn net.Conn) {
	files, err := os.ReadDir(DIRECTORY)
	if err != nil {
		conn.Write([]byte("Erro ao listar arquivos.\n"))
		return
	}

	if len(files) == 0 {
		conn.Write([]byte("Nenhum arquivo disponível\n"))
	} else {
		var fileList []string
		for _, file := range files {
			fileList = append(fileList, file.Name())
		}
		conn.Write([]byte("Arquivos disponíveis: " + strings.Join(fileList, ", ") + "\n"))
	}
}

// Função para enviar mensagens entre clientes
func handleMessage(conn net.Conn, data string) {
	parts := strings.Split(data, "|")
	if len(parts) < 3 {
		conn.Write([]byte("Erro: Formato de comando MESSAGE incorreto.\n"))
		return
	}

	recipientAddr, msgContent := parts[1], parts[2]
	mu.Lock()
	recipientConn, ok := clients[recipientAddr]
	mu.Unlock()

	if !ok {
		conn.Write([]byte("Erro: Nó " + recipientAddr + " não encontrado.\n"))
		return
	}

	currentTime := time.Now().Format("15:04:05")
	msgWithTime := fmt.Sprintf("MESSAGE from %s at %s: %s", conn.RemoteAddr().String(), currentTime, msgContent)
	recipientConn.Write([]byte(msgWithTime + "\n"))

	// Armazenando a mensagem
	mu.Lock()
	messages = append(messages, fmt.Sprintf("From %s to %s at %s: %s", conn.RemoteAddr().String(), recipientAddr, currentTime, msgContent))
	mu.Unlock()
	conn.Write([]byte("Mensagem enviada para " + recipientAddr + "\n"))
}

// Função para listar todas as mensagens
func handleListMessages(conn net.Conn) {
	mu.Lock()
	defer mu.Unlock()
	if len(messages) == 0 {
		conn.Write([]byte("Nenhuma mensagem disponível.\n"))
		return
	}
	conn.Write([]byte("Mensagens:\n" + strings.Join(messages, "\n") + "\n"))
}

// Inicia o servidor
func startServer() {
	ln, err := net.Listen("tcp", HOST+":"+PORT)
	if err != nil {
		fmt.Println("Erro ao iniciar o servidor:", err)
		return
	}
	defer ln.Close()

	fmt.Printf("Servidor iniciado em %s:%s...\n", HOST, PORT)
	for {
		conn, err := ln.Accept()
		if err != nil {
			fmt.Println("Erro ao aceitar conexão:", err)
			continue
		}
		go handleClient(conn)
	}
}

func main() {
	// Cria o diretório de arquivos, se não existir
	if _, err := os.Stat(DIRECTORY); os.IsNotExist(err) {
		os.Mkdir(DIRECTORY, 0755)
	}
	startServer()
}
