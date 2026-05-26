#include <bits/stdc++.h>
using namespace std;
using ll = long long;
static int gain(int x, int y){ return (y - x + 5) % 5; }
static int enc(int a,int b,int c,int d){ return (((a*6+b)*6+c)*6+d); }
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    vector<int>a(n);
    for(int&i:a) cin>>i;
    const ll NEG = -(1LL<<60);
    vector<ll> dp(6*6*6*6, NEG), ndp(6*6*6*6, NEG);
    dp[enc(0,0,0,0)] = 0;
    for(int v: a){
        fill(ndp.begin(), ndp.end(), NEG);
        for(int fk=0; fk<=5; ++fk) for(int lk=0; lk<=5; ++lk)
        for(int fm=0; fm<=5; ++fm) for(int lm=0; lm<=5; ++lm){
            ll cur = dp[enc(fk,lk,fm,lm)];
            if(cur==NEG) continue;
            if(fk==0) ndp[enc(v,v,fm,lm)] = max(ndp[enc(v,v,fm,lm)], cur);
            else ndp[enc(fk,v,fm,lm)] = max(ndp[enc(fk,v,fm,lm)], cur + gain(lk,v));
            if(fm==0) ndp[enc(fk,lk,v,v)] = max(ndp[enc(fk,lk,v,v)], cur);
            else ndp[enc(fk,lk,fm,v)] = max(ndp[enc(fk,lk,fm,v)], cur + gain(lm,v));
        }
        dp.swap(ndp);
    }
    ll best = 0;
    for(int fk=0; fk<=5; ++fk) for(int lk=0; lk<=5; ++lk)
    for(int fm=0; fm<=5; ++fm) for(int lm=0; lm<=5; ++lm){
        ll cur = dp[enc(fk,lk,fm,lm)];
        if(cur < 0) continue;
        if(fk && fm) cur += gain(lk,fm);
        best = max(best, cur);
    }
    cout << best + n << "\n";
}
