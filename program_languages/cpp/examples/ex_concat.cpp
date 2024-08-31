#include <iostream>
#include <string>

using namespace std;

void version1()
{
    string s = "";
    
    for(char c = 'a'; c <= 'z'; c++) {
        s += c;
    }
    
    cout << s << endl;
}

void version2()
{
    char c;
    string s="";
    
    for(int i=0; i<26; i++)
    {
        c = 'a' + i;
        s += c;
    }
    
    cout << s << endl;
}


struct Person {
    string name;
    int age;
};

int main() {

    struct Person p1;
    Person p2;
    
    version1();
    version2();

    return 0;
}