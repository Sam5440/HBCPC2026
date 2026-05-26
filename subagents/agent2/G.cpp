#include <bits/stdc++.h>
using namespace std;
struct DSU{vector<int> p,sz;DSU(int n=0){init(n);}void init(int n){p.resize(n+1);sz.assign(n+1,1);iota(p.begin(),p.end(),0);}int find(int x){return p[x]==x?x:p[x]=find(p[x]);}bool unite(int a,int b){a=find(a);b=find(b);if(a==b)return false;if(sz[a]<sz[b])swap(a,b);p[b]=a;sz[a]+=sz[b];return true;}};
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,m,q; if(!(cin>>n>>m>>q)) return 0;
    vector<long long>a(n+1); for(int i=1;i<=n;i++) cin>>a[i];
    struct E{int u,v;long long w;};
    vector<E> e(m); for(auto &x:e) cin>>x.u>>x.v>>x.w;
    sort(e.begin(),e.end(),[](auto &x,auto&y){return x.w<y.w;});
    vector<vector<pair<int,long long>>> tree(n+1);
    DSU d(n);
    for(auto &x:e) if(d.unite(x.u,x.v)){tree[x.u].push_back({x.v,x.w});tree[x.v].push_back({x.u,x.w});}
    int LOG=1; while((1<<LOG)<=n) LOG++;
    vector<vector<int>> up(LOG, vector<int>(n+1));
    vector<vector<long long>> mx(LOG, vector<long long>(n+1));
    vector<int> dep(n+1), order={1}; up[0][1]=1;
    for(size_t i=0;i<order.size();i++){
        int u=order[i];
        for(auto [v,w]:tree[u]) if(v!=up[0][u]){up[0][v]=u;mx[0][v]=w;dep[v]=dep[u]+1;order.push_back(v);}
    }
    for(int j=1;j<LOG;j++)for(int i=1;i<=n;i++){up[j][i]=up[j-1][up[j-1][i]];mx[j][i]=max(mx[j-1][i],mx[j-1][up[j-1][i]]);}
    auto pathmax=[&](int u,int v){
        long long ans=0;
        if(dep[u]<dep[v]) swap(u,v);
        int diff=dep[u]-dep[v];
        for(int j=0;j<LOG;j++) if(diff>>j&1){ans=max(ans,mx[j][u]);u=up[j][u];}
        if(u==v) return ans;
        for(int j=LOG-1;j>=0;j--) if(up[j][u]!=up[j][v]){ans=max({ans,mx[j][u],mx[j][v]});u=up[j][u];v=up[j][v];}
        return max({ans,mx[0][u],mx[0][v]});
    };
    set<pair<long long,int>> ord;
    for(int i=1;i<=n;i++) ord.insert({-a[i],i});
    while(q--){
        int op; cin>>op;
        if(op==1){int c; long long t; cin>>c>>t; ord.erase({-a[c],c}); a[c]=t; ord.insert({-a[c],c});}
        else{
            int k; cin>>k;
            vector<int> v; v.reserve(k);
            auto it=ord.begin(); for(int i=0;i<k;i++,++it) v.push_back(it->second);
            long long ans=0;
            for(int i=1;i<k;i++) ans=max(ans,pathmax(v[0],v[i]));
            cout<<ans<<"\n";
        }
    }
}
