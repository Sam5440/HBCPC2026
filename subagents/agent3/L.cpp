#include <bits/stdc++.h>
using namespace std;
const long double PI=acosl(-1.0L);
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; if(!(cin>>T)) return 0;
    cout.setf(ios::fixed); cout<<setprecision(12);
    while(T--){
        int n,k; cin>>n>>k; vector<pair<long double,long double>> p(n);
        for(auto &e:p){long long x,y;cin>>x>>y; long double ang=atan2l((long double)y,(long double)x); if(ang<0) ang+=2*PI; e={ang,(long double)x*x+(long double)y*y};}
        sort(p.begin(),p.end());
        vector<pair<long double,long double>> a=p; for(auto e:p) a.push_back({e.first+2*PI,e.second});
        long double ans=1e100L;
        deque<int> dq;
        for(int i=0;i<2*n;i++){
            while(!dq.empty() && a[dq.back()].second<=a[i].second) dq.pop_back();
            dq.push_back(i);
            if(i>=k-1){
                int l=i-k+1; while(!dq.empty() && dq.front()<l) dq.pop_front();
                if(l<n){ long double ang=a[i].first-a[l].first; ans=min(ans,0.5L*ang*a[dq.front()].second); }
            }
        }
        cout<<(double)ans<<"\n";
    }
}
