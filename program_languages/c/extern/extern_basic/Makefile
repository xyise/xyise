OBJ_DIR := obj
BIN_DIR := bin

all: $(BIN_DIR)/main

$(BIN_DIR)/main: $(OBJ_DIR)/main.o $(OBJ_DIR)/extern.o
	mkdir -p $(BIN_DIR)
	gcc -o $@ $^

$(OBJ_DIR)/main.o: main.c
	mkdir -p $(OBJ_DIR)
	gcc -c -o $@ $<

$(OBJ_DIR)/extern.o: extern.c
	mkdir -p $(OBJ_DIR)
	gcc -c -o $@ $<

clean:
	rm -f $(OBJ_DIR)/*.o $(BIN_DIR)/main
