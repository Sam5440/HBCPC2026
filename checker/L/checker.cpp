#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){
    if(argc<4){cerr<<"usage: checker input output answer\n";return 2;}
    ifstream out(argv[2]), ans(argv[3]);
    long double a,b; 
    while(ans>>a){
        if(!(out>>b)) return 1;
        long double diff=fabsl(a-b);
        long double tol=1e-9L*max((long double)1.0, fabsl(a));
        if(diff>tol) return 1;
    }
    return 0;
}
