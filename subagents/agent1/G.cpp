#include <bits/stdc++.h>
using namespace std;
struct DSU{vector<int>p,sz;DSU(int n=0):p(n+1),sz(n+1,1){iota(p.begin(),p.end(),0);}int f(int x){return p[x]==x?x:p[x]=f(p[x]);}void unite(int a,int b){a=f(a);b=f(b);if(a!=b){if(sz[a]<sz[b])swap(a,b);p[b]=a;sz[a]+=sz[b];}}};
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);
 int n,m,q; if(!(cin>>n>>m>>q)) return 0; vector<long long>a(n+1); for(int i=1;i<=n;i++)cin>>a[i];
 vector<tuple<int,int,int>> edges(m); for(auto &e:edges){int x,y,d;cin>>x>>y>>d;e={d,x,y};} sort(edges.begin(),edges.end());
 while(q--){int op;cin>>op; if(op==1){int c;long long t;cin>>c>>t;a[c]=t;}else{int k;cin>>k; vector<int> id(n); iota(id.begin(),id.end(),1); sort(id.begin(),id.end(),[&](int x,int y){if(a[x]!=a[y])return a[x]>a[y];return x<y;}); vector<char> need(n+1); for(int i=0;i<k;i++)need[id[i]]=1; if(k<=1){cout<<0<<"\n";continue;} DSU dsu(n); int comp=k; long long ans=0; for(auto [w,u,v]:edges){int fu=dsu.f(u),fv=dsu.f(v); if(fu!=fv){bool bu=false,bv=false; for(int i=0;i<k;i++){bu|=dsu.f(id[i])==fu; bv|=dsu.f(id[i])==fv;} dsu.unite(u,v); if(bu&&bv){comp--; ans=w; if(comp==1)break;}}} cout<<ans<<"\n";}}
}
