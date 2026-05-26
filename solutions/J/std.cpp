#include <bits/stdc++.h>
using namespace std; using ll=long long;
ll best(ll A,ll B,ll M){
    if(B>=12*A) return M/A;
    ll d=M/B, rem=M-d*B;
    ll ans=12*d+rem/A;
    if(d>0) ans=max(ans,12*(d-1)+(rem+B)/A);
    return ans;
}
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; ll M; if(!(cin>>n>>M)) return 0;
    ll bestCnt=-1; int bestId=1;
    for(int i=1;i<=n;i++){
        ll A,B; cin>>A>>B; ll cur=best(A,B,M);
        if(cur>bestCnt){bestCnt=cur; bestId=i;}
    }
    cout<<bestCnt<<" "<<bestId<<"\n";
}
