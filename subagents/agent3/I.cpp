#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int N; long long M; if(!(cin>>N>>M)) return 0;
    vector<int> t(N); int mn=1e9; for(int&i:t){cin>>i; mn=min(mn,i);}
    long long lo=0, hi=mn*M;
    while(lo<hi){long long mid=(lo+hi)/2, s=0; for(int x:t){s+=mid/x; if(s>=M) break;} if(s>=M) hi=mid; else lo=mid+1;}
    cout<<lo<<"\n";
}
