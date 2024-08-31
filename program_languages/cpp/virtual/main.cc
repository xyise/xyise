#include <iostream>

using namespace std;

class MyBase {
    protected:
    int x;
    public:
    MyBase(int x) : x(x) {}
    void print_nv() {
        cout << "MyBase::print_nv(): x = " << x << endl;
    }

    virtual void print_v() {
        cout << "MyBase::print_v(): x = " << x << endl;
    }
};

class MyDerived : public MyBase {
    private:
    int y;
    public:
    MyDerived(int x, int y) : MyBase(x), y(y) {}
    void print_nv() {
        cout << "MyDerived::print_nv(): x = " << x << ", y = " << y << endl;
    }

    // This function signature can be
    // void print_v()
    // void print_v() override 
    // virtual void print_v() 
    // virtual void print_v() override
    void print_v() {
        cout << "MyDerived::print_v(): x = " << x << ", y = " << y << endl;
    }
};

int main() {

    cout << "Through derived object:" << endl;
    MyDerived deriv_obj(2, 3);
    cout << "Calling MyDerived::print_nv():" << endl;
    deriv_obj.print_nv();
    cout << "Calling MyDerived::print_v():" << endl;
    deriv_obj.print_v();

    cout << "Through a base pointer to the derived object:" << endl;
    MyBase *deriv_ptr = &deriv_obj;
    cout << "Calling non-virtual MyDerived::print_nv() through MyBase pointer:" << endl;
    deriv_ptr->print_nv();
    cout << "Calling virtual     MyDerived::print_v() through MyBase pointer:" << endl;
    deriv_ptr->print_v();

    return 0;
}