#include <chrono>
#include <iostream>
#include <thread>
#include
using namespace std;

void run_chrono()
{
    using namespace std::chrono;
    using namespace std::chrono_literals;

    // clock
    auto start = system_clock::now();
    this_thread::sleep_for(std::chrono::milliseconds(10));
    auto end = system_clock::now();
    auto duration = duration_cast<milliseconds>(end - start);
    cout << "Duration: " << duration.count() << "ms" << endl;

}

void run_lambdas()
{
    
}

int main()
{
    run_chrono();
    return 0;
}
