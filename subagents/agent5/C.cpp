#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n,q;
    if(!(cin>>n>>q)) return 0;
    vector<vector<pair<int,ll>>> g(n+1);
    for(int i=0;i<n-1;i++){
        int u,v; ll w; cin>>u>>v>>w;
        g[u].push_back({v,w});
        g[v].push_back({u,w});
    }
    int LOG=1;
    while((1<<LOG)<=n) LOG++;
    vector<vector<int>> up(LOG, vector<int>(n+1));
    vector<int> dep(n+1);
    vector<ll> dist(n+1);
    vector<int> st={1}; up[0][1]=1;
    vector<int> par(n+1,0); par[1]=1;
    for(size_t it=0;it<st.size();it++){
        int u=st[it];
        for(auto [v,w]:g[u]) if(v!=par[u]){
            par[v]=u; up[0][v]=u; dep[v]=dep[u]+1; dist[v]=dist[u]+w; st.push_back(v);
        }
    }
    for(int j=1;j<LOG;j++) for(int i=1;i<=n;i++) up[j][i]=up[j-1][up[j-1][i]];
    auto lca=[&](int a,int b){
        if(dep[a]<dep[b]) swap(a,b);
        int d=dep[a]-dep[b];
        for(int j=0;j<LOG;j++) if(d>>j&1) a=up[j][a];
        if(a==b) return a;
        for(int j=LOG-1;j>=0;j--) if(up[j][a]!=up[j][b]) a=up[j][a], b=up[j][b];
        return up[0][a];
    };
    auto dis=[&](int a,int b)->ll{
        int c=lca(a,b);
        return dist[a]+dist[b]-2*dist[c];
    };
    const int BRUTE_LIMIT = 20000000;
    bool brute = 1LL*n*q <= BRUTE_LIMIT;
    while(q--){
        int x,y; cin>>x>>y;
        if(brute){
            ll best=LLONG_MIN;
            for(int u=1;u<=n;u++) best=max(best, dis(x,u)+dis(y,u));
            cout<<best<<"\n";
        }else{
            ll best=LLONG_MIN;
            for(int u=1;u<=n;u++) best=max(best, dis(x,u)+dis(y,u));
            cout<<best<<"\n";
        }
    }
    return 0;
}
