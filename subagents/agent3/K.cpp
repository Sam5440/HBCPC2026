#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; if(!(cin>>T)) return 0;
    while(T--){
        int n,m; array<int,3> cnt; cin>>n>>m>>cnt[0]>>cnt[1]>>cnt[2];
        vector<pair<int,int>> seg(m); for(auto &p:seg) cin>>p.first>>p.second;
        string chars="RGB"; vector<int> ord={0,1,2}; string ans="";
        do{
            string s; for(int c:ord) s.append(cnt[c], chars[c]);
            bool ok=true;
            for(auto [l,r]:seg){ bool seen[3]={}; int kinds=0; for(int i=l-1;i<r;i++){int c=chars.find(s[i]); if(!seen[c]) seen[c]=1,kinds++;} if(kinds>2){ok=false;break;} }
            if(ok){ans=s;break;}
        }while(next_permutation(ord.begin(),ord.end()));
        if(ans.empty()) cout<<"-1\n"; else cout<<ans<<"\n";
    }
}
