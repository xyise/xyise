# Makefile

# Compiler
CC = gcc
CXX = g++

# Flags
CFLAGS = -Wall -Wextra -std=c11
CXXFLAGS = -Wall -Wextra -std=c++11

# Directories
OBJ_DIR = obj
BIN_DIR = bin

# Targets
TARGET = $(BIN_DIR)/main

# Source Files
C_SOURCES = c_library.c
CPP_SOURCES = main.cpp

# Object Files
C_OBJECTS = $(addprefix $(OBJ_DIR)/, $(C_SOURCES:.c=.o))
CPP_OBJECTS = $(addprefix $(OBJ_DIR)/, $(CPP_SOURCES:.cpp=.o))

# Rules
all: $(TARGET)

$(TARGET): $(C_OBJECTS) $(CPP_OBJECTS)
	mkdir -p $(BIN_DIR)
	$(CXX) -o $@ $^
$(OBJ_DIR)/%.o: %.c
	mkdir -p $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(OBJ_DIR)/%.o: %.cpp
	mkdir -p $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(C_OBJECTS) $(CPP_OBJECTS) $(TARGET)

.PHONY: all clean
