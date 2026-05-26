#include <bits/stdc++.h>
using namespace std;
struct DSU{ vector<int> p; DSU(int n=0){init(n);} void init(int n){p.resize(n+1); iota(p.begin(),p.end(),0);} int find(int x){return p[x]==x?x:p[x]=find(p[x]);} bool unite(int a,int b){a=find(a);b=find(b); if(a==b)return false; p[b]=a; return true;} };
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,m,q; if(!(cin>>n>>m>>q)) return 0;
    vector<long long>a(n+1);
    for(int i=1;i<=n;i++) cin>>a[i];
    struct Edge{int u,v; long long w;};
    vector<Edge> e(m);
    for(auto &x:e) cin>>x.u>>x.v>>x.w;
    sort(e.begin(),e.end(),[](auto&x,auto&y){return x.w<y.w;});
    while(q--){
        int op; cin>>op;
        if(op==1){int c; long long t; cin>>c>>t; a[c]=t;}
        else{
            int k; cin>>k;
            vector<int> id(n);
            iota(id.begin(),id.end(),1);
            sort(id.begin(),id.end(),[&](int x,int y){ if(a[x]!=a[y]) return a[x]>a[y]; return x<y;});
            vector<char> need(n+1,false);
            for(int i=0;i<k;i++) need[id[i]]=true;
            if(k<=1){ cout<<0<<"\n"; continue; }
            DSU d(n); vector<int> cnt(n+1);
            for(int i=1;i<=n;i++) cnt[i]=need[i];
            long long ans=0;
            for(auto &ed:e){
                int ru=d.find(ed.u), rv=d.find(ed.v);
                if(ru==rv) continue;
                d.p[rv]=ru; cnt[ru]+=cnt[rv];
                if(cnt[ru]==k){ ans=ed.w; break; }
            }
            cout<<ans<<"\n";
        }
    }
    return 0;
}
