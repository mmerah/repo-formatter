cmake_minimum_required(VERSION 3.10)
project(Project VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Include directories
include_directories(include)

# Add executable
add_executable(sample_app src/main.cpp src/utils/project/calculator.cpp)

# Print message
message(STATUS "Configuring Project for MyOrg")