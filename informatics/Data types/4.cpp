#include <iostream>
#include <cmath>
using namespace std;
int main()
{
    int n;
    cin >> n;
    double pi = 0; 
    for (int i = 0; i < n; i++)
    {
    pi += ((4 * (pow(-1, i))) / (2 * i + 1));
    }
    // pi *= 4;
 
    
    cout << pi;
    return 0;
}