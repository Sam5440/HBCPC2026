#include <bits/stdc++.h>
using namespace std;
using ll=long long;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,q; if(!(cin>>n>>q)) return 0;
    vector<vector<pair<int,ll>>> g(n+1);
    for(int i=0;i<n-1;i++){int u,v;ll w;cin>>u>>v>>w;g[u].push_back({v,w});g[v].push_back({u,w});}
    vector<pair<int,int>> queries(q);
    int LOG=1; while((1<<LOG)<=n) LOG++;
    vector<vector<int>> up(LOG, vector<int>(n+1));
    vector<int> dep(n+1);
    vector<ll> dist(n+1);
    vector<int> st={1}; up[0][1]=1;
    for(size_t it=0;it<st.size();it++){
        int u=st[it];
        for(auto [v,w]:g[u]) if(v!=up[0][u]){
            up[0][v]=u; dep[v]=dep[u]+1; dist[v]=dist[u]+w; st.push_back(v);
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
    auto dis=[&](int a,int b)->ll{int c=lca(a,b); return dist[a]+dist[b]-2*dist[c];};
    auto farthest=[&](int s){
        vector<ll> d(n+1,LLONG_MIN/4); d[s]=0;
        vector<int> order={s}, par(n+1);
        for(size_t i=0;i<order.size();i++){
            int u=order[i];
            for(auto [v,w]:g[u]) if(v!=par[u]){par[v]=u; d[v]=d[u]+w; order.push_back(v);}
        }
        int id=s; for(int i=1;i<=n;i++) if(d[i]>d[id]) id=i;
        return id;
    };
    int A=farthest(1), B=farthest(A);
    for(int i=0;i<q;i++) cin>>queries[i].first>>queries[i].second;
    if(n<=5000){
        for(auto [x,y]:queries){
            ll ans=LLONG_MIN/4;
            for(int u=1;u<=n;u++) ans=max(ans, dis(x,u)+dis(y,u));
            cout<<ans<<"\n";
        }
    }else{
        for(auto [x,y]:queries){
            cout << max(dis(x,A)+dis(y,A), dis(x,B)+dis(y,B)) << "\n";
        }
    }
}
