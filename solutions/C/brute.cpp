#include <bits/stdc++.h>
using namespace std; using ll=long long;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,q; if(!(cin>>n>>q)) return 0;
    vector<vector<pair<int,ll>>> g(n+1);
    for(int i=0;i<n-1;i++){int u,v;ll w;cin>>u>>v>>w;g[u].push_back({v,w});g[v].push_back({u,w});}
    auto dist=[&](int s){
        vector<ll>d(n+1); vector<int>st={s},p(n+1); p[s]=-1;
        while(!st.empty()){int u=st.back();st.pop_back();for(auto [v,w]:g[u])if(v!=p[u]){p[v]=u;d[v]=d[u]+w;st.push_back(v);}}
        return d;
    };
    while(q--){int x,y;cin>>x>>y; auto dx=dist(x), dy=dist(y); ll ans=LLONG_MIN; for(int u=1;u<=n;u++) ans=max(ans,dx[u]+dy[u]); cout<<ans<<"\n";}
}
