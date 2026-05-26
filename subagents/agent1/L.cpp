#include <bits/stdc++.h>
using namespace std;
const long double PI=acosl(-1.0L);
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);
 int T; if(!(cin>>T)) return 0; cout.setf(ios::fixed); cout<<setprecision(12);
 while(T--){int n,k;cin>>n>>k; vector<pair<long double,long double>> p(n); for(auto &e:p){long double x,y;cin>>x>>y; e={atan2l(y,x), x*x+y*y}; if(e.first<0)e.first+=2*PI;} sort(p.begin(),p.end()); vector<pair<long double,long double>> a=p; for(auto e:p)a.push_back({e.first+2*PI,e.second}); long double ans=1e100; for(int i=0;i<n;i++){long double mx=0; for(int j=i;j<i+k;j++) mx=max(mx,a[j].second); long double ang=a[i+k-1].first-a[i].first; ans=min(ans, 0.5L*mx*ang);} cout<<(double)ans<<"\n"; }
}
