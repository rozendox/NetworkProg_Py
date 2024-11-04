package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

const (
	HOST      = "127.0.0.1"
	PORT      = "12346"
	DIRECTORY = "files"
)

func clientProgram() {
	conn, err := net.Dial("tcp", HOST+":"+PORT)
	if err != nil {
		fmt.Println("Erro ao conectar ao servidor:", err)
		return
	}
	defer conn.Close()

	message, _ := bufio.NewReader(conn).ReadString('\n')
	fmt.Print(message)

	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Print("Digite o comando (UPLOAD, DOWNLOAD, LIST, MESSAGE, LIST MESSAGES): ")
		command, _ := reader.ReadString('\n')
		command = strings.TrimSpace(command)

		var message string
		switch strings.ToUpper(command) {
		case "UPLOAD":
			fmt.Print("Nome do arquivo: ")
			filename, _ := reader.ReadString('\n')
			filename = strings.TrimSpace(filename)
			fmt.Print("Conteúdo do arquivo: ")
			fileContent, _ := reader.ReadString('\n')
			message = fmt.Sprintf("UPLOAD|%s|%s", filename, fileContent)
		case "DOWNLOAD":
			fmt.Print("Nome do arquivo: ")
			filename, _ := reader.ReadString('\n')
			message = fmt.Sprintf("DOWNLOAD|%s", filename)
		case "LIST":
			message = "LIST"
		case "MESSAGE":
			fmt.Print("Digite o IP e porta do nó destinatário (ex: 127.0.0.1:63324): ")
			recipientAddr, _ := reader.ReadString('\n')
			fmt.Print("Digite a mensagem: ")
			msgContent, _ := reader.ReadString('\n')
			message = fmt.Sprintf("MESSAGE|%s|%s", strings.TrimSpace(recipientAddr), strings.TrimSpace(msgContent))
		case "LIST MESSAGES":
			message = "LIST MESSAGES"
		default:
			fmt.Println("Comando inválido!")
			continue
		}

		conn.Write([]byte(message + "\n"))
		response, _ := bufio.NewReader(conn).ReadString('\n')
		fmt.Print("Resposta do servidor: ", response)
	}
}

func main() {
	clientProgram()
}
