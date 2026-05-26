#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false);cin.tie(nullptr);
    int n,q; if(!(cin>>n>>q)) return 0;
    vector<vector<pair<int,long long>>> g(n+1);
    for(int i=0,u,v;i<n-1;i++){long long w;cin>>u>>v>>w;g[u].push_back({v,w});g[v].push_back({u,w});}
    vector<long long>d(n+1);
    vector<int>par(n+1),dep(n+1),ord{1}; par[1]=0;
    for(size_t i=0;i<ord.size();++i){int u=ord[i]; for(auto [v,w]:g[u]) if(v!=par[u]){par[v]=u;dep[v]=dep[u]+1;d[v]=d[u]+w;ord.push_back(v);}}
    int LOG=1; while((1<<LOG)<=n) LOG++;
    vector<vector<int>> up(LOG, vector<int>(n+1));
    up[0]=par; for(int k=1;k<LOG;k++) for(int i=1;i<=n;i++) up[k][i]=up[k-1][up[k-1][i]];
    auto lca=[&](int a,int b){
        if(dep[a]<dep[b]) swap(a,b);
        int diff=dep[a]-dep[b]; for(int k=0;k<LOG;k++) if(diff>>k&1) a=up[k][a];
        if(a==b) return a;
        for(int k=LOG-1;k>=0;k--) if(up[k][a]!=up[k][b]) a=up[k][a],b=up[k][b];
        return par[a];
    };
    auto dist=[&](int a,int b){int c=lca(a,b); return d[a]+d[b]-2*d[c];};
    // Exact fallback by scanning all vertices. This is intentionally simple and independent.
    while(q--){int x,y;cin>>x>>y; long long ans=LLONG_MIN; for(int u=1;u<=n;u++) ans=max(ans, dist(x,u)+dist(y,u)); cout<<ans<<"\n";}
}
