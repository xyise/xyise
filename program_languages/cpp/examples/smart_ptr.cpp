#include <memory>
#include <iostream>
#include <exception>

class A
{
private:
    std::shared_ptr<int> ptr;

public:
    A(std::shared_ptr<int> p) : ptr(std::move(p)) {}
    void print()
    {
        std::cout << "A::print() " << *ptr << ", " << "count: " << ptr.use_count() << std::endl;
    }
};

class B
{
private:
    int *ptr;

public:
    B(int *p) : ptr(p) {}
    void print()
    {
        std::cout << "B:print() " << *ptr << std::endl;
    }
};

class C
{
private:
    std::shared_ptr<int> ptr;

public:
    C(int *p) : ptr(p) {}
    void print()
    {
        std::cout << "C:print() " << *ptr << std::endl;
    }
};

A make_A()
{
    std::shared_ptr<int> p = std::make_shared<int>(42);
    std::cout << p.use_count() << std::endl;
    A a(p);
    a.print();
    std::cout << p.use_count() << std::endl;
    return a;
}

A run_make_A()
{
    A a = make_A();
    a.print();
    return a;
}

B make_B()
{
    int val_a = 30;
    B b(&val_a);
    b.print();
    return b;
}

B run_make_B()
{
    B b = make_B();
    b.print();
    return b;
}

B make_B_2()
{
    auto pb = std::make_shared<int>(42);
    B b(pb.get());
    b.print();
    return b;
}

// C make_C()
// {
//     auto p = std::make_shared<int>(42);
//     C c(p.get());
//     c.print();
//     return c;
// }

class K
{
private:
    B *ptr;

public:
    K(B *p) : ptr(p) {}
    void print()
    {
        std::cout << "K:print() ";
        ptr->print();
    }
};

K make_K()
{
    auto p = std::make_shared<int>(42);
    B b(p.get());
    b.print();
    K k(&b);
    k.print();
    return k;
}

int main()
{
    // auto a = run_make_A();
    // std::cout << "** back in main **" << std::endl;
    // a.print();
    // std::cout << "End of main" << std::endl;

    // // B
    // auto b = run_make_B();
    // b.print();

    // auto b2 = make_B_2();
    // b2.print();

    // C
    // auto c = make_C();
    // c.print();
    // auto p = std::make_shared<int>(42);
    // C c(p.get());

    // int *d = new int(42);
    // std::cout << "Before delete: " << "addr: " << d << " val: " << *d << std::endl;

    // delete d;

    // std::cout << "After delete: " << "addr: " << d << " val: " << *d << std::endl;

    // B *b = new B(d);
    // std::cout << "Before" << std::endl;
    // b->print();
    // delete b;
    // std::cout << "After" << std::endl;
    // b->print();


    auto k = make_K();
    k.print();

    return 0;
}