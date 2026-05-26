#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,q; string s; if(!(cin>>n>>q>>s)) return 0;
    vector<array<int,26>> pref(n+1); pref[0].fill(0);
    for(int i=1;i<=n;i++){pref[i]=pref[i-1]; pref[i][s[i-1]-'a']++;}
    while(q--){int l,r;cin>>l>>r;int ans=0;for(int c=0;c<26;c++) ans=max(ans,pref[r][c]-pref[l-1][c]); cout<<ans<<"\n";}
}
