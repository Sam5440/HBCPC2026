#include <bits/stdc++.h>
using namespace std; using ll=long long;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; ll m; if(!(cin>>n>>m)) return 0;
    vector<int> t(n); for(int&i:t) cin>>i;
    ll lo=0, hi=*min_element(t.begin(),t.end())*m;
    while(lo<hi){
        ll mid=(lo+hi)/2, made=0;
        for(int x:t){ made += mid/x; if(made>=m) break; }
        if(made>=m) hi=mid; else lo=mid+1;
    }
    cout<<lo<<"\n";
}
