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
