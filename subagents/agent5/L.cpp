#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; if(!(cin>>T)) return 0;
    cout.setf(ios::fixed); cout<<setprecision(12);
    const long double PI=acosl(-1.0L);
    while(T--){
        int n,k; cin>>n>>k;
        vector<pair<long double,long double>> p(n);
        for(int i=0;i<n;i++){
            long double x,y; cin>>x>>y;
            long double ang=atan2l(y,x); if(ang<0) ang+=2*PI;
            long double r2=x*x+y*y;
            p[i]={ang,r2};
        }
        if(k==1){ cout<<"0.000000000000\n"; continue; }
        sort(p.begin(),p.end());
        vector<long double> ang(2*n), r2(2*n);
        for(int i=0;i<2*n;i++){ ang[i]=p[i%n].first+(i>=n?2*PI:0); r2[i]=p[i%n].second; }
        deque<int> dq;
        long double ans=1e100L;
        for(int i=0;i<2*n;i++){
            while(!dq.empty() && r2[dq.back()]<=r2[i]) dq.pop_back();
            dq.push_back(i);
            int l=i-k+1;
            while(!dq.empty() && dq.front()<l) dq.pop_front();
            if(l>=0 && l<n){
                long double theta=ang[i]-ang[l];
                long double rr=r2[dq.front()];
                ans=min(ans, 0.5L*theta*rr);
            }
        }
        cout<<(double)ans<<"\n";
    }
    return 0;
}
