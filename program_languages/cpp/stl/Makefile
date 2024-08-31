# Makefile for compiling C++ files with separate main functions

# Compiler
CC := g++

# Compiler flags
CFLAGS := -Wall -Wextra -std=c++17 -g

# Directories
SRC_DIR := .
OBJ_DIR := obj
BIN_DIR := bin

# Source files
SRCS := $(wildcard $(SRC_DIR)/*.cpp)

# Object files
OBJS := $(patsubst $(SRC_DIR)/%.cpp,$(OBJ_DIR)/%.o,$(SRCS))

# Binary files
BINS := $(patsubst $(SRC_DIR)/%.cpp,$(BIN_DIR)/%,$(SRCS))

# Default target
all: $(BINS)

# Rule for creating object files 
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(@D)
	$(CC) $(CFLAGS) -c $< -o $@

# Rule for creating binary files
$(BIN_DIR)/%: $(OBJ_DIR)/%.o
	@mkdir -p $(@D)
	$(CC) $(CFLAGS) $< -o $@

# Clean target
clean:
	rm -rf $(OBJ_DIR) $(BIN_DIR)

.PHONY: all clean
