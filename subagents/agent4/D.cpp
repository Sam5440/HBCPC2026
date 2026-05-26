#include <bits/stdc++.h>
using namespace std;
const int MOD=998244353, G=3;
long long modpow(long long a,long long e){long long r=1;while(e){if(e&1)r=r*a%MOD;a=a*a%MOD;e>>=1;}return r;}
void ntt(vector<int>& a,bool inv){
    int n=a.size();
    for(int i=1,j=0;i<n;i++){int bit=n>>1;for(;j&bit;bit>>=1)j^=bit;j^=bit;if(i<j)swap(a[i],a[j]);}
    for(int len=2;len<=n;len<<=1){
        int wlen=modpow(G,(MOD-1)/len); if(inv) wlen=modpow(wlen,MOD-2);
        for(int i=0;i<n;i+=len){long long w=1;for(int j=0;j<len/2;j++){int u=a[i+j],v=w*a[i+j+len/2]%MOD; a[i+j]=(u+v)%MOD; a[i+j+len/2]=(u-v+MOD)%MOD; w=w*wlen%MOD;}}
    }
    if(inv){long long ni=modpow(n,MOD-2); for(int &x:a)x=ni*x%MOD;}
}
vector<int> zfunc(const string&s){
    int n=s.size(); vector<int> z(n); int l=0,r=0; z[0]=n;
    for(int i=1;i<n;i++){ if(i<=r) z[i]=min(r-i+1,z[i-l]); while(i+z[i]<n&&s[z[i]]==s[i+z[i]])z[i]++; if(i+z[i]-1>r)l=i,r=i+z[i]-1; }
    return z;
}
vector<int> ways_period_prefix(const string&s){
    int n=s.size(); auto z=zfunc(s); vector<int>w(n+1);
    for(int d=1;d<=n;d++){
        int lim=d+(d<n?z[d]:0);
        for(int p=d;p<=lim;p+=d) w[p]++;
    }
    return w;
}
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,k; string s; if(!(cin>>n>>k>>s)) return 0;
    auto pref=ways_period_prefix(s);
    reverse(s.begin(),s.end());
    auto suff=ways_period_prefix(s);
    vector<int> fact(n+1), ifact(n+1); fact[0]=1;
    for(int i=1;i<=n;i++) fact[i]=1LL*fact[i-1]*i%MOD;
    ifact[n]=modpow(fact[n],MOD-2); for(int i=n;i;i--) ifact[i-1]=1LL*ifact[i]*i%MOD;
    auto C=[&](int N,int K)->int{ if(K<0||K>N) return 0; return 1LL*fact[N]*ifact[K]%MOD*ifact[N-K]%MOD; };
    if(k==0){
        long long ans=0;
        for(int p=1;p<n;p++) ans=(ans+1LL*pref[p]*suff[n-p])%MOD;
        cout<<ans<<"\n"; return 0;
    }
    int sz=1; while(sz<=2*n) sz<<=1;
    vector<int>a(sz),b(sz);
    for(int i=1;i<=n;i++) a[i]=pref[i], b[i]=suff[i];
    ntt(a,false); ntt(b,false); for(int i=0;i<sz;i++) a[i]=1LL*a[i]*b[i]%MOD; ntt(a,true);
    long long ans=0;
    for(int sum=2;sum<=n-k;sum++){
        ans = (ans + 1LL*a[sum]*C(n-sum-1,k-1))%MOD;
    }
    cout<<ans<<"\n";
}
