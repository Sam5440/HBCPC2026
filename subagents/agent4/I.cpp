#include <bits/stdc++.h>
using namespace std;
using ll=long long;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int N; long long M; if(!(cin>>N>>M)) return 0;
    vector<int> t(N); for(int&i:t)cin>>i;
    ll lo=0, hi=*min_element(t.begin(),t.end())*M;
    while(lo<hi){
        ll mid=(lo+hi)/2; __int128 made=0;
        for(int x:t){ made+=mid/x; if(made>=M) break; }
        if(made>=M) hi=mid; else lo=mid+1;
    }
    cout<<lo<<"\n";
}
