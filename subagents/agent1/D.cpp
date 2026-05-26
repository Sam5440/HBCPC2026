#include <bits/stdc++.h>
using namespace std;
const long long MOD=998244353, G=3;
long long modpow(long long a,long long e){long long r=1;while(e){if(e&1)r=r*a%MOD;a=a*a%MOD;e>>=1;}return r;}
void ntt(vector<long long>&a,bool inv){int n=a.size(); for(int i=1,j=0;i<n;i++){int b=n>>1; for(;j&b;b>>=1) j^=b; j^=b; if(i<j) swap(a[i],a[j]);} for(int len=2;len<=n;len<<=1){long long wlen=modpow(G,(MOD-1)/len); if(inv) wlen=modpow(wlen,MOD-2); for(int i=0;i<n;i+=len){long long w=1; for(int j=0;j<len/2;j++){long long u=a[i+j],v=a[i+j+len/2]*w%MOD; a[i+j]=(u+v)%MOD; a[i+j+len/2]=(u-v+MOD)%MOD; w=w*wlen%MOD;}}} if(inv){long long ni=modpow(n,MOD-2); for(auto &x:a)x=x*ni%MOD;}}
vector<long long> conv(vector<long long>a, vector<long long>b){int need=a.size()+b.size()-1,n=1;while(n<need)n<<=1;a.resize(n);b.resize(n);ntt(a,false);ntt(b,false);for(int i=0;i<n;i++)a[i]=a[i]*b[i]%MOD;ntt(a,true);a.resize(need);return a;}
vector<int> zfunc(const string&s){int n=s.size();vector<int>z(n);for(int i=1,l=0,r=0;i<n;i++){if(i<=r)z[i]=min(r-i+1,z[i-l]);while(i+z[i]<n&&s[z[i]]==s[i+z[i]])z[i]++;if(i+z[i]-1>r)l=i,r=i+z[i]-1;}return z;}
vector<long long> cnt(const string&s){int n=s.size();auto z=zfunc(s);vector<long long>L(n+1);for(int d=1;d<=n;d++){for(int p=d;p<=n;p+=d){if(p==d || z[d]>=p-d) L[p]++;}}return L;}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);
 int n,k; string s; if(!(cin>>n>>k>>s)) return 0;
 auto L=cnt(s); reverse(s.begin(),s.end()); auto R=cnt(s);
 if(k==0){long long ans=0; for(int p=1;p<n;p++) ans=(ans+L[p]*R[n-p])%MOD; cout<<ans<<"\n"; return 0;}
 vector<long long> fac(n+1),ifac(n+1); fac[0]=1; for(int i=1;i<=n;i++)fac[i]=fac[i-1]*i%MOD; ifac[n]=modpow(fac[n],MOD-2); for(int i=n;i;i--)ifac[i-1]=ifac[i]*i%MOD;
 auto C=[&](int N,int K)->long long{return K<0||K>N?0:fac[N]*ifac[K]%MOD*ifac[N-K]%MOD;};
 vector<long long>A(n+1),B(n+1); for(int i=1;i<=n;i++)A[i]=L[i],B[i]=R[i];
 auto P=conv(A,B); long long ans=0; for(int sum=2;sum<=n-k;sum++) ans=(ans+P[sum]*C(n-sum-1,k-1))%MOD;
 cout<<ans<<"\n";
}
