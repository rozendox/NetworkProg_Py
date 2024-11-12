section .data
    ip_address db 127, 0, 0, 1                  ; Endereço IP do servidor (localhost)
    port dw 12345                               ; Porta do servidor
    msg db 'Olá, servidor!', 0xA                ; Mensagem para enviar
    msg_len equ $ - msg                         ; Tamanho da mensagem

section .bss
    sock_fd resd 1                              ; Descritor de arquivo do socket

section .text
    global _start

_start:

    mov eax, 0x66                               ; syscall: socketcall
    mov ebx, 1                                  ; syscall: socket
    push dword 6                                ; protocolo (TCP)
    push dword 1                                ; tipo SOCK_STREAM
    push dword 2                                ; domínio AF_INET
    mov ecx, esp                                ; argumento da syscall
    int 0x80                                    ; chama o sistema
    mov [sock_fd], eax                          ; salva sock_fd

    ; Configurar a estrutura de conexão (estrutura sockaddr_in)
    mov edx, esp
    mov dword [edx], 0x00002                    ; família AF_INET
    mov word [edx+2], port                      ; porta do servidor
    mov dword [edx+4], ip_address               ; endereço IP do servidor

    ; Conectar ao servidor
    mov eax, 0x66                               ; syscall: socketcall
    mov ebx, 3                                  ; syscall: connect
    push 16                                     ; tamanho da estrutura sockaddr_in
    push edx                                    ; endereço de sockaddr_in
    push dword [sock_fd]                        ; sock_fd
    mov ecx, esp                                ; argumento da syscall
    int 0x80                                    ; chama o sistema

    ; Enviar mensagem para o servidor
    mov eax, 0x66                               ; syscall: socketcall
    mov ebx, 9                                  ; syscall: send
    push msg_len                                ; comprimento da mensagem
    push msg                                    ; ponteiro para a mensagem
    push dword [sock_fd]                        ; sock_fd
    mov ecx, esp                                ; argumento da syscall
    int 0x80                                    ; chama o sistema

    ; Receber resposta do servidor
    mov eax, 0x66                               ; syscall: socketcall
    mov ebx, 10                                 ; syscall: recv
    push 0x100                                  ; tamanho máximo
    push esp                                    ; buffer para receber a resposta
    push dword [sock_fd]                        ; sock_fd
    mov ecx, esp                                ; argumento da syscall
    int 0x80                                    ; chama o sistema

    ; Fechar o socket
    mov eax, 6                                  ; syscall: close
    mov ebx, [sock_fd]                          ; sock_fd
    int 0x80                                    ; chama o sistema

    ; Terminar o programa
    mov eax, 1                                  ; syscall: exit
    xor ebx, ebx                                ; código de saída 0
    int 0x80
