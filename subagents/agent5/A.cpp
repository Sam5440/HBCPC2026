#include <bits/stdc++.h>
using namespace std;

int gain(int x, int y){ return (y - x + 5) % 5; }

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if(!(cin >> n)) return 0;
    vector<int>a(n);
    for(int &x:a) cin >> x;
    const long long NEG = -(1LL<<60);
    static long long dp[6][6][6][6], ndp[6][6][6][6];
    for(int i=0;i<6;i++)for(int j=0;j<6;j++)for(int k=0;k<6;k++)for(int l=0;l<6;l++) dp[i][j][k][l]=NEG;
    dp[0][0][0][0]=0;
    for(int x:a){
        for(int i=0;i<6;i++)for(int j=0;j<6;j++)for(int k=0;k<6;k++)for(int l=0;l<6;l++) ndp[i][j][k][l]=NEG;
        for(int fk=0;fk<6;fk++)for(int lk=0;lk<6;lk++)for(int ft=0;ft<6;ft++)for(int lt=0;lt<6;lt++){
            long long v=dp[fk][lk][ft][lt];
            if(v==NEG) continue;
            int nfk=fk?fk:x, nlk=x;
            long long add = lk?gain(lk,x):0;
            ndp[nfk][nlk][ft][lt]=max(ndp[nfk][nlk][ft][lt], v+add);
            int nft=ft?ft:x, nlt=x;
            add = lt?gain(lt,x):0;
            ndp[fk][lk][nft][nlt]=max(ndp[fk][lk][nft][nlt], v+add);
        }
        memcpy(dp, ndp, sizeof(dp));
    }
    long long ans=0;
    for(int fk=0;fk<6;fk++)for(int lk=0;lk<6;lk++)for(int ft=0;ft<6;ft++)for(int lt=0;lt<6;lt++){
        long long v=dp[fk][lk][ft][lt];
        if(v==NEG) continue;
        if(lk && ft) v += gain(lk, ft);
        ans=max(ans,v);
    }
    cout << ans + n << "\n";
    return 0;
}
