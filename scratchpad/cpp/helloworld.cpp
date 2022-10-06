#include <iostream>
#include <vector>
#include <string>
#include <math.h>


using namespace std;

int main()
{

    double a1 = 1.1;
    double a2 = 0.1;
    double a = a1 + a2; 
    double b = 1.2;

    if (abs(a - b) < 1.0e-12)
    {
        cout << "Yes" << endl;
    }
    else
    {
        cout << "No" << endl;
    }

    // vector<int> vect(arr, arr + n); 
    // for (int x : vect)
    //     cout << x << " ";
    // cout << "Hello World" << endl;
}