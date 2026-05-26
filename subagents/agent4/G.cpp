#include <bits/stdc++.h>
using namespace std;
struct Edge{int u,v; long long w;};
struct FHQ{
    struct Node{pair<long long,int> key; int city,prio,sz,l,r,agg;};
    vector<Node> tr; vector<vector<int>> *up; vector<int> *dep; int LOG;
    FHQ(int n=0){tr.reserve(n+5); tr.push_back({}); srand(712367);}
    int lca(int a,int b){
        if(!a) return b; if(!b) return a;
        auto &U=*up; auto &D=*dep;
        if(D[a]<D[b]) swap(a,b);
        int d=D[a]-D[b]; for(int j=0;j<LOG;j++) if(d>>j&1) a=U[j][a];
        if(a==b) return a;
        for(int j=LOG-1;j>=0;j--) if(U[j][a]!=U[j][b]) a=U[j][a],b=U[j][b];
        return U[0][a];
    }
    int sz(int x){return x?tr[x].sz:0;}
    int agg(int x){return x?tr[x].agg:0;}
    void pull(int x){ if(x) tr[x].sz=1+sz(tr[x].l)+sz(tr[x].r), tr[x].agg=lca(lca(agg(tr[x].l),tr[x].city),agg(tr[x].r)); }
    int node(pair<long long,int> key,int city){tr.push_back({key,city,rand(),1,0,0,city}); return (int)tr.size()-1;}
    void splitKey(int x,pair<long long,int> key,int &a,int &b){
        if(!x){a=b=0;return;}
        if(tr[x].key<key){a=x; splitKey(tr[x].r,key,tr[x].r,b); pull(a);}
        else{b=x; splitKey(tr[x].l,key,a,tr[x].l); pull(b);}
    }
    void splitSize(int x,int k,int&a,int&b){
        if(!x){a=b=0;return;}
        if(sz(tr[x].l)>=k){b=x; splitSize(tr[x].l,k,a,tr[x].l); pull(b);}
        else{a=x; splitSize(tr[x].r,k-sz(tr[x].l)-1,tr[x].r,b); pull(a);}
    }
    int merge(int a,int b){
        if(!a||!b) return a?a:b;
        if(tr[a].prio<tr[b].prio){tr[a].r=merge(tr[a].r,b); pull(a); return a;}
        tr[b].l=merge(a,tr[b].l); pull(b); return b;
    }
    void insert(int &root,pair<long long,int> key,int city){int a,b; splitKey(root,key,a,b); root=merge(merge(a,node(key,city)),b);}
    void erase(int &root,pair<long long,int> key){int a,b,c; splitKey(root,key,a,b); splitKey(b,{key.first,key.second+1},b,c); root=merge(a,c);}
    int prefixAgg(int &root,int k){int a,b; splitSize(root,k,a,b); int res=agg(a); root=merge(a,b); return res;}
};
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,m,q; if(!(cin>>n>>m>>q)) return 0;
    vector<long long> val(n+1); for(int i=1;i<=n;i++) cin>>val[i];
    vector<Edge> edges(m); for(auto &e:edges) cin>>e.u>>e.v>>e.w;
    sort(edges.begin(),edges.end(),[](auto&a,auto&b){return a.w<b.w;});
    int maxN=2*n+m+5, tot=n;
    vector<int> dsu(maxN), chL(maxN), chR(maxN); vector<long long> wt(maxN);
    iota(dsu.begin(),dsu.end(),0);
    auto find = [&](int x){
        int r=x;
        while(dsu[r]!=r) r=dsu[r];
        while(dsu[x]!=x){int p=dsu[x]; dsu[x]=r; x=p;}
        return r;
    };
    for(auto e:edges){
        int a=find(e.u), b=find(e.v); if(a==b) continue;
        ++tot; wt[tot]=e.w; chL[tot]=a; chR[tot]=b; dsu[a]=dsu[b]=dsu[tot]=tot;
    }
    int rootTree=find(1), LOG=1; while((1<<LOG)<=tot) LOG++;
    vector<vector<int>> up(LOG, vector<int>(tot+1)); vector<int> dep(tot+1);
    vector<vector<int>> tree(tot+1);
    for(int i=n+1;i<=tot;i++){tree[i].push_back(chL[i]); tree[i].push_back(chR[i]);}
    vector<int> st={rootTree}; up[0][rootTree]=rootTree;
    while(!st.empty()){
        int u=st.back(); st.pop_back();
        for(int j=1;j<LOG;j++) up[j][u]=up[j-1][up[j-1][u]];
        for(int v:tree[u]){dep[v]=dep[u]+1; up[0][v]=u; st.push_back(v);}
    }
    FHQ fhq(n+q+5); fhq.up=&up; fhq.dep=&dep; fhq.LOG=LOG;
    int treap=0;
    for(int i=1;i<=n;i++) fhq.insert(treap, {-val[i],i}, i);
    while(q--){
        int op; cin>>op;
        if(op==1){int c; long long t; cin>>c>>t; fhq.erase(treap,{-val[c],c}); val[c]=t; fhq.insert(treap,{-val[c],c},c);}
        else{int k; cin>>k; int a=fhq.prefixAgg(treap,k); cout<<wt[a]<<"\n";}
    }
}
