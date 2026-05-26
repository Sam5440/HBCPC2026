#!/usr/bin/env python3
import argparse
import json
import os
import random
import re
import shutil
import string
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LETTERS = list("ABCDEFGHIJKLM")

MANIFEST = {
    "A": {"name": "求求你不要再摔馍片了", "type": "normal", "time_limit": 2.0, "memory_limit_mb": 256},
    "B": {"name": "一句祝贺", "type": "normal", "time_limit": 1.0, "memory_limit_mb": 128},
    "C": {"name": "世界树", "type": "normal", "time_limit": 4.0, "memory_limit_mb": 512},
    "D": {"name": "简单字符串题", "type": "normal", "time_limit": 4.0, "memory_limit_mb": 512},
    "E": {"name": "电梯", "type": "constructive", "time_limit": 4.0, "memory_limit_mb": 512, "validator": "checker/E/validator.cpp"},
    "F": {"name": "猜 01 序列", "type": "interactive", "time_limit": 2.0, "memory_limit_mb": 256, "interactor": "checker/F/interactor.cpp"},
    "G": {"name": "建设高铁", "type": "normal", "time_limit": 4.0, "memory_limit_mb": 512},
    "H": {"name": "可能是字符串签到题", "type": "normal", "time_limit": 3.0, "memory_limit_mb": 512},
    "I": {"name": "山海关老冰糕", "type": "normal", "time_limit": 2.0, "memory_limit_mb": 256},
    "J": {"name": "海鲜大排档点生蚝", "type": "normal", "time_limit": 2.0, "memory_limit_mb": 256},
    "K": {"name": "灯带", "type": "constructive", "time_limit": 3.0, "memory_limit_mb": 512, "validator": "checker/K/validator.cpp"},
    "L": {"name": "贪吃蛇", "type": "special_judge", "time_limit": 3.0, "memory_limit_mb": 512, "checker": "checker/L/checker.cpp"},
    "M": {"name": "拯救猫猫", "type": "special_judge", "time_limit": 3.0, "memory_limit_mb": 512, "checker": "checker/M/checker.cpp"},
}


STD = {}
BRUTE = {}
CHECKERS = {}

STD["A"] = r'''
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
static int gain(int x, int y){ return (y - x + 5) % 5; }
static int enc(int a,int b,int c,int d){ return (((a*6+b)*6+c)*6+d); }
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    vector<int>a(n);
    for(int&i:a) cin>>i;
    const ll NEG = -(1LL<<60);
    vector<ll> dp(6*6*6*6, NEG), ndp(6*6*6*6, NEG);
    dp[enc(0,0,0,0)] = 0;
    for(int v: a){
        fill(ndp.begin(), ndp.end(), NEG);
        for(int fk=0; fk<=5; ++fk) for(int lk=0; lk<=5; ++lk)
        for(int fm=0; fm<=5; ++fm) for(int lm=0; lm<=5; ++lm){
            ll cur = dp[enc(fk,lk,fm,lm)];
            if(cur==NEG) continue;
            if(fk==0) ndp[enc(v,v,fm,lm)] = max(ndp[enc(v,v,fm,lm)], cur);
            else ndp[enc(fk,v,fm,lm)] = max(ndp[enc(fk,v,fm,lm)], cur + gain(lk,v));
            if(fm==0) ndp[enc(fk,lk,v,v)] = max(ndp[enc(fk,lk,v,v)], cur);
            else ndp[enc(fk,lk,fm,v)] = max(ndp[enc(fk,lk,fm,v)], cur + gain(lm,v));
        }
        dp.swap(ndp);
    }
    ll best = 0;
    for(int fk=0; fk<=5; ++fk) for(int lk=0; lk<=5; ++lk)
    for(int fm=0; fm<=5; ++fm) for(int lm=0; lm<=5; ++lm){
        ll cur = dp[enc(fk,lk,fm,lm)];
        if(cur < 0) continue;
        if(fk && fm) cur += gain(lk,fm);
        best = max(best, cur);
    }
    cout << best + n << "\n";
}
'''

BRUTE["A"] = r'''
#include <bits/stdc++.h>
using namespace std;
static int gain(int x, int y){ return (y - x + 5) % 5; }
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    vector<int>a(n); for(int&i:a) cin>>i;
    if(n > 24) return 0;
    long long best = 0;
    for(long long mask=0; mask<(1LL<<n); ++mask){
        vector<int> b;
        for(int i=0;i<n;i++) if(!(mask>>i&1)) b.push_back(a[i]);
        for(int i=0;i<n;i++) if(mask>>i&1) b.push_back(a[i]);
        long long cur = n;
        for(int i=1;i<n;i++) cur += gain(b[i-1], b[i]);
        best = max(best, cur);
    }
    cout << best << "\n";
}
'''

STD["B"] = BRUTE["B"] = r'''
#include <bits/stdc++.h>
using namespace std;
int main(){
    cout << "Congratulations on the success of the 10th Hebei CPC and the 2026 CCPC National Invitational (Qinhuangdao)!\n";
    return 0;
}
'''

STD["C"] = r'''
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
'''

BRUTE["C"] = r'''
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
'''

STD["D"] = r'''
#include <bits/stdc++.h>
using namespace std;
const int MOD=998244353, G=3;
int modpow(long long a,long long e){long long r=1;while(e){if(e&1)r=r*a%MOD;a=a*a%MOD;e>>=1;}return (int)r;}
void ntt(vector<int>& a,bool inv){
    int n=a.size();
    for(int i=1,j=0;i<n;i++){int bit=n>>1;for(;j&bit;bit>>=1)j^=bit;j^=bit;if(i<j)swap(a[i],a[j]);}
    for(int len=2;len<=n;len<<=1){
        int wlen=modpow(G,(MOD-1)/len); if(inv) wlen=modpow(wlen,MOD-2);
        for(int i=0;i<n;i+=len){
            long long w=1;
            for(int j=0;j<len/2;j++){
                int u=a[i+j], v=(int)(a[i+j+len/2]*w%MOD);
                a[i+j]=u+v<MOD?u+v:u+v-MOD;
                a[i+j+len/2]=u-v>=0?u-v:u-v+MOD;
                w=w*wlen%MOD;
            }
        }
    }
    if(inv){int ninv=modpow(n,MOD-2); for(int&x:a)x=(int)((long long)x*ninv%MOD);}
}
vector<int> conv(vector<int>a, vector<int>b){
    int need=a.size()+b.size()-1, n=1; while(n<need)n<<=1; a.resize(n); b.resize(n);
    ntt(a,false); ntt(b,false); for(int i=0;i<n;i++) a[i]=(long long)a[i]*b[i]%MOD; ntt(a,true); a.resize(need); return a;
}
vector<int> zfunc(const string&s){
    int n=s.size(); vector<int>z(n); z[0]=n;
    for(int i=1,l=0,r=0;i<n;i++){
        if(i<=r) z[i]=min(r-i+1,z[i-l]);
        while(i+z[i]<n && s[z[i]]==s[i+z[i]]) z[i]++;
        if(i+z[i]-1>r) l=i,r=i+z[i]-1;
    }
    return z;
}
vector<int> period_counts(const string&s){
    int n=s.size(); auto z=zfunc(s); vector<int> cnt(n+1);
    for(int len=1; len<=n; ++len){
        int lim = len==n ? n : min(n, len + z[len]);
        for(int p=len; p<=lim; p+=len) cnt[p]++;
    }
    return cnt;
}
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,k; string s; if(!(cin>>n>>k>>s)) return 0;
    vector<int> pref=period_counts(s);
    reverse(s.begin(),s.end());
    vector<int> suf=period_counts(s);
    vector<int> h=conv(pref,suf);
    vector<int> fact(n+1), ifact(n+1); fact[0]=1;
    for(int i=1;i<=n;i++) fact[i]=(long long)fact[i-1]*i%MOD;
    ifact[n]=modpow(fact[n],MOD-2);
    for(int i=n;i>=1;i--) ifact[i-1]=(long long)ifact[i]*i%MOD;
    auto C=[&](int N,int K)->int{ if(K<0||K>N) return 0; return (long long)fact[N]*ifact[K]%MOD*ifact[N-K]%MOD; };
    long long ans=0;
    if(k==0){
        if(n<(int)h.size()) ans=h[n];
    }else{
        for(int t=2; t<=n-k && t<(int)h.size(); ++t){
            ans = (ans + (long long)h[t] * C(n-t-1,k-1)) % MOD;
        }
    }
    cout << ans % MOD << "\n";
}
'''

BRUTE["D"] = r'''
#include <bits/stdc++.h>
using namespace std; const int MOD=998244353;
bool periodic(const string&s,int start,int len,int base){
    for(int i=0;i<len;i++) if(s[start+i]!=s[start+i%base]) return false;
    return true;
}
long long Csmall(int n,int k){ if(k<0||k>n)return 0; long long r=1; for(int i=1;i<=k;i++) r=r*(n-k+i)/i; return r%MOD; }
int main(){
    ios::sync_with_stdio(false);cin.tie(nullptr);
    int n,k; string s; if(!(cin>>n>>k>>s)) return 0;
    vector<int> pc(n+1), sc(n+1);
    for(int p=1;p<=n;p++) for(int a=1;a<=p;a++) if(p%a==0 && periodic(s,0,p,a)) pc[p]++;
    string rs=s; reverse(rs.begin(),rs.end());
    for(int p=1;p<=n;p++) for(int a=1;a<=p;a++) if(p%a==0 && periodic(rs,0,p,a)) sc[p]++;
    long long ans=0;
    for(int p=1;p<n;p++) for(int q=1;p+q<=n;q++){
        int mid=n-p-q;
        if(k==0){ if(mid==0) ans=(ans+(long long)pc[p]*sc[q])%MOD; }
        else if(mid>=k) ans=(ans+(long long)pc[p]*sc[q]%MOD*Csmall(mid-1,k-1))%MOD;
    }
    cout<<ans%MOD<<"\n";
}
'''

STD["E"] = BRUTE["E"] = r'''
#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    vector<vector<pair<int,int>>> byColor;
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>> pq;
    for(int l=1;l<=n;l++){
        for(int r=l+1;r<=n;r++){
            int c;
            if(!pq.empty() && pq.top().first<=l){
                c=pq.top().second; pq.pop();
            }else{
                c=byColor.size(); byColor.push_back({});
            }
            byColor[c].push_back({l,r});
            pq.push({r,c});
        }
    }
    cout << byColor.size() << "\n";
    for(auto &vec: byColor){
        vector<int> stops; stops.push_back(1);
        for(auto [l,r]: vec){
            if(stops.back()!=l) stops.push_back(l);
            if(stops.back()!=r) stops.push_back(r);
        }
        if(stops.back()!=n) stops.push_back(n);
        for(size_t i=0;i<stops.size();++i){ if(i) cout << ' '; cout << stops[i]; }
        cout << "\n";
    }
}
'''

STD["F"] = r'''
#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    vector<long long> res;
    for(int b=0;b<17;b++){
        vector<int> pos;
        for(int i=1;i<=n;i++) if((i>>b)&1) pos.push_back(i);
        if(pos.empty()) pos.push_back(1);
        cout << "? " << pos.size();
        for(int x:pos) cout << ' ' << x;
        cout << endl;
        long long v; if(!(cin>>v)) return 0;
        res.push_back(v);
    }
    int answer=1;
    for(int s=1;s<=n;s++){
        bool ok=true;
        for(long long p:res){
            long long d=1LL*s*s-4*p;
            if(d<0){ok=false;break;}
            long long rt=sqrt((long double)d);
            while(rt*rt<d) rt++;
            while(rt*rt>d) rt--;
            if(rt*rt!=d || ((s+rt)&1)){ok=false;break;}
        }
        if(ok){answer=s;break;}
    }
    cout << "! " << answer << endl;
}
'''

BRUTE["F"] = r'''
#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    string s; cin>>s;
    long long ans=0; for(char c:s) if(c=='1') ans++;
    cout<<ans<<"\n";
}
'''

STD["G"] = r'''
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
        if(k<n) nth_element(id.begin(), id.begin()+k, id.end(), [&](int x,int y){ if(a[x]!=a[y]) return a[x]>a[y]; return x<y; });
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
'''

BRUTE["G"] = STD["G"]

STD["H"] = r'''
#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,q; if(!(cin>>n>>q)) return 0;
    string s; cin>>s;
    vector<array<int,26>> pref(n+1);
    pref[0].fill(0);
    for(int i=1;i<=n;i++){ pref[i]=pref[i-1]; pref[i][s[i-1]-'a']++; }
    while(q--){
        int l,r; cin>>l>>r; int ans=0;
        for(int c=0;c<26;c++) ans=max(ans, pref[r][c]-pref[l-1][c]);
        cout<<ans<<"\n";
    }
}
'''

BRUTE["H"] = r'''
#include <bits/stdc++.h>
using namespace std;
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n,q;if(!(cin>>n>>q))return 0;string s;cin>>s;while(q--){int l,r;cin>>l>>r;int cnt[26]={0};for(int i=l-1;i<r;i++)cnt[s[i]-'a']++;cout<<*max_element(cnt,cnt+26)<<"\n";}}
'''

STD["I"] = BRUTE["I"] = r'''
#include <bits/stdc++.h>
using namespace std; using ll=long long;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; ll m; if(!(cin>>n>>m)) return 0;
    vector<int> t(n); for(int&i:t) cin>>i;
    ll lo=0, hi=*min_element(t.begin(),t.end())*m;
    while(lo<hi){
        ll mid=(lo+hi)/2, made=0;
        for(int x:t){ made += mid/x; if(made>=m) break; }
        if(made>=m) hi=mid; else lo=mid+1;
    }
    cout<<lo<<"\n";
}
'''

STD["J"] = r'''
#include <bits/stdc++.h>
using namespace std; using ll=long long;
ll best(ll A,ll B,ll M){
    if(B>=12*A) return M/A;
    ll d=M/B, rem=M-d*B;
    ll ans=12*d+rem/A;
    if(d>0) ans=max(ans,12*(d-1)+(rem+B)/A);
    return ans;
}
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; ll M; if(!(cin>>n>>M)) return 0;
    ll bestCnt=-1; int bestId=1;
    for(int i=1;i<=n;i++){
        ll A,B; cin>>A>>B; ll cur=best(A,B,M);
        if(cur>bestCnt){bestCnt=cur; bestId=i;}
    }
    cout<<bestCnt<<" "<<bestId<<"\n";
}
'''

BRUTE["J"] = r'''
#include <bits/stdc++.h>
using namespace std; using ll=long long;
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n;ll M;if(!(cin>>n>>M))return 0;ll bc=-1;int bi=1;for(int i=1;i<=n;i++){ll A,B;cin>>A>>B;ll cur=0;for(ll d=0;d*B<=M && d<=100000;d++)cur=max(cur,12*d+(M-d*B)/A); if(cur>bc){bc=cur;bi=i;}}cout<<bc<<" "<<bi<<"\n";}
'''

STD["K"] = r'''
#include <bits/stdc++.h>
using namespace std;
int id(char c){ return c=='R'?0:c=='G'?1:2; }
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; if(!(cin>>T)) return 0;
    const char ch[3]={'R','G','B'};
    while(T--){
        int n,m; array<int,3> rem; cin>>n>>m>>rem[0]>>rem[1]>>rem[2];
        vector<pair<int,int>> seg(m);
        vector<char> ans(n,'?');
        for(auto &p:seg){cin>>p.first>>p.second; --p.first; --p.second;}
        bool ok=true;
        for(auto [l,r]:seg){
            int len=r-l+1;
            vector<pair<pair<int,int>, pair<int,int>>> cand;
            for(int a=0;a<3;a++) for(int b=a+1;b<3;b++){
                if(rem[a]+rem[b]>=len){
                    cand.push_back({{rem[a]+rem[b], max(rem[a], rem[b])}, {a,b}});
                }
            }
            if(cand.empty()){ok=false;break;}
            sort(cand.begin(), cand.end());
            vector<int> use={cand[0].second.first, cand[0].second.second};
            sort(use.begin(),use.end(),[&](int a,int b){return rem[a]<rem[b];});
            for(int i=l;i<=r;i++){
                int c = rem[use[0]]>0 ? use[0] : use[1];
                ans[i]=ch[c]; rem[c]--;
            }
        }
        if(ok){
            for(int i=0;i<n;i++) if(ans[i]=='?'){
                int c=max_element(rem.begin(),rem.end())-rem.begin();
                if(rem[c]<=0){ok=false;break;}
                ans[i]=ch[c]; rem[c]--;
            }
        }
        for(int c=0;c<3;c++) if(rem[c]!=0) ok=false;
        if(ok){
            for(auto [l,r]:seg){
                set<char> s;
                for(int i=l;i<=r;i++) s.insert(ans[i]);
                if(s.size()>2) ok=false;
            }
        }
        if(!ok) cout << -1 << "\n";
        else { for(char c:ans) cout<<c; cout<<"\n"; }
    }
}
'''

BRUTE["K"] = STD["K"]

STD["L"] = BRUTE["L"] = r'''
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
struct Group{ long double ang,r2; int cnt; };
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    cout.setf(ios::fixed); cout<<setprecision(12);
    int T; if(!(cin>>T)) return 0;
    const long double PI = acosl(-1.0L);
    while(T--){
        int n,k; cin>>n>>k;
        map<pair<ll,ll>, Group> mp;
        for(int i=0;i<n;i++){
            ll x,y; cin>>x>>y;
            ll g=std::gcd(llabs(x), llabs(y));
            pair<ll,ll> key={x/g,y/g};
            long double ang=atan2l((long double)y,(long double)x); if(ang<0) ang += 2*PI;
            long double r2=(long double)x*x+(long double)y*y;
            auto &grp=mp[key];
            if(grp.cnt==0){ grp.ang=ang; grp.r2=r2; }
            else grp.r2=max(grp.r2,r2);
            grp.cnt++;
        }
        vector<Group> a; for(auto &kv:mp) a.push_back(kv.second);
        sort(a.begin(),a.end(),[](const Group&x,const Group&y){return x.ang<y.ang;});
        int g=a.size(), r=0, have=0;
        deque<int> dq;
        long double best=1e100L;
        auto angle_at=[&](int idx){return a[idx%g].ang + (idx>=g?2*PI:0);};
        auto r2_at=[&](int idx){return a[idx%g].r2;};
        auto cnt_at=[&](int idx){return a[idx%g].cnt;};
        for(int l=0;l<g;l++){
            if(r<l) r=l;
            while(r<l+g && have<k){
                while(!dq.empty() && r2_at(dq.back())<=r2_at(r)) dq.pop_back();
                dq.push_back(r);
                have += cnt_at(r);
                r++;
            }
            if(have>=k){
                long double width=angle_at(r-1)-angle_at(l);
                best=min(best, 0.5L*width*r2_at(dq.front()));
            }
            if(r>l){
                have -= cnt_at(l);
                if(!dq.empty() && dq.front()==l) dq.pop_front();
            }
        }
        cout << (double)best << "\n";
    }
}
'''

STD["M"] = BRUTE["M"] = r'''
#include <bits/stdc++.h>
using namespace std;
bool dog(char c){return c=='U'||c=='D'||c=='L'||c=='R';}
int dr(char c){return c=='D'?1:c=='U'?-1:0;}
int dc(char c){return c=='R'?1:c=='L'?-1:0;}
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; if(!(cin>>T)) return 0;
    while(T--){
        int n,m; cin>>n>>m; vector<string> grid(n);
        for(auto &row:grid) cin>>row;
        vector<pair<int,int>> dogs; pair<int,int>S,E;
        for(int i=0;i<n;i++)for(int j=0;j<m;j++){
            if(dog(grid[i][j])) dogs.push_back({i,j});
            if(grid[i][j]=='S') S={i,j};
            if(grid[i][j]=='E') E={i,j};
        }
        auto can=[&](int sleep)->bool{
            vector<vector<int>> seen(n, vector<int>(m,0));
            for(int idx=0; idx<(int)dogs.size(); ++idx) if(idx!=sleep){
                auto [r,c]=dogs[idx]; char d=grid[r][c]; int nr=r+dr(d), nc=c+dc(d);
                while(nr>=0&&nr<n&&nc>=0&&nc<m && grid[nr][nc]!='#' && !dog(grid[nr][nc])){
                    seen[nr][nc]++;
                    nr+=dr(d); nc+=dc(d);
                }
            }
            queue<pair<int,int>> q; vector<vector<char>> vis(n, vector<char>(m,0));
            auto freecell=[&](int r,int c){
                if(r<0||r>=n||c<0||c>=m) return false;
                if(grid[r][c]=='#'||dog(grid[r][c])||seen[r][c]) return false;
                return true;
            };
            if(!freecell(S.first,S.second)||!freecell(E.first,E.second)) return false;
            q.push(S); vis[S.first][S.second]=1;
            int rr[4]={1,-1,0,0}, cc[4]={0,0,1,-1};
            while(!q.empty()){
                auto [r,c]=q.front(); q.pop();
                if(make_pair(r,c)==E) return true;
                for(int z=0;z<4;z++){int nr=r+rr[z],nc=c+cc[z]; if(freecell(nr,nc)&&!vis[nr][nc]){vis[nr][nc]=1;q.push({nr,nc});}}
            }
            return false;
        };
        if(can(-1)){ cout<<dogs[0].first+1<<" "<<dogs[0].second+1<<"\n"; continue; }
        pair<int,int> ans={-1,-1};
        for(int i=0;i<(int)dogs.size();i++) if(can(i)){ ans={dogs[i].first+1,dogs[i].second+1}; break; }
        cout<<ans.first<<" "<<ans.second<<"\n";
    }
}
'''

CHECKERS["E/validator.cpp"] = r'''
#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){
    if(argc<3){cerr<<"usage: validator input output\n";return 2;}
    ifstream in(argv[1]), out(argv[2]);
    int n; in>>n;
    long long expected=1LL*(n/2)*(n-n/2);
    int m; if(!(out>>m)) return 1;
    if(m!=expected) return 1;
    vector<vector<char>> cov(n+1, vector<char>(n+1,0));
    long long total=0;
    string line; getline(out,line);
    for(int i=0;i<m;i++){
        if(!getline(out,line)) return 1;
        stringstream ss(line); vector<int> a; int x;
        while(ss>>x) a.push_back(x);
        if(a.size()<2 || a.front()!=1 || a.back()!=n) return 1;
        total += a.size();
        for(int j=1;j<(int)a.size();j++){
            if(a[j-1]>=a[j] || a[j]<1 || a[j]>n) return 1;
            cov[a[j-1]][a[j]]=1;
        }
    }
    if(total>2000000) return 1;
    for(int l=1;l<=n;l++) for(int r=l+1;r<=n;r++) if(!cov[l][r]) return 1;
    return 0;
}
'''

CHECKERS["F/interactor.cpp"] = r'''
#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){
    if(argc<2){cerr<<"usage: interactor data.in\n";return 2;}
    ifstream fin(argv[1]);
    int n; string s; fin>>n>>s;
    int total=0; for(char c:s) total+=c=='1';
    cerr<<"This standalone interactor expects to be connected to a contestant process via stdin/stdout.\n";
    cout<<n<<endl;
    int queries=0;
    string tag;
    while(cin>>tag){
        if(tag=="?"){
            int k; cin>>k; vector<int> used(n+1,0); int inside=0;
            for(int i=0;i<k;i++){int p;cin>>p; if(p<1||p>n||used[p]) return 1; used[p]=1; inside+=s[p-1]=='1';}
            if(++queries>17) return 1;
            cout << 1LL*inside*(total-inside) << endl;
        }else if(tag=="!"){
            int ans; cin>>ans; return ans==total?0:1;
        }else return 1;
    }
    return 1;
}
'''

CHECKERS["K/validator.cpp"] = r'''
#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){
    if(argc<3){cerr<<"usage: validator input output\n";return 2;}
    ifstream in(argv[1]), out(argv[2]);
    int T; in>>T;
    while(T--){
        int n,m,r,g,b; in>>n>>m>>r>>g>>b;
        vector<pair<int,int>> seg(m); for(auto &p:seg) in>>p.first>>p.second;
        string s; if(!(out>>s)) return 1;
        if(s=="-1") continue;
        if((int)s.size()!=n) return 1;
        int cr=0,cg=0,cb=0;
        for(char c:s){ if(c=='R')cr++; else if(c=='G')cg++; else if(c=='B')cb++; else return 1; }
        if(cr!=r||cg!=g||cb!=b) return 1;
        for(auto [l,rr]:seg){
            set<char> st; for(int i=l-1;i<=rr-1;i++) st.insert(s[i]);
            if(st.size()>2) return 1;
        }
    }
    return 0;
}
'''

CHECKERS["L/checker.cpp"] = r'''
#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){
    if(argc<4){cerr<<"usage: checker input output answer\n";return 2;}
    ifstream out(argv[2]), ans(argv[3]);
    long double a,b; 
    while(ans>>a){
        if(!(out>>b)) return 1;
        long double diff=fabsl(a-b);
        long double tol=1e-9L*max((long double)1.0, fabsl(a));
        if(diff>tol) return 1;
    }
    return 0;
}
'''

CHECKERS["M/checker.cpp"] = r'''
#include <bits/stdc++.h>
using namespace std;
bool dog(char c){return c=='U'||c=='D'||c=='L'||c=='R';}
int dr(char c){return c=='D'?1:c=='U'?-1:0;}
int dc(char c){return c=='R'?1:c=='L'?-1:0;}
bool can_sleep(const vector<string>&grid, int sleepR, int sleepC){
    int n=grid.size(), m=grid[0].size(); vector<pair<int,int>> dogs; pair<int,int>S,E;
    for(int i=0;i<n;i++)for(int j=0;j<m;j++){ if(dog(grid[i][j])) dogs.push_back({i,j}); if(grid[i][j]=='S')S={i,j}; if(grid[i][j]=='E')E={i,j}; }
    vector<vector<int>> seen(n, vector<int>(m,0));
    for(auto [r,c]:dogs) if(!(r==sleepR&&c==sleepC)){
        char d=grid[r][c]; int nr=r+dr(d), nc=c+dc(d);
        while(nr>=0&&nr<n&&nc>=0&&nc<m && grid[nr][nc]!='#' && !dog(grid[nr][nc])){ seen[nr][nc]++; nr+=dr(d); nc+=dc(d); }
    }
    auto freecell=[&](int r,int c){return r>=0&&r<n&&c>=0&&c<m&&grid[r][c]!='#'&&!dog(grid[r][c])&&!seen[r][c];};
    if(!freecell(S.first,S.second)||!freecell(E.first,E.second)) return false;
    queue<pair<int,int>> q; vector<vector<char>> vis(n, vector<char>(m,0)); q.push(S); vis[S.first][S.second]=1;
    int rr[4]={1,-1,0,0}, cc[4]={0,0,1,-1};
    while(!q.empty()){auto [r,c]=q.front();q.pop(); if(make_pair(r,c)==E)return true; for(int k=0;k<4;k++){int nr=r+rr[k],nc=c+cc[k]; if(freecell(nr,nc)&&!vis[nr][nc]){vis[nr][nc]=1;q.push({nr,nc});}}}
    return false;
}
int main(int argc,char**argv){
    if(argc<3){cerr<<"usage: checker input output\n";return 2;}
    ifstream in(argv[1]), out(argv[2]);
    int T; in>>T;
    while(T--){
        int n,m; in>>n>>m; vector<string> grid(n); for(auto &s:grid) in>>s;
        int x,y; if(!(out>>x>>y)) return 1;
        vector<pair<int,int>> dogs; for(int i=0;i<n;i++)for(int j=0;j<m;j++) if(dog(grid[i][j])) dogs.push_back({i,j});
        if(x==-1&&y==-1){
            for(auto [r,c]:dogs) if(can_sleep(grid,r,c)) return 1;
        }else{
            --x;--y; if(x<0||x>=n||y<0||y>=m||!dog(grid[x][y])) return 1;
            if(!can_sleep(grid,x,y)) return 1;
        }
    }
    return 0;
}
'''


STRESS_SCRIPT = r'''#!/usr/bin/env python3
import os
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "stress"
LETTERS = list("ABCDEGHIJKLM")

def run(cmd, inp, timeout=5):
    p = subprocess.run(cmd, input=inp.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode(errors="ignore"))
    return p.stdout.decode()

def compile_one(letter, kind):
    exe = BUILD / f"{letter}_{kind}.exe"
    src = ROOT / "solutions" / letter / f"{kind}.cpp"
    subprocess.check_call(["g++", "-std=c++17", "-O2", str(src), "-o", str(exe)])
    return exe

def gen(letter):
    if letter == "A":
        n=random.randint(1,12); a=[random.randint(1,5) for _ in range(n)]
        return f"{n}\n{' '.join(map(str,a))}\n"
    if letter == "B":
        return ""
    if letter == "C":
        n=random.randint(2,12); q=random.randint(1,20); edges=[]
        for v in range(2,n+1):
            u=random.randint(1,v-1); w=random.randint(-10,10); edges.append((u,v,w))
        qs=[(random.randint(1,n),random.randint(1,n)) for _ in range(q)]
        return f"{n} {q}\n"+"\n".join(f"{u} {v} {w}" for u,v,w in edges)+"\n"+"\n".join(f"{x} {y}" for x,y in qs)+"\n"
    if letter == "D":
        n=random.randint(2,15); k=random.randint(0,n-2); s="".join(random.choice("abc") for _ in range(n))
        return f"{n} {k} {s}\n"
    if letter == "E":
        return f"{random.randint(2,18)}\n"
    if letter == "G":
        n=random.randint(2,10); m=n-1; q=random.randint(1,12)
        a=[random.randint(1,20) for _ in range(n)]
        edges=[(i,i+1,random.randint(1,20)) for i in range(1,n)]
        ops=[]
        for _ in range(q):
            if random.random()<0.4:
                ops.append(f"1 {random.randint(1,n)} {random.randint(1,20)}")
            else:
                ops.append(f"2 {random.randint(1,n)}")
        return f"{n} {m} {q}\n{' '.join(map(str,a))}\n"+"\n".join(f"{u} {v} {d}" for u,v,d in edges)+"\n"+"\n".join(ops)+"\n"
    if letter == "H":
        n=random.randint(1,30); q=random.randint(1,20); s="".join(random.choice("abc") for _ in range(n))
        qs=[] 
        for _ in range(q):
            l=random.randint(1,n); r=random.randint(l,n); qs.append((l,r))
        return f"{n} {q}\n{s}\n"+"\n".join(f"{l} {r}" for l,r in qs)+"\n"
    if letter == "I":
        n=random.randint(1,10); m=random.randint(1,100); t=[random.randint(1,20) for _ in range(n)]
        return f"{n} {m}\n{' '.join(map(str,t))}\n"
    if letter == "J":
        n=random.randint(1,10); M=random.randint(1,200); rows=[(random.randint(1,30),random.randint(1,200)) for _ in range(n)]
        return f"{n} {M}\n"+"\n".join(f"{a} {b}" for a,b in rows)+"\n"
    if letter == "K":
        n=random.randint(3,25); cuts=sorted(random.sample(range(1,n),2)); r=random.randint(0,n); g=random.randint(0,n-r); b=n-r-g
        return f"1\n{n} 1 {r} {g} {b}\n1 {max(2,min(n-1,cuts[1]))}\n"
    if letter == "L":
        n=random.randint(1,20); k=random.randint(1,n); pts=[]
        for _ in range(n):
            x=y=0
            while x==0 and y==0: x=random.randint(-10,10); y=random.randint(-10,10)
            pts.append((x,y))
        return f"1\n{n} {k}\n"+"\n".join(f"{x} {y}" for x,y in pts)+"\n"
    if letter == "M":
        return "1\n3 3\nS..\n.R.\n..E\n"
    raise ValueError(letter)

def main():
    random.seed(20260526)
    BUILD.mkdir(parents=True, exist_ok=True)
    for letter in LETTERS:
        std=compile_one(letter,"std")
        brute=compile_one(letter,"brute")
        for case in range(50):
            inp=gen(letter)
            a=run([str(std)], inp)
            b=run([str(brute)], inp)
            if letter=="L":
                av=[float(x) for x in a.split()]
                bv=[float(x) for x in b.split()]
                if len(av)!=len(bv) or any(abs(x-y)>1e-8 for x,y in zip(av,bv)):
                    print("Mismatch", letter, case, inp, a, b); return 1
            elif a!=b:
                print("Mismatch", letter, case)
                print(inp)
                print("std:",a)
                print("brute:",b)
                return 1
        print(f"{letter}: ok")
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''


def clean_dirs():
    for name in ["problems", "data", "solutions", "checker", "build"]:
        path = ROOT / name
        if path.exists():
            shutil.rmtree(path)
    for name in ["problem_list.md", "manifest.json", "subagent_report.md"]:
        path = ROOT / name
        if path.exists():
            path.unlink()


def read_statement_file():
    raw = (ROOT / "OJ题目.md").read_bytes()
    for enc in ("utf-8-sig", "utf-16", "gb18030"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            pass
    return raw.decode("utf-8", errors="replace")


def split_problem_statements():
    source = read_statement_file()
    out = ROOT / "problems"
    out.mkdir(exist_ok=True)
    (out / "OJ题目.md").write_text(source, encoding="utf-8")
    matches = list(re.finditer(r"(?m)^## 题目 ([A-M])\. (.+)$", source))
    for i, m in enumerate(matches):
        letter = m.group(1)
        start = m.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(source)
        (out / f"{letter}.md").write_text(source[start:end].strip() + "\n", encoding="utf-8")
    lines = [
        "# 题目清单",
        "",
        "| 题号 | 题目名称 | 类型 | 关键约束 |",
        "| --- | --- | --- | --- |",
    ]
    constraints = {
        "A": "n <= 1e5, ai in [1,5]",
        "B": "无输入，固定输出",
        "C": "n,q <= 5e5, 树边权 |w| <= 1e9，可为负",
        "D": "n <= 5e5, 0 <= k <= n-2, mod 998244353",
        "E": "构造题，n <= 1000，输出停层总数 <= 2e6",
        "F": "交互题，n <= 1e5，最多 17 次询问，至少一个 1",
        "G": "n,m,q <= 5e5，动态图 top-k 连通阈值",
        "H": "n,q <= 1e6，小写字符串区间查询",
        "I": "N <= 1e5, M < 1e12, ti <= 1e6",
        "J": "N <= 1e5, M <= 1e9, Ai,Bi <= 1e5",
        "K": "构造题，多测，总 n <= 2e5，区间两两不交",
        "L": "SPJ，几何实数，sum n <= 2e5，误差 1e-9",
        "M": "SPJ/构造，网格 n,m <= 2000，多解按字典序",
    }
    type_name = {"normal":"普通题", "constructive":"构造题", "interactive":"交互题", "special_judge":"Special Judge 题"}
    for letter in LETTERS:
        item = MANIFEST[letter]
        lines.append(f"| {letter} | {item['name']} | {type_name[item['type']]} | {constraints[letter]} |")
    (ROOT / "problem_list.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (ROOT / "manifest.json").write_text(json.dumps(MANIFEST, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_sources():
    for letter in LETTERS:
        d = ROOT / "solutions" / letter
        d.mkdir(parents=True, exist_ok=True)
        (d / "std.cpp").write_text(STD[letter].lstrip(), encoding="utf-8")
        (d / "brute.cpp").write_text(BRUTE[letter].lstrip(), encoding="utf-8")
    for rel, code in CHECKERS.items():
        path = ROOT / "checker" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(code.lstrip(), encoding="utf-8")
    scripts = ROOT / "scripts"
    scripts.mkdir(exist_ok=True)
    (scripts / "stress_test.py").write_text(STRESS_SCRIPT, encoding="utf-8")


def rand_string(rng, n, alphabet="abcdefghijklmnopqrstuvwxyz"):
    return "".join(rng.choice(alphabet) for _ in range(n))


def tree_random(rng, n, wlo=-10, whi=10):
    edges = []
    for v in range(2, n+1):
        u = rng.randint(1, v-1)
        w = rng.randint(wlo, whi)
        edges.append((u, v, w))
    return edges


def gen_inputs(seed):
    rng = random.Random(seed)
    data = {x: [] for x in LETTERS}

    # A
    edges = [
        "1\n1\n", "2\n1 5\n", "5\n1 1 1 1 1\n", "5\n1 2 3 4 5\n",
        "5\n5 4 3 2 1\n", "10\n1 5 1 5 1 5 1 5 1 5\n", "7\n3 3 3 4 4 5 5\n"
    ]
    for i in range(10):
        n = rng.randint(6, 60); arr = [rng.randint(1,5) for _ in range(n)]
        data["A"].append(("regular", f"{n}\n{' '.join(map(str,arr))}\n"))
    for i in range(8):
        n = 100000
        if i == 0: arr = [1]*n
        elif i == 1: arr = [(j%5)+1 for j in range(n)]
        elif i == 2: arr = [5-(j%5) for j in range(n)]
        else: arr = [rng.randint(1,5) for _ in range(n)]
        data["A"].append(("stress", f"{n}\n{' '.join(map(str,arr))}\n"))
    data["A"].extend(("edge", x) for x in edges)

    # B
    for i in range(25): data["B"].append(("regular" if i<10 else "stress" if i<18 else "edge", ""))

    # C
    for i in range(10):
        n=rng.randint(4,35); q=rng.randint(5,40); edges=tree_random(rng,n,-20,20)
        qs=[(rng.randint(1,n), rng.randint(1,n)) for _ in range(q)]
        s=f"{n} {q}\n"+"\n".join(f"{u} {v} {w}" for u,v,w in edges)+"\n"+"\n".join(f"{x} {y}" for x,y in qs)+"\n"
        data["C"].append(("regular", s))
    for i in range(8):
        if i < 4:
            n=500000; q=5000 if i else 500000
            edges_txt="\n".join(f"{j} {j+1} {(-1 if j%3==0 else 1)*(j%1000+1)}" for j in range(1,n))
            qs=[]
            for t in range(q):
                if t%3==0: qs.append(f"1 {n}")
                elif t%3==1: qs.append(f"{n//2} {n}")
                else: qs.append(f"{rng.randint(1,n)} {rng.randint(1,n)}")
            data["C"].append(("stress", f"{n} {q}\n{edges_txt}\n"+"\n".join(qs)+"\n"))
        else:
            n=500000; q=5000
            edges_txt="\n".join(f"1 {j} {rng.randint(-1000000000,1000000000)}" for j in range(2,n+1))
            qs=[f"{rng.randint(1,n)} {rng.randint(1,n)}" for _ in range(q)]
            data["C"].append(("stress", f"{n} {q}\n{edges_txt}\n"+"\n".join(qs)+"\n"))
    c_edges = [
        "2 3\n1 2 0\n1 1\n1 2\n2 2\n",
        "3 3\n1 2 -5\n2 3 -6\n1 3\n2 2\n3 1\n",
        "4 2\n1 2 1000000000\n2 3 -1000000000\n3 4 7\n1 4\n2 3\n",
        "5 3\n1 2 1\n1 3 1\n1 4 1\n1 5 1\n2 3\n4 5\n1 1\n",
        "6 2\n1 2 -1\n2 3 -1\n3 4 -1\n4 5 -1\n5 6 -1\n1 6\n3 3\n",
        "7 2\n1 2 5\n2 3 5\n3 4 5\n4 5 5\n5 6 5\n6 7 5\n2 6\n4 4\n",
        "8 2\n1 2 1\n2 3 2\n2 4 3\n4 5 -2\n4 6 4\n1 7 -1\n7 8 9\n5 8\n3 6\n",
    ]
    data["C"].extend(("edge", x) for x in c_edges)

    # D
    for i in range(10):
        n=rng.randint(5,80); k=rng.randint(0,n-2); s=rand_string(rng,n,"abc")
        data["D"].append(("regular", f"{n} {k} {s}\n"))
    for i in range(8):
        n=500000; k=[0,1,2,10,n//3,n//2,n-3,n-2][i]
        if i==0: s="a"*n
        elif i==1: s=("ab"*(n//2+1))[:n]
        elif i==2: s=("abcde"*(n//5+1))[:n]
        else: s=rand_string(rng,n,"abcd")
        data["D"].append(("stress", f"{n} {k} {s}\n"))
    d_edge=[(2,0,"aa"),(2,0,"ab"),(3,1,"aaa"),(4,0,"aaaa"),(5,3,"abcde"),(10,0,"ababababab"),(12,5,"aaaaaaaaaaaa")]
    data["D"].extend(("edge", f"{n} {k} {s}\n") for n,k,s in d_edge)

    # E
    for i in range(10): data["E"].append(("regular", f"{rng.randint(5,60)}\n"))
    for i in range(8): data["E"].append(("stress", f"{1000-i%3}\n"))
    for n in [2,3,4,5,6,7,8]: data["E"].append(("edge", f"{n}\n"))

    # F
    def bits(n, mode):
        if mode=="one": s=["0"]*n; s[rng.randrange(n)]="1"; return "".join(s)
        if mode=="all": return "1"*n
        if mode=="alt": return "".join("1" if i%2 else "0" for i in range(n))
        return "".join("1" if rng.random()<0.35 else "0" for _ in range(n)).replace("0","1",1)
    for i in range(10):
        n=rng.randint(2,80); s=bits(n,"random")
        data["F"].append(("regular", f"{n}\n{s}\n"))
    for i in range(8):
        n=100000; s=bits(n,["one","all","alt","random"][i%4])
        data["F"].append(("stress", f"{n}\n{s}\n"))
    for n,mode in [(1,"all"),(2,"one"),(2,"all"),(3,"alt"),(10,"one"),(17,"random"),(100000,"one")]:
        s=bits(n,mode); data["F"].append(("edge", f"{n}\n{s}\n"))

    # G
    for i in range(10):
        n=rng.randint(4,12); m=n-1; q=rng.randint(8,25)
        a=[rng.randint(1,100) for _ in range(n)]
        ed=[(j,j+1,rng.randint(1,100)) for j in range(1,n)]
        ops=[]
        for _ in range(q):
            if rng.random()<0.4: ops.append(f"1 {rng.randint(1,n)} {rng.randint(1,100)}")
            else: ops.append(f"2 {rng.randint(1,n)}")
        data["G"].append(("regular", f"{n} {m} {q}\n{' '.join(map(str,a))}\n"+"\n".join(f"{u} {v} {d}" for u,v,d in ed)+"\n"+"\n".join(ops)+"\n"))
    for i in range(8):
        n=500000 if i<2 else 200000; m=n-1; q=500000 if i==0 else 5000
        a=" ".join(str((j*37)%1000000000+1) for j in range(1,n+1))
        ed="\n".join(f"{j} {j+1} {(j*97)%1000000000+1}" for j in range(1,n))
        ops=[]
        for t in range(q):
            if t%5==0: ops.append(f"1 {(t*13)%n+1} {(t*19)%1000000000+1}")
            else: ops.append("2 1")
        data["G"].append(("stress", f"{n} {m} {q}\n{a}\n{ed}\n"+"\n".join(ops)+"\n"))
    g_edge=[
        "2 1 3\n1 2\n1 2 5\n2 1\n1 1 10\n2 2\n",
        "3 2 2\n3 3 3\n1 2 1\n2 3 2\n2 2\n2 3\n",
        "4 3 2\n4 3 2 1\n1 2 4\n2 3 5\n3 4 6\n2 4\n2 1\n",
        "5 4 3\n1 1 1 1 1\n1 2 1\n2 3 1\n3 4 1\n4 5 1\n2 3\n1 5 10\n2 3\n",
        "6 5 1\n6 5 4 3 2 1\n1 2 9\n1 3 8\n1 4 7\n1 5 6\n1 6 5\n2 6\n",
        "4 3 4\n1 2 3 4\n1 2 1\n2 3 10\n3 4 100\n2 2\n1 1 1000\n2 2\n2 4\n",
        "7 6 2\n7 6 5 4 3 2 1\n1 2 1\n2 3 2\n3 4 3\n4 5 4\n5 6 5\n6 7 6\n2 5\n2 7\n",
    ]
    data["G"].extend(("edge", x) for x in g_edge)

    # H
    for i in range(10):
        n=rng.randint(5,100); q=rng.randint(10,80); s=rand_string(rng,n,"abcd")
        qs=[]; 
        for _ in range(q):
            l=rng.randint(1,n); r=rng.randint(l,n); qs.append(f"{l} {r}")
        data["H"].append(("regular", f"{n} {q}\n{s}\n"+"\n".join(qs)+"\n"))
    for i in range(8):
        n=1000000; q=1000000 if i==0 else 5000
        s=("abcdefghijklmnopqrstuvwxyz"*((n//26)+1))[:n] if i%2 else "a"*n
        qs=[f"{rng.randint(1,n)} {rng.randint(1,n)}" for _ in range(q)]
        qs=[f"{min(map(int,x.split()))} {max(map(int,x.split()))}" for x in qs]
        data["H"].append(("stress", f"{n} {q}\n{s}\n"+"\n".join(qs)+"\n"))
    h_edge=[(1,1,"a",["1 1"]),(5,3,"aaaaa",["1 5","2 4","3 3"]),(5,2,"abcde",["1 5","2 3"]),(6,2,"ababab",["1 6","2 5"]),(10,2,"zzzzzyyyyy",["1 10","6 10"]),(3,3,"abc",["1 1","2 2","3 3"]),(26,1,string.ascii_lowercase,["1 26"])]
    for n,q,s,qs in h_edge: data["H"].append(("edge", f"{n} {q}\n{s}\n"+"\n".join(qs)+"\n"))

    # I
    for i in range(10):
        n=rng.randint(1,50); m=rng.randint(1,10000); t=[rng.randint(1,100) for _ in range(n)]
        data["I"].append(("regular", f"{n} {m}\n{' '.join(map(str,t))}\n"))
    for i in range(8):
        n=100000; m=10**12-1-i; t=[rng.randint(1,1000000) for _ in range(n)]
        data["I"].append(("stress", f"{n} {m}\n{' '.join(map(str,t))}\n"))
    i_edge=[(1,1,[1]),(1,999999999999,[1000000]),(3,10,[2,3,5]),(5,1,[10,20,30,40,50]),(4,100,[1,1,1,1]),(2,999,[999999,1000000]),(10,1000,[i+1 for i in range(10)])]
    data["I"].extend(("edge", f"{n} {m}\n{' '.join(map(str,t))}\n") for n,m,t in i_edge)

    # J
    for i in range(10):
        n=rng.randint(1,80); M=rng.randint(1,100000); rows=[(rng.randint(1,1000),rng.randint(1,12000)) for _ in range(n)]
        data["J"].append(("regular", f"{n} {M}\n"+"\n".join(f"{a} {b}" for a,b in rows)+"\n"))
    for i in range(8):
        n=100000; M=1000000000-i; rows=[(rng.randint(1,100000),rng.randint(1,100000)) for _ in range(n)]
        data["J"].append(("stress", f"{n} {M}\n"+"\n".join(f"{a} {b}" for a,b in rows)+"\n"))
    j_edge=[
        (1,1,[(1,1)]),(1,11,[(2,100)]),(1,12,[(2,12)]),(2,100,[(10,200),(9,500)]),
        (3,1000,[(100,1),(1,100),(50,500)]),(2,144,[(12,144),(20,100)]),(5,999999999,[(1,100000),(100000,1),(99999,99999),(7,84),(8,95)])
    ]
    data["J"].extend(("edge", f"{n} {m}\n"+"\n".join(f"{a} {b}" for a,b in rows)+"\n") for n,m,rows in j_edge)

    # K
    def kcase(n,m,counts):
        seg=[]; cur=1
        for _ in range(m):
            length=rng.randint(2, min(5, max(2,n-cur)))
            if cur+length-1>=n: break
            seg.append((cur,cur+length-1)); cur += length + rng.randint(1,3)
            if cur>=n: break
        return f"{n} {len(seg)} {counts[0]} {counts[1]} {counts[2]}\n"+"\n".join(f"{l} {r}" for l,r in seg)+"\n"
    for i in range(10):
        n=rng.randint(5,80); r=rng.randint(0,n); g=rng.randint(0,n-r); b=n-r-g
        data["K"].append(("regular", "1\n"+kcase(n,rng.randint(1,5),(r,g,b))))
    for i in range(8):
        n=99999; r=n//3; g=n//3; b=n-r-g
        data["K"].append(("stress", "1\n"+kcase(n,20000,(r,g,b))))
    k_edges=[
        "1\n3 1 1 1 1\n1 2\n",
        "1\n4 1 1 1 2\n1 3\n",
        "1\n6 1 2 2 2\n1 5\n",
        "1\n5 2 5 0 0\n1 2\n3 4\n",
        "1\n8 1 0 4 4\n2 7\n",
        "2\n3 1 1 1 1\n1 2\n4 1 0 2 2\n1 3\n",
        "1\n10 3 3 3 4\n1 2\n4 5\n7 8\n",
    ]
    data["K"].extend(("edge", x) for x in k_edges)

    # L
    for i in range(10):
        n=rng.randint(2,80); k=rng.randint(1,n); pts=[]
        for _ in range(n):
            x=y=0
            while x==0 and y==0: x=rng.randint(-100,100); y=rng.randint(-100,100)
            pts.append((x,y))
        data["L"].append(("regular", f"1\n{n} {k}\n"+"\n".join(f"{x} {y}" for x,y in pts)+"\n"))
    for i in range(8):
        n=200000; k=1 if i==0 else rng.randint(2,n); pts=[]
        for j in range(n):
            pts.append((rng.randint(-1000000,1000000) or 1, rng.randint(-1000000,1000000) or 2))
        data["L"].append(("stress", f"1\n{n} {k}\n"+"\n".join(f"{x} {y}" for x,y in pts)+"\n"))
    l_edge=[
        "1\n1 1\n1 2\n",
        "1\n2 2\n1 0\n0 1\n",
        "1\n3 2\n0 2\n1 0\n-1 -1\n",
        "1\n4 3\n1 0\n2 0\n3 0\n0 1\n",
        "1\n5 5\n1 0\n0 1\n-1 0\n0 -1\n1 1\n",
        "1\n3 2\n1000000 0\n-1000000 0\n0 1000000\n",
        "2\n1 1\n5 5\n3 2\n1 0\n0 1\n-1 0\n",
    ]
    data["L"].extend(("edge", x) for x in l_edge)

    # M
    m_regular=[
        "1\n3 3\nS..\n.R.\n..E\n",
        "1\n4 5\nS...E\n.###.\n.R...\n.....\n",
        "1\n5 5\nS...E\n.###.\n.R.L.\n.....\n.....\n",
        "1\n3 4\nS..E\n.R..\n....\n",
        "1\n6 6\nS....E\n.####.\n.R....\n......\n....L.\n......\n",
    ]
    for i in range(10): data["M"].append(("regular", m_regular[i%len(m_regular)]))
    for i in range(8):
        if i==0:
            n=1000; m=1000
            rows=["."*m for _ in range(n)]
            rows[0]="S"+"."*(m-2)+"E"
            rows[-1]="R"+"."*(m-1)
            data["M"].append(("stress", f"1\n{n} {m}\n"+"\n".join(rows)+"\n"))
        elif i%2:
            n=2000; m=1; rows=["."]*n; rows[0]="S"; rows[-1]="E"; rows[n//2]="D"
            data["M"].append(("stress", f"1\n{n} {m}\n"+"\n".join(rows)+"\n"))
        else:
            n=1; m=2000; row=list("."*m); row[0]="S"; row[-1]="E"; row[m//2]="R"
            data["M"].append(("stress", f"1\n{n} {m}\n{''.join(row)}\n"))
    m_edges=[
        "1\n1 3\nSRE\n",
        "1\n2 2\nSE\nR.\n",
        "1\n3 3\nS#E\n.R.\n...\n",
        "1\n3 3\nS..\nR#E\n...\n",
        "1\n4 4\nS..E\n.##.\n.R..\n....\n",
        "1\n5 1\nS\n.\nD\n.\nE\n",
        "2\n3 3\nS..\n.R.\n..E\n3 3\nS#E\n.R.\n...\n",
    ]
    data["M"].extend(("edge", x) for x in m_edges)

    for letter, cases in data.items():
        assert len(cases) == 25, (letter, len(cases))
    return data


def write_inputs(seed):
    data = gen_inputs(seed)
    for letter, cases in data.items():
        d = ROOT / "data" / letter
        d.mkdir(parents=True, exist_ok=True)
        for idx, (cat, text) in enumerate(cases, 1):
            (d / f"{idx:02d}_{cat}.in").write_text(text, encoding="utf-8")


def compile_std(letter):
    out = ROOT / "build" / "std" / f"{letter}.exe"
    out.parent.mkdir(parents=True, exist_ok=True)
    src = ROOT / "solutions" / letter / "std.cpp"
    subprocess.check_call(["g++", "-std=c++17", "-O2", str(src), "-o", str(out)])
    return out


def generate_answers():
    for letter in LETTERS:
        exe = compile_std(letter)
        data_dir = ROOT / "data" / letter
        for inp in sorted(data_dir.glob("*.in")):
            ans = inp.with_suffix(".ans")
            if letter == "F":
                parts = inp.read_text(encoding="utf-8").split()
                hidden = parts[1] if len(parts) > 1 else ""
                ans.write_text(str(hidden.count("1")) + "\n", encoding="utf-8")
                continue
            p = subprocess.run([str(exe)], input=inp.read_bytes(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
            if p.returncode != 0:
                raise RuntimeError(f"{letter} failed on {inp.name}: {p.stderr.decode(errors='ignore')}")
            ans.write_bytes(p.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260526)
    ap.add_argument("--no-clean", action="store_true")
    args = ap.parse_args()
    if not args.no_clean:
        clean_dirs()
    split_problem_statements()
    write_sources()
    write_inputs(args.seed)
    generate_answers()
    print("core assets generated")


if __name__ == "__main__":
    main()
