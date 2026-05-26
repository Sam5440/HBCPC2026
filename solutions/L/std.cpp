#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    cout.setf(ios::fixed); cout<<setprecision(12);
    int T; if(!(cin>>T)) return 0;
    const long double PI = acosl(-1.0L);
    while(T--){
        int n,k; cin>>n>>k;
        vector<pair<long double,long double>> a(n);
        for(int i=0;i<n;i++){
            long double x,y; cin>>x>>y;
            long double ang=atan2l(y,x); if(ang<0) ang += 2*PI;
            long double r2=x*x+y*y;
            a[i]={ang,r2};
        }
        if(k==1){ cout<<"0.000000000000\n"; continue; }
        sort(a.begin(),a.end());
        vector<long double> ang(2*n), r2(2*n);
        for(int i=0;i<2*n;i++){ ang[i]=a[i%n].first + (i>=n?2*PI:0); r2[i]=a[i%n].second; }
        deque<int> dq;
        long double best=1e100L;
        for(int j=0;j<2*n;j++){
            while(!dq.empty() && r2[dq.back()]<=r2[j]) dq.pop_back();
            dq.push_back(j);
            int i=j-k+1;
            if(i<0) continue;
            while(!dq.empty() && dq.front()<i) dq.pop_front();
            if(i<n){
                long double width=ang[j]-ang[i];
                best=min(best, 0.5L*width*r2[dq.front()]);
            }
        }
        cout << (double)best << "\n";
    }
}
