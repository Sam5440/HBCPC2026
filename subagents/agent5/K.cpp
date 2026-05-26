#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; if(!(cin>>T)) return 0;
    while(T--){
        int n,m; int cnt[3]; cin>>n>>m>>cnt[0]>>cnt[1]>>cnt[2];
        vector<pair<int,int>> seg(m);
        for(auto &p:seg) cin>>p.first>>p.second;
        string ans(n,'?');
        vector<int> order={0,1,2};
        bool ok=false;
        string chars="RGB";
        sort(order.begin(),order.end());
        do{
            int rem[3]={cnt[0],cnt[1],cnt[2]};
            string s(n,'?');
            for(int i=0;i<n;i++){
                for(int c:order) if(rem[c]>0){ s[i]=chars[c]; rem[c]--; break; }
            }
            bool good=true;
            for(auto [l,r]:seg){
                bool seen[3]={0,0,0};
                for(int i=l-1;i<=r-1;i++){
                    int c=chars.find(s[i]);
                    seen[c]=true;
                }
                if(seen[0]&&seen[1]&&seen[2]){ good=false; break; }
            }
            if(good){ ans=s; ok=true; break; }
        }while(next_permutation(order.begin(),order.end()));
        if(ok) cout<<ans<<"\n"; else cout<<"-1\n";
    }
    return 0;
}
