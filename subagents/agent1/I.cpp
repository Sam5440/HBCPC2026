#include <bits/stdc++.h>
using namespace std;
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);
 int N; long long M; if(!(cin>>N>>M)) return 0; vector<long long>t(N); for(auto &x:t)cin>>x; long long lo=0,hi=*min_element(t.begin(),t.end())*M; while(lo<hi){long long mid=(lo+hi)/2, can=0; for(long long x:t){can+=mid/x; if(can>=M)break;} if(can>=M)hi=mid;else lo=mid+1;} cout<<lo<<"\n";
}
