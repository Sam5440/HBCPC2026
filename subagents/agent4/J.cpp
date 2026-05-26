#include <bits/stdc++.h>
using namespace std;
using ll=long long;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int N; ll M; if(!(cin>>N>>M)) return 0;
    ll best=-1; int idx=1;
    for(int i=1;i<=N;i++){
        ll A,B; cin>>A>>B;
        ll cur=M/A;
        ll p=M/B;
        for(ll d=0; d<=100 && p-d>=0; d++){
            ll pp=p-d;
            cur=max(cur, pp*12 + (M-pp*B)/A);
        }
        if(cur>best){best=cur;idx=i;}
    }
    cout<<best<<" "<<idx<<"\n";
}
