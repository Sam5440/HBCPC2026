#include <bits/stdc++.h>
using namespace std;
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);
 int N; long long M; if(!(cin>>N>>M)) return 0; long long best=-1; int bi=1;
 for(int i=1;i<=N;i++){long long A,B;cin>>A>>B; long long val=0; if(B<12*A){long long d=M/B; val=d*12+(M-d*B)/A; for(long long dd=max(0LL,d-20);dd<=d;dd++) val=max(val, dd*12+(M-dd*B)/A);} else val=M/A; if(val>best){best=val;bi=i;}}
 cout<<best<<" "<<bi<<"\n";
}
