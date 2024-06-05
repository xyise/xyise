#include <map>
#include <string>

using namespace std;
int main() {
  map<int, string> m;
  for(int i = 0; i < 1000; i++)
    m[i] = to_string(i);
  return 0;
}