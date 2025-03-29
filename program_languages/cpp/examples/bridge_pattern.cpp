#include <iostream>
#include <optional>
#include <string>
#include <memory>

class Base
{
protected:
    class Impl
    {
    public:
        virtual void print() { std::cout << "Impl in Base" << std::endl; };
    };

    std::shared_ptr<Impl> pImp_;

public:
    Base() { pImp_ = std::make_shared<Impl>(); }
    virtual void printImp()
    {
        pImp_->print();
    }

    virtual void print()
    {
        std::cout << "Base" << std::endl;
    }
};

class Derived : public Base
{
protected:
    class Impl : public Base::Impl
    {
    public:
        Impl() = default;
        void print() override
        {
            std::cout << "Impl in Derived" << std::endl;
        }
    };

public:
    Derived()
    {
        pImp_ = std::make_shared<Impl>();
    }

    void printImp() override
    {
        pImp_->print();
    }

    void print() override
    {
        std::cout << "Derived" << std::endl;
    }
};

void printItPassByRef(Base &b)
{
    std::cout << "**** From printItPassByRef" << std::endl;
    b.print();
    b.printImp();
}

void printItPassByValue(Base b)
{
    std::cout << "**** From printItPassByValue" << std::endl;
    b.print();
    b.printImp();
}

int main()
{
    auto pDerived = std::make_unique<Derived>();

    std::cout << "**** From Main" << std::endl;
    pDerived->print();

    printItPassByRef(*pDerived);

    printItPassByValue(*pDerived);

    return 0;
}