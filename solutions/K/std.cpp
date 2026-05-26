#include <bits/stdc++.h>
using namespace std;
int id(char c){ return c=='R'?0:c=='G'?1:2; }
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; if(!(cin>>T)) return 0;
    const char ch[3]={'R','G','B'};
    while(T--){
        int n,m; array<int,3> rem; cin>>n>>m>>rem[0]>>rem[1]>>rem[2];
        vector<pair<int,int>> seg(m);
        vector<char> ans(n,'?');
        for(auto &p:seg){cin>>p.first>>p.second; --p.first; --p.second;}
        bool ok=true;
        for(auto [l,r]:seg){
            int len=r-l+1, choose=-1;
            vector<int> order={0,1,2};
            sort(order.begin(),order.end(),[&](int a,int b){return rem[a]<rem[b];});
            for(int avoid:order){
                int a=(avoid+1)%3,b=(avoid+2)%3;
                if(rem[a]+rem[b]>=len){choose=avoid; break;}
            }
            if(choose==-1){ok=false;break;}
            vector<int> use;
            for(int c=0;c<3;c++) if(c!=choose) use.push_back(c);
            sort(use.begin(),use.end(),[&](int a,int b){return rem[a]>rem[b];});
            for(int i=l;i<=r;i++){
                int c = rem[use[0]]>0 ? use[0] : use[1];
                ans[i]=ch[c]; rem[c]--;
            }
        }
        if(ok){
            for(int i=0;i<n;i++) if(ans[i]=='?'){
                int c=max_element(rem.begin(),rem.end())-rem.begin();
                if(rem[c]<=0){ok=false;break;}
                ans[i]=ch[c]; rem[c]--;
            }
        }
        for(int c=0;c<3;c++) if(rem[c]!=0) ok=false;
        if(ok){
            for(auto [l,r]:seg){
                set<char> s;
                for(int i=l;i<=r;i++) s.insert(ans[i]);
                if(s.size()>2) ok=false;
            }
        }
        if(!ok) cout << -1 << "\n";
        else { for(char c:ans) cout<<c; cout<<"\n"; }
    }
}
