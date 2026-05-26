#include <bits/stdc++.h>
using namespace std;
int addv(int x,int y){return (y-x+5)%5;}
int main(){
    ios::sync_with_stdio(false);cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    vector<int>a(n); for(int&i:a){cin>>i;--i;}
    const long long NEG=-4e18;
    long long best=NEG;
    // Stable partition into kept then moved. DP tracks last kept and last moved.
    for(int first=0; first<5; ++first){
        long long dp[6][6], ndp[6][6];
        for(auto &r:dp) for(long long &x:r) x=NEG;
        dp[5][5]=0;
        for(int x:a){
            for(auto &r:ndp) for(long long &v:r) v=NEG;
            for(int lk=0;lk<6;lk++) for(int lm=0;lm<6;lm++) if(dp[lk][lm]>NEG/2){
                long long cur=dp[lk][lm];
                int nlk=x;
                ndp[nlk][lm]=max(ndp[nlk][lm], cur+(lk==5?0:addv(lk,x)));
                if(lm==5){
                    if(x==first) ndp[lk][x]=max(ndp[lk][x], cur);
                }else{
                    ndp[lk][x]=max(ndp[lk][x], cur+addv(lm,x));
                }
            }
            memcpy(dp,ndp,sizeof(dp));
        }
        for(int lk=0;lk<6;lk++) for(int lm=0;lm<6;lm++) if(dp[lk][lm]>NEG/2){
            long long val=dp[lk][lm];
            if(lk!=5 && lm!=5) val+=addv(lk,first);
            best=max(best,val);
        }
    }
    // no moved item
    long long val=0; for(int i=1;i<n;i++) val+=addv(a[i-1],a[i]);
    best=max(best,val);
    cout << best + n << "\n";
}
