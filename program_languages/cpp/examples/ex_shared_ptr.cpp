#include <iostream>
#include <memory>
#include <string>


class Base {
public:
    virtual void print() const {
        std::cout << "This is the base class." << std::endl;
    }
};

class Derived : public Base {
private:
    std::string name;
public:
    Derived(std::string name) : name(name) {}
    void print() const override {
        std::cout << "This is the derived class: " << name << "." << std::endl;
    }
};

int main() {
    std::shared_ptr<Base> basePtr = std::make_shared<Derived>("class 1");
    basePtr = std::make_shared<Derived>("class 2");
    basePtr->print();
    return 0;
}