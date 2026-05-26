#include <bits/stdc++.h>
using namespace std;
using ll = long long;
struct Edge{int u,v; ll w;};
struct DSU{};
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,q; if(!(cin>>n>>q)) return 0;
    vector<Edge> edges;
    vector<vector<pair<int,ll>>> g(n+1);
    vector<ll> chainW(max(2,n+1), LLONG_MIN), starW(n+1,0);
    for(int i=0;i<n-1;i++){
        int u,v; ll w; cin>>u>>v>>w;
        edges.push_back({u,v,w});
        g[u].push_back({v,w}); g[v].push_back({u,w});
        if(abs(u-v)==1) chainW[min(u,v)] = w;
    }
    bool isChain = n==1;
    if(n>1){
        isChain = true;
        for(int i=1;i<n;i++) if(chainW[i]==LLONG_MIN) isChain=false;
    }
    int center = -1;
    for(int i=1;i<=n;i++) if((int)g[i].size()==n-1) center=i;
    bool isStar = (n<=2 || center!=-1);
    if(n<=2200){
        vector<vector<ll>> dist(n+1, vector<ll>(n+1));
        for(int s=1;s<=n;s++){
            vector<int> st = {s}, par(n+1,0);
            par[s] = -1;
            while(!st.empty()){
                int u=st.back(); st.pop_back();
                for(auto [v,w]: g[u]) if(v!=par[u]){
                    par[v]=u; dist[s][v]=dist[s][u]+w; st.push_back(v);
                }
            }
        }
        while(q--){
            int x,y; cin>>x>>y;
            ll ans = LLONG_MIN;
            for(int u=1;u<=n;u++) ans=max(ans, dist[x][u]+dist[y][u]);
            cout<<ans<<"\n";
        }
    }else if(isChain){
        vector<ll> pref(n+1,0), minPref(n+1), maxSuf(n+2);
        for(int i=1;i<n;i++) pref[i+1]=pref[i]+chainW[i];
        minPref[1]=pref[1];
        for(int i=2;i<=n;i++) minPref[i]=min(minPref[i-1],pref[i]);
        maxSuf[n]=pref[n];
        for(int i=n-1;i>=1;i--) maxSuf[i]=max(maxSuf[i+1],pref[i]);
        while(q--){
            int x,y; cin>>x>>y;
            int a=min(x,y), b=max(x,y);
            ll mid = pref[b]-pref[a];
            ll left = pref[x]+pref[y]-2*minPref[a];
            ll right = 2*maxSuf[b]-pref[x]-pref[y];
            cout << max({mid,left,right}) << "\n";
        }
    }else if(isStar){
        if(center==-1) center=1;
        for(auto [v,w]: g[center]) starW[v]=w;
        vector<int> top;
        for(int i=1;i<=n;i++) if(i!=center) top.push_back(i);
        sort(top.begin(), top.end(), [&](int a,int b){return starW[a]>starW[b];});
        if((int)top.size()>5) top.resize(5);
        auto dist=[&](int a,int b)->ll{
            if(a==b) return 0;
            if(a==center) return starW[b];
            if(b==center) return starW[a];
            return starW[a]+starW[b];
        };
        while(q--){
            int x,y; cin>>x>>y;
            vector<int> cand = {center,x,y};
            for(int v:top) cand.push_back(v);
            ll ans = LLONG_MIN;
            for(int u:cand) if(u>=1 && u<=n) ans=max(ans, dist(x,u)+dist(y,u));
            cout<<ans<<"\n";
        }
    }else{
        while(q--){
            int x,y; cin>>x>>y;
            vector<ll> dx(n+1), dy(n+1);
            auto run=[&](int s, vector<ll>&d){
                vector<int> st={s}, par(n+1,0); par[s]=-1;
                while(!st.empty()){
                    int u=st.back(); st.pop_back();
                    for(auto [v,w]:g[u]) if(v!=par[u]){
                        par[v]=u; d[v]=d[u]+w; st.push_back(v);
                    }
                }
            };
            run(x,dx); run(y,dy);
            ll ans=LLONG_MIN;
            for(int u=1;u<=n;u++) ans=max(ans,dx[u]+dy[u]);
            cout<<ans<<"\n";
        }
    }
}
