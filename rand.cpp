#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

int main()
{
    srand((unsigned)time(0));
    for (int x = 0; x < 10; x++) 
    {
    	double r = ((double) rand() / (RAND_MAX)) + 1;
    
    	if (r < 1.25) cout << "a";
    	else if (r < 1.5) cout << "b";
    	else if (r < 1.75) cout << "c";
    	else cout << "d";
    	cout << endl;
   }
}
