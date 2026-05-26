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
