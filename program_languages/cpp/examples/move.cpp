#include <memory>
#include <iostream>

class A
{
protected:
    std::shared_ptr<int> ptr;

public:
    A(std::shared_ptr<int> p) : ptr(std::move(p)) {}
    virtual void print()
    {
        std::cout << "A::print() " << *ptr << std::endl;
    }
};

class B : A
{

    public:
    B() : A(std::move(create_ptr())) {}
    void print() override
    {
        std::cout << "B::print() " << *ptr << std::endl;
    }
    private:
    static std::shared_ptr<int> create_ptr()
    {
        return std::make_shared<int>(42);
    }
};

int main()
{
    B b;
    b.print();

    B b1{b};
    b1.print();
    b.print();

    B b2{std::move(b)};
    b2.print();

    b.print();
    return 0;
}