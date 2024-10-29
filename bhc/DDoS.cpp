#include <iostream>
#include <cstring>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <thread>
#include <chrono>

#pragma comment (lib, "Ws2_32.lib")

int main() {
    WSADATA wsaData;
    SOCKET sock;
    struct sockaddr_in target;
    char buffer[512];  // Tamanho menor e mais razoável

    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "WSAStartup falhou" << std::endl;
        return 1;
    }

    if ((sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == INVALID_SOCKET) {
        std::cerr << "socket() falhou" << std::endl;
        WSACleanup();
        return 1;
    }

    std::string ipAddress;
    int porta;

    std::cout << "Digite o IP do servidor de teste: ";
    std::cin >> ipAddress;
    std::cout << "Digite a porta: ";
    std::cin >> porta;

    target.sin_family = AF_INET;
    target.sin_addr.s_addr = inet_addr(ipAddress.c_str());
    target.sin_port = htons(porta);

    // Dados de teste identificáveis
    const char* testData = "TESTE-REDE-123";
    strncpy(buffer, testData, sizeof(buffer));

    // Envio controlado com delay
    int packetSize = strlen(testData);
    int numPacotes = 10; // Número limitado de pacotes

    std::cout << "Iniciando teste de rede..." << std::endl;

    for (int i = 0; i < numPacotes; i++) {
        int sendResult = sendto(sock, buffer, packetSize, 0, (struct sockaddr*)&target, sizeof(target));
        if (sendResult == SOCKET_ERROR) {
            std::cerr << "sendto() falhou" << std::endl;
            break;
        }
        std::cout << "Pacote " << (i + 1) << "/" << numPacotes << " enviado" << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(100)); // Delay entre pacotes
    }

    closesocket(sock);
    WSACleanup();

    std::cout << "Teste de rede concluído" << std::endl;
    return 0;
}