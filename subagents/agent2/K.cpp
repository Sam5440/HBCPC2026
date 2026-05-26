#include <bits/stdc++.h>
using namespace std;
int id(char c){return c=='R'?0:c=='G'?1:2;}
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; if(!(cin>>T)) return 0;
    const char C[3]={'R','G','B'};
    while(T--){
        int n,m; array<int,3> cnt; cin>>n>>m>>cnt[0]>>cnt[1]>>cnt[2];
        vector<pair<int,int>> seg(m);
        vector<int> covered(n+1,0);
        for(auto &p:seg){cin>>p.first>>p.second; for(int i=p.first;i<=p.second;i++) covered[i]=1;}
        string ans(n,'?');
        bool ok=true;
        for(auto [l,r]:seg){
            int len=r-l+1;
            array<int,3> ord={0,1,2};
            sort(ord.begin(),ord.end(),[&](int a,int b){return cnt[a]>cnt[b];});
            int a=ord[0], b=ord[1];
            for(int i=l;i<=r;i++){
                int c=(cnt[a]>=cnt[b]?a:b);
                if(cnt[c]==0) c=(c==a?b:a);
                if(cnt[c]==0){ ok=false; break; }
                ans[i-1]=C[c]; cnt[c]--;
            }
            if(!ok) break;
        }
        for(int i=1;i<=n&&ok;i++) if(!covered[i]){
            int c=max_element(cnt.begin(),cnt.end())-cnt.begin();
            if(cnt[c]==0){ok=false;break;}
            ans[i-1]=C[c]; cnt[c]--;
        }
        if(cnt[0]||cnt[1]||cnt[2]) ok=false;
        if(!ok) cout<<"-1\n"; else cout<<ans<<"\n";
    }
}
