# Makefile for Eigen project

# Compiler and flags
CXX = g++
CXXFLAGS = -I$(HOME)/local/include -I$(HOME)/local/eigen-3.2.10 -std=c++11

# Directories
LIBS = -L$(HOME)/local/lib -lboost_system
SRC_DIR = .
OBJ_DIR = obj
BIN_DIR = bin

# Create a list of source files
SOURCES = $(wildcard $(SRC_DIR)/example_*.cpp)

# Create a list of object files
OBJECTS = $(patsubst $(SRC_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(SOURCES))

# Create a list of executables
EXECUTABLES = $(patsubst $(SRC_DIR)/%.cpp, $(BIN_DIR)/%, $(SOURCES))

# Default target
all: $(EXECUTABLES)

# Rule to create object files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Rule to create executables
$(BIN_DIR)/%: $(OBJ_DIR)/%.o
	@mkdir -p $(BIN_DIR)
	$(CXX) $(CXXFLAGS) $< -o $@ $(LIBS)

# Clean up
clean:
	rm -rf $(OBJ_DIR) $(BIN_DIR)

.PHONY: all clean


