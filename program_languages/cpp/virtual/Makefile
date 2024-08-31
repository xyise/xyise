CXX = g++
CXXFLAGS = -std=c++17

SRCS = main.cc
OBJS = $(addprefix obj/,$(SRCS:.cc=.o))
EXEC = obj/main

.PHONY: all clean

all: $(EXEC)

$(EXEC): $(OBJS)
	$(CXX) $(CXXFLAGS) $(OBJS) -o $(EXEC)

obj/%.o: %.cc | obj
	$(CXX) $(CXXFLAGS) -c $< -o $@

obj:
	mkdir -p obj

clean:
	rm -rf obj