#include <bits/stdc++.h>
using namespace std;
const int MOD=998244353, G=3;
using ll=long long;

int modpow(long long a,long long e){ long long r=1; while(e){ if(e&1) r=r*a%MOD; a=a*a%MOD; e>>=1;} return (int)r; }
void ntt(vector<int>& a,bool inv){
    int n=a.size();
    static vector<int> rev;
    static vector<int> roots{0,1};
    if((int)rev.size()!=n){
        int k=__builtin_ctz(n);
        rev.assign(n,0);
        for(int i=0;i<n;i++) rev[i]=(rev[i>>1]>>1)|((i&1)<<(k-1));
    }
    if((int)roots.size()<n){
        int k=__builtin_ctz(roots.size());
        roots.resize(n);
        while((1<<k)<n){
            int e=modpow(G,(MOD-1)>>(k+1));
            for(int i=1<<(k-1);i<(1<<k);i++){
                roots[2*i]=roots[i];
                roots[2*i+1]=(ll)roots[i]*e%MOD;
            }
            k++;
        }
    }
    for(int i=0;i<n;i++) if(i<rev[i]) swap(a[i],a[rev[i]]);
    for(int len=1;len<n;len<<=1){
        for(int i=0;i<n;i+=2*len){
            for(int j=0;j<len;j++){
                int u=a[i+j], v=(ll)a[i+j+len]*roots[len+j]%MOD;
                a[i+j]=u+v<MOD?u+v:u+v-MOD;
                a[i+j+len]=u-v>=0?u-v:u-v+MOD;
            }
        }
    }
    if(inv){
        reverse(a.begin()+1,a.end());
        int in=modpow(n,MOD-2);
        for(int &x:a) x=(ll)x*in%MOD;
    }
}
vector<int> conv(vector<int>a, vector<int>b){
    int need=a.size()+b.size()-1, n=1; while(n<need) n<<=1;
    a.resize(n); b.resize(n);
    ntt(a,false); ntt(b,false);
    for(int i=0;i<n;i++) a[i]=(ll)a[i]*b[i]%MOD;
    ntt(a,true); a.resize(need); return a;
}
vector<int> pi_func(const string& s){
    int n=s.size(); vector<int> pi(n);
    for(int i=1;i<n;i++){ int j=pi[i-1]; while(j&&s[i]!=s[j]) j=pi[j-1]; if(s[i]==s[j]) j++; pi[i]=j; }
    return pi;
}
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,k; string s; if(!(cin>>n>>k>>s)) return 0;
    vector<int> fac(n+1), ifac(n+1); fac[0]=1;
    for(int i=1;i<=n;i++) fac[i]=(ll)fac[i-1]*i%MOD;
    ifac[n]=modpow(fac[n],MOD-2); for(int i=n;i;i--) ifac[i-1]=(ll)ifac[i]*i%MOD;
    auto C=[&](int N,int K)->int{ if(K<0||K>N) return 0; return (ll)fac[N]*ifac[K]%MOD*ifac[N-K]%MOD; };
    auto get=[&](string t){
        auto pi=pi_func(t);
        vector<int> res(n+1);
        for(int L=1;L<=n;L++){
            int p=L-pi[L-1];
            if(L%p) p=L;
            int x=L/p, cnt=0;
            for(int d=1; (ll)d*d<=x; d++) if(x%d==0){ cnt++; if(d*d!=x) cnt++; }
            res[L]=cnt;
        }
        return res;
    };
    auto P=get(s); reverse(s.begin(),s.end()); auto Q=get(s);
    vector<int>a(n+1),b(n+1);
    for(int i=1;i<=n;i++) a[i]=P[i], b[i]=Q[i];
    auto cv=conv(a,b);
    long long ans=0;
    if(k==0){
        if(n<(int)cv.size()) ans=cv[n];
    }else{
        for(int sum=2; sum<=n-k && sum<(int)cv.size(); sum++){
            ans = (ans + (ll)cv[sum]*C(n-sum-1,k-1))%MOD;
        }
    }
    cout<<ans%MOD<<"\n";
    return 0;
}
