#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; if(!(cin>>T)) return 0;
    while(T--){
        int n,m; array<int,3> need; cin>>n>>m>>need[0]>>need[1]>>need[2];
        vector<pair<int,int>> seg(m); vector<int> len(m);
        int covered=0;
        for(int i=0;i<m;i++){cin>>seg[i].first>>seg[i].second; len[i]=seg[i].second-seg[i].first+1; covered+=len[i];}
        array<int,3> cap = {n-need[0], n-need[1], n-need[2]};
        vector<int> ord(m); iota(ord.begin(),ord.end(),0);
        sort(ord.begin(),ord.end(),[&](int a,int b){return len[a]>len[b];});
        vector<int> omit(m,-1); array<int,3> rem=cap; bool ok=true;
        for(int id:ord){
            int best=-1;
            for(int c=0;c<3;c++) if(rem[c]>=len[id] && (best==-1 || rem[c]>rem[best])) best=c;
            if(best==-1){ok=false;break;}
            omit[id]=best; rem[best]-=len[id];
        }
        if(!ok){ cout<<"-1\n"; continue; }
        string ans(n,'?'); array<int,3> left=need; const string cs="RGB";
        vector<vector<int>> allowed(n);
        for(int i=0;i<n;i++) allowed[i]={0,1,2};
        for(int i=0;i<m;i++){
            for(int p=seg[i].first-1;p<=seg[i].second-1;p++){
                allowed[p].clear();
                for(int c=0;c<3;c++) if(c!=omit[i]) allowed[p].push_back(c);
            }
        }
        vector<int> pos(n); iota(pos.begin(),pos.end(),0);
        sort(pos.begin(),pos.end(),[&](int a,int b){return allowed[a].size()<allowed[b].size();});
        for(int p:pos){
            int best=-1;
            for(int c:allowed[p]) if(left[c]>0 && (best==-1 || left[c]>left[best])) best=c;
            if(best==-1){ok=false;break;}
            ans[p]=cs[best]; left[best]--;
        }
        if(!ok || left[0]||left[1]||left[2]) cout<<"-1\n"; else cout<<ans<<"\n";
    }
}
