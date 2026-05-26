#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int N; long long M; if(!(cin>>N>>M)) return 0;
    vector<long long> t(N); long long mn=LLONG_MAX;
    for(auto &x:t){cin>>x; mn=min(mn,x);}
    long long l=0, r=mn*M;
    while(l<r){
        long long mid=(l+r)/2;
        __int128 made=0;
        for(long long x:t){ made += mid/x; if(made>=M) break; }
        if(made>=M) r=mid; else l=mid+1;
    }
    cout<<l<<"\n";
    return 0;
}
