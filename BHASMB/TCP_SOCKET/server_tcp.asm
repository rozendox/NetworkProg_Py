section .data
    msg db 'Mensagem recebida com sucesso', 0xA ; Mensagem de resposta
    msg_len equ $ - msg                         ; Tamanho da mensagem
    ip_address db 127, 0, 0, 1                  ; Endereço IP (localhost)
    port dw 12345                               ; Porta do servidor

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

    mov edx, esp
    mov dword [edx], 0x00002                    ; família AF_INET
    mov word [edx+2], port                      ; define porta
    mov dword [edx+4], ip_address               ; endereço IP (localhost)


    mov eax, 0x66                               ; syscall: socketcall
    mov ebx, 2                                  ; syscall: bind
    push 16                                     ; tamanho da estrutura sockaddr_in
    push edx                                    ; endereço de sockaddr_in
    push dword [sock_fd]                        ; sock_fd
    mov ecx, esp                                ; argumento da syscall
    int 0x80                                    ; chama o sistema


    mov eax, 0x66                               ; syscall: socketcall
    mov ebx, 4                                  ; syscall: listen
    push 0x10                                   ; backlog
    push dword [sock_fd]                        ; sock_fd
    mov ecx, esp                                ; argumento da syscall
    int 0x80                                    ; chama o sistema

    mov eax, 0x66                               ; syscall: socketcall
    mov ebx, 5                                  ; syscall: accept
    push 0                                      ; NULL para sockaddr
    push 0                                      ; NULL para tamanho
    push dword [sock_fd]                        ; sock_fd
    mov ecx, esp                                ; argumento da syscall
    int 0x80                                    ; chama o sistema
    mov [sock_fd], eax                          ; salva novo sock_fd para comunicação

    mov eax, 0x66                               ; syscall: socketcall
    mov ebx, 10                                 ; syscall: recv
    push 0x100                                  ; tamanho máximo
    push esp                                    ; buffer para receber a mensagem
    push dword [sock_fd]                        ; sock_fd
    mov ecx, esp                                ; argumento da syscall
    int 0x80                                    ; chama o sistema


    mov eax, 0x66                               ; syscall: socketcall
    mov ebx, 9                                  ; syscall: send
    push msg_len                                ; comprimento da mensagem
    push msg                                    ; ponteiro para a mensagem
    push dword [sock_fd]                        ; sock_fd
    mov ecx, esp                                ; argumento da syscall
    int 0x80                                    ; chama o sistema


    mov eax, 6                                  ; syscall: close
    mov ebx, [sock_fd]                          ; sock_fd
    int 0x80                                    ; chama o sistema


    mov eax, 1                                  ; syscall: exit
    xor ebx, ebx                                ; código de saída 0
    int 0x80
