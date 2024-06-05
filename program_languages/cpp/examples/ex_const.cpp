#include <iostream>
#include <string>

using namespace std;

class MyClass
{
    private:
        int *a;
        int b;
        string s = "Hello";
    public:
        MyClass(int a, int b) : a(new int(a)), b(b) {}
        ~MyClass() { delete a; }
        int &get_a() const { return *a; } // This compiles.
        int &get_b() { return b; }
        // int &get_b_const() const { return b; } // This does not compile. See https://stackoverflow.com/questions/5055427/returning-non-const-reference-from-a-const-member-function
        const int &get_const_b() { return b; }
        const int &get_const_b_const() const { return b; }
        string &get_s() { return s; }
        const string &get_const_s_const() { return s; }
};

void const_ex()
{
    MyClass mc(1, 2);
    mc.get_a() = 3;
    int const_b_const = mc.get_const_b_const();
    int const_b = mc.get_const_b();
    int b = mc.get_b();
    std::cout << const_b_const << " " << const_b << " " << b << std::endl;
    b = 3; // This does not change the value of b in mc.
    std::cout << mc.get_b() << std::endl;

    string& ref_s = mc.get_s();
    ref_s[0] = 'a'; 
    cout << mc.get_s() << endl; 

//    string& ref_s_const = mc.get_const_s_const(); // This does not compile.
    string s_const = mc.get_const_s_const(); // This compiles.
    s_const[0] = 'b'; // This does not change the value of s in mc.
    cout << mc.get_s() << endl;
}


int main()
{
    const_ex();
    return 0;
}