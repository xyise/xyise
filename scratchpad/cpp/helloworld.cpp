#include <iostream>
#include <vector>
#include <string>

using namespace std;

int main()
{
    int x = 4;
    int y = 5;
    vector<double> v{2.0, 3.0, 4.0};

    int arr[] = {10, 20, 30};
    int n = sizeof(arr) / sizeof(arr[0]);

    vector<int> vect(arr, arr + n); 
    for (int x : vect)
        cout << x << " ";
    cout << "Hello World" << endl;
}