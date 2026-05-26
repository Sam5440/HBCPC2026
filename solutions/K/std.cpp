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
            int len=r-l+1;
            vector<pair<pair<int,int>, pair<int,int>>> cand;
            for(int a=0;a<3;a++) for(int b=a+1;b<3;b++){
                if(rem[a]+rem[b]>=len){
                    cand.push_back({{rem[a]+rem[b], max(rem[a], rem[b])}, {a,b}});
                }
            }
            if(cand.empty()){ok=false;break;}
            sort(cand.begin(), cand.end());
            vector<int> use={cand[0].second.first, cand[0].second.second};
            sort(use.begin(),use.end(),[&](int a,int b){return rem[a]<rem[b];});
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
