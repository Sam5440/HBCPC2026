#include <bits/stdc++.h>
using namespace std;
static int gain(int x, int y){ return (y - x + 5) % 5; }
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    vector<int>a(n); for(int&i:a) cin>>i;
    if(n > 24) return 0;
    long long best = 0;
    for(long long mask=0; mask<(1LL<<n); ++mask){
        vector<int> b;
        for(int i=0;i<n;i++) if(!(mask>>i&1)) b.push_back(a[i]);
        for(int i=0;i<n;i++) if(mask>>i&1) b.push_back(a[i]);
        long long cur = n;
        for(int i=1;i<n;i++) cur += gain(b[i-1], b[i]);
        best = max(best, cur);
    }
    cout << best << "\n";
}
