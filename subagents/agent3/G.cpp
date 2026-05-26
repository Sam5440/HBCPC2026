#include <bits/stdc++.h>
using namespace std;
struct DSU{vector<int>p,sz;DSU(int n=0){p.resize(n+1);sz.assign(n+1,1);iota(p.begin(),p.end(),0);}int f(int x){return p[x]==x?x:p[x]=f(p[x]);}bool uni(int a,int b){a=f(a);b=f(b);if(a==b)return false;if(sz[a]<sz[b])swap(a,b);p[b]=a;sz[a]+=sz[b];return true;}};
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,m,q; if(!(cin>>n>>m>>q)) return 0;
    vector<long long>a(n+1); for(int i=1;i<=n;i++) cin>>a[i];
    struct E{int u,v;long long w;}; vector<E> edges(m);
    for(auto &e:edges) cin>>e.u>>e.v>>e.w;
    sort(edges.begin(),edges.end(),[](const E&x,const E&y){return x.w<y.w;});
    while(q--){
        int op; cin>>op;
        if(op==1){int c; long long t; cin>>c>>t; a[c]=t;}
        else{
            int k; cin>>k;
            vector<int> id(n); iota(id.begin(),id.end(),1);
            nth_element(id.begin(),id.begin()+k,id.end(),[&](int x,int y){return a[x]!=a[y]?a[x]>a[y]:x<y;});
            id.resize(k); vector<char> need(n+1); for(int x:id) need[x]=1;
            if(k==1){cout<<0<<"\n"; continue;}
            DSU dsu(n); vector<int> cnt(n+1); for(int x:id) cnt[x]=1; long long ans=0; int got=0;
            for(auto &e:edges){int fu=dsu.f(e.u),fv=dsu.f(e.v); if(fu==fv) continue; int cu=cnt[fu], cv=cnt[fv]; dsu.uni(fu,fv); int fr=dsu.f(fu); cnt[fr]=cu+cv; if(cu+cv==k){ans=e.w;break;}}
            cout<<ans<<"\n";
        }
    }
}
