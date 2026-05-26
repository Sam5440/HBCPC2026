#include <bits/stdc++.h>
using namespace std;
int val(int x,int y){return (y-x+5)%5;}
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    const int NEG=-1e9;
    static int dp[6][6][6], ndp[6][6][6];
    for(int a=0;a<6;a++)for(int b=0;b<6;b++)for(int c=0;c<6;c++) dp[a][b][c]=NEG;
    dp[5][5][5]=0;
    for(int i=0,x;i<n;i++){
        cin>>x; --x;
        for(int a=0;a<6;a++)for(int b=0;b<6;b++)for(int c=0;c<6;c++) ndp[a][b][c]=NEG;
        for(int lf=0;lf<6;lf++)for(int fb=0;fb<6;fb++)for(int lb=0;lb<6;lb++){
            int cur=dp[lf][fb][lb]; if(cur<0) continue;
            int add = (lf==5?0:val(lf,x));
            ndp[x][fb][lb]=max(ndp[x][fb][lb], cur+add);
            if(fb==5) ndp[lf][x][x]=max(ndp[lf][x][x], cur);
            else ndp[lf][fb][x]=max(ndp[lf][fb][x], cur+val(lb,x));
        }
        memcpy(dp,ndp,sizeof(dp));
    }
    int best=0;
    for(int lf=0;lf<6;lf++)for(int fb=0;fb<6;fb++)for(int lb=0;lb<6;lb++){
        int cur=dp[lf][fb][lb]; if(cur<0) continue;
        if(lf!=5 && fb!=5) cur+=val(lf,fb);
        best=max(best,cur);
    }
    cout << best + n << "\n";
}
