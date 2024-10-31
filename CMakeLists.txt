cmake_minimum_required(VERSION 3.29)
project(Network_Prog)

set(CMAKE_CXX_STANDARD 14)

add_executable(Network_Prog
        bhc/DDos/DDoS_2.cpp)

target_link_libraries(Network_Prog ws2_32)
