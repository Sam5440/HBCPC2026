#include <bits/stdc++.h>
using namespace std; using ll=long long;
struct Edge{int u,v; int d;};
struct Op{int type,c; int t;};
struct DSU{
    vector<int> p,sz,cnt;
    DSU(int n=0){init(n);}
    void init(int n){p.resize(n+1);sz.assign(n+1,1);cnt.assign(n+1,0);iota(p.begin(),p.end(),0);}
    int find(int x){while(p[x]!=x)x=p[x]=p[p[x]];return x;}
    int unite(int a,int b){a=find(a);b=find(b);if(a==b)return a;if(sz[a]<sz[b])swap(a,b);p[b]=a;sz[a]+=sz[b];cnt[a]+=cnt[b];return a;}
};
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,m,q; if(!(cin>>n>>m>>q)) return 0;
    vector<int>a(n+1); for(int i=1;i<=n;i++) cin>>a[i];
    vector<Edge> edges(m);
    for(auto &e:edges) cin>>e.u>>e.v>>e.d;
    sort(edges.begin(),edges.end(),[](const Edge&A,const Edge&B){return A.d<B.d;});
    vector<Op> ops; ops.reserve(q); bool onlyK1=true;
    for(int i=0;i<q;i++){
        int op; cin>>op;
        if(op==1){int c,t;cin>>c>>t;ops.push_back({1,c,t});}
        else{int k;cin>>k;ops.push_back({2,k,0}); if(k!=1) onlyK1=false;}
    }
    if(onlyK1){
        for(auto &op:ops){ if(op.type==1) a[op.c]=op.t; else cout<<0<<"\n"; }
        return 0;
    }
    for(auto &op:ops){
        if(op.type==1){ a[op.c]=op.t; continue; }
        int k=op.c;
        vector<int> id(n); iota(id.begin(),id.end(),1);
        nth_element(id.begin(), id.begin()+k, id.end(), [&](int x,int y){ if(a[x]!=a[y]) return a[x]>a[y]; return x<y; });
        id.resize(k);
        vector<char> sel(n+1,0); for(int x:id) sel[x]=1;
        if(k<=1){ cout<<0<<"\n"; continue; }
        DSU dsu(n); for(int i=1;i<=n;i++) dsu.cnt[i]=sel[i];
        int ans=0;
        for(auto &e:edges){
            int r=dsu.unite(e.u,e.v);
            if(dsu.cnt[dsu.find(r)]==k){ ans=e.d; break; }
        }
        cout<<ans<<"\n";
    }
}
