#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    vector<int>a(n); for(int&i:a){cin>>i;--i;}
    const long long NEG=-4e18;
    static long long dp[6][6][6][6], ndp[6][6][6][6];
    for(auto &x:dp) for(auto &y:x) for(auto &z:y) for(long long &v:z) v=NEG;
    dp[5][5][5][5]=0;
    for(int v:a){
        for(auto &x:ndp) for(auto &y:x) for(auto &z:y) for(long long &t:z) t=NEG;
        for(int fk=0;fk<6;fk++)for(int lk=0;lk<6;lk++)for(int fm=0;fm<6;fm++)for(int lm=0;lm<6;lm++){
            long long cur=dp[fk][lk][fm][lm]; if(cur<NEG/2) continue;
            int nfk=fk==5?v:fk, nlk=v;
            long long add=(lk==5?0:(v-lk+5)%5);
            ndp[nfk][nlk][fm][lm]=max(ndp[nfk][nlk][fm][lm],cur+add);
            int nfm=fm==5?v:fm, nlm=v;
            add=(lm==5?0:(v-lm+5)%5);
            ndp[fk][lk][nfm][nlm]=max(ndp[fk][lk][nfm][nlm],cur+add);
        }
        memcpy(dp,ndp,sizeof(dp));
    }
    long long best=0;
    for(int fk=0;fk<6;fk++)for(int lk=0;lk<6;lk++)for(int fm=0;fm<6;fm++)for(int lm=0;lm<6;lm++){
        long long cur=dp[fk][lk][fm][lm]; if(cur<NEG/2) continue;
        if(lk!=5 && fm!=5) cur+=(fm-lk+5)%5;
        best=max(best,cur);
    }
    cout<<best+n<<"\n";
}
