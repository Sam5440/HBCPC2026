#include <bits/stdc++.h>
using namespace std;
const int MOD=998244353, G=3;
long long modpow(long long a,long long e){long long r=1;while(e){if(e&1)r=r*a%MOD;a=a*a%MOD;e>>=1;}return r;}
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
            long long e=modpow(G,(MOD-1)>>(k+1));
            for(int i=1<<(k-1);i<(1<<k);i++){
                roots[2*i]=roots[i];
                roots[2*i+1]=roots[i]*e%MOD;
            }
            k++;
        }
    }
    for(int i=0;i<n;i++) if(i<rev[i]) swap(a[i],a[rev[i]]);
    for(int len=1;len<n;len<<=1){
        for(int i=0;i<n;i+=2*len){
            for(int j=0;j<len;j++){
                int u=a[i+j], v=(long long)a[i+j+len]*roots[len+j]%MOD;
                a[i+j]=u+v<MOD?u+v:u+v-MOD;
                a[i+j+len]=u-v>=0?u-v:u-v+MOD;
            }
        }
    }
    if(inv){
        reverse(a.begin()+1,a.end());
        long long in=modpow(n,MOD-2);
        for(int &x:a) x=x*in%MOD;
    }
}
vector<int> conv(vector<int>a, vector<int>b){
    int need=a.size()+b.size()-1, n=1; while(n<need) n<<=1;
    a.resize(n); b.resize(n); ntt(a,false); ntt(b,false);
    for(int i=0;i<n;i++) a[i]=(long long)a[i]*b[i]%MOD;
    ntt(a,true); a.resize(need); return a;
}
vector<int> zfunc(const string& s){
    int n=s.size(); vector<int> z(n);
    for(int i=1,l=0,r=0;i<n;i++){
        if(i<=r) z[i]=min(r-i+1,z[i-l]);
        while(i+z[i]<n && s[z[i]]==s[i+z[i]]) z[i]++;
        if(i+z[i]-1>r) l=i,r=i+z[i]-1;
    }
    return z;
}
vector<int> counts(const string& s){
    int n=s.size(); auto z=zfunc(s);
    vector<int> f(n+1);
    for(int d=1;d<=n;d++){
        int lim=d+(d<n?z[d]:0);
        for(int p=d;p<=lim;p+=d) f[p]++;
    }
    return f;
}
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,k; string s; if(!(cin>>n>>k>>s)) return 0;
    auto F=counts(s);
    reverse(s.begin(),s.end());
    auto Gr=counts(s);
    vector<int> Gv(n+1); for(int i=1;i<=n;i++) Gv[i]=Gr[i];
    auto H=conv(F,Gv);
    long long ans=0;
    if(k==0){
        if(n<(int)H.size()) ans=H[n];
    }else{
        vector<long long> fact(n+1), invfact(n+1);
        fact[0]=1; for(int i=1;i<=n;i++) fact[i]=fact[i-1]*i%MOD;
        invfact[n]=modpow(fact[n],MOD-2); for(int i=n;i;i--) invfact[i-1]=invfact[i]*i%MOD;
        auto C=[&](int N,int R)->long long{
            if(R<0||R>N) return 0;
            return fact[N]*invfact[R]%MOD*invfact[N-R]%MOD;
        };
        for(int sum=2;sum<=n-k && sum<(int)H.size();sum++){
            ans = (ans + (long long)H[sum]*C(n-sum-1,k-1))%MOD;
        }
    }
    cout<<ans%MOD<<"\n";
}
