#include <bits/stdc++.h>
using namespace std;
const int MOD=998244353, G=3;
long long modpow(long long a,long long e){long long r=1;while(e){if(e&1)r=r*a%MOD;a=a*a%MOD;e>>=1;}return r;}
void ntt(vector<int>& a,bool inv){
    int n=a.size();
    for(int i=1,j=0;i<n;i++){int bit=n>>1;for(;j&bit;bit>>=1)j^=bit;j^=bit;if(i<j)swap(a[i],a[j]);}
    for(int len=2;len<=n;len<<=1){
        int wlen=modpow(G,(MOD-1)/len); if(inv) wlen=modpow(wlen,MOD-2);
        for(int i=0;i<n;i+=len){long long w=1;for(int j=0;j<len/2;j++){int u=a[i+j],v=w*a[i+j+len/2]%MOD;a[i+j]=(u+v)%MOD;a[i+j+len/2]=(u-v+MOD)%MOD;w=w*wlen%MOD;}}
    }
    if(inv){long long ninv=modpow(n,MOD-2);for(int &x:a)x=x*ninv%MOD;}
}
vector<int> multiply(vector<int>a,vector<int>b){
    int n=1, need=a.size()+b.size()-1; while(n<need)n<<=1; a.resize(n);b.resize(n);ntt(a,false);ntt(b,false);for(int i=0;i<n;i++)a[i]=(long long)a[i]*b[i]%MOD;ntt(a,true);a.resize(need);return a;
}
vector<int> prefix_function(const string&s){
    int n=s.size(); vector<int> pi(n);
    for(int i=1;i<n;i++){int j=pi[i-1];while(j&&s[i]!=s[j])j=pi[j-1];if(s[i]==s[j])j++;pi[i]=j;}return pi;
}
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,k; string s; if(!(cin>>n>>k>>s)) return 0;
    vector<int> divcnt(n+1,0); for(int i=1;i<=n;i++) for(int j=i;j<=n;j+=i) divcnt[j]++;
    auto calc=[&](string t){
        auto pi=prefix_function(t); vector<int>w(n+1);
        for(int len=1;len<=n;len++){int p=len-pi[len-1]; int mp=(len%p==0?p:len); w[len]=divcnt[len/mp];}
        return w;
    };
    vector<int> pre=calc(s); reverse(s.begin(),s.end()); vector<int> suf=calc(s);
    vector<int>A(n+1),B(n+1); for(int i=1;i<=n;i++) A[i]=pre[i],B[i]=suf[i];
    auto conv=multiply(A,B);
    long long ans=0;
    if(k==0){ if(n<(int)conv.size()) ans=conv[n]; }
    else{
        vector<int> fact(n+1),invfact(n+1); fact[0]=1; for(int i=1;i<=n;i++) fact[i]=(long long)fact[i-1]*i%MOD;
        invfact[n]=modpow(fact[n],MOD-2); for(int i=n;i;i--) invfact[i-1]=(long long)invfact[i]*i%MOD;
        auto C=[&](int N,int R)->int{ if(R<0||R>N) return 0; return (long long)fact[N]*invfact[R]%MOD*invfact[N-R]%MOD; };
        for(int sum=2;sum<=n-k;sum++) if(sum<(int)conv.size()) ans=(ans+(long long)conv[sum]*C(n-sum-1,k-1))%MOD;
    }
    cout<<ans%MOD<<"\n";
}
