#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    vector<int>a(n); for(int&i:a){cin>>i;--i;}
    const long long NEG=-(1LL<<60);
    static long long dp[6][6][6], ndp[6][6][6];
    for(auto &x: dp) for(auto &y:x) for(long long &z:y) z=NEG;
    dp[5][5][5]=0;
    for(int v:a){
        for(auto &x: ndp) for(auto &y:x) for(long long &z:y) z=NEG;
        for(int lk=0;lk<6;lk++)for(int lt=0;lt<6;lt++)for(int ft=0;ft<6;ft++){
            long long cur=dp[lk][lt][ft]; if(cur==NEG) continue;
            long long add = (lk==5?0:(v-lk+5)%5);
            ndp[v][lt][ft]=max(ndp[v][lt][ft],cur+add);
            add = (lt==5?0:(v-lt+5)%5);
            int nft = (ft==5?v:ft);
            ndp[lk][v][nft]=max(ndp[lk][v][nft],cur+add);
        }
        memcpy(dp,ndp,sizeof(dp));
    }
    long long ans=0;
    for(int lk=0;lk<6;lk++)for(int lt=0;lt<6;lt++)for(int ft=0;ft<6;ft++){
        long long cur=dp[lk][lt][ft]; if(cur==NEG) continue;
        if(lk!=5 && ft!=5) cur += (ft-lk+5)%5;
        ans=max(ans,cur);
    }
    cout << ans + n << "\n";
}
