#include <bits/stdc++.h>
using namespace std;
const long double PI=acos((long double)-1);
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; if(!(cin>>T)) return 0;
    cout.setf(ios::fixed); cout<<setprecision(12);
    while(T--){
        int n,k; cin>>n>>k;
        vector<pair<long double,long double>> p(n);
        for(auto &e:p){long double x,y;cin>>x>>y; e={atan2(y,x), x*x+y*y}; if(e.first<0)e.first+=2*PI;}
        sort(p.begin(),p.end());
        vector<long double> ang(2*n), rr(2*n);
        for(int i=0;i<n;i++){
            ang[i]=p[i].first; rr[i]=p[i].second;
            ang[i+n]=p[i].first+2*PI; rr[i+n]=p[i].second;
        }
        long double ans=1e100;
        deque<int> dq;
        for(int i=0;i<2*n;i++){
            while(!dq.empty() && rr[dq.back()]<=rr[i]) dq.pop_back();
            dq.push_back(i);
            while(!dq.empty() && dq.front()<=i-k) dq.pop_front();
            int l=i-k+1;
            if(l>=0 && l<n) ans=min(ans, (ang[i]-ang[l])*rr[dq.front()]/2);
        }
        cout<<(double)ans<<"\n";
    }
}
