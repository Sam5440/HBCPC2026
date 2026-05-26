#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int N; long long M; if(!(cin>>N>>M)) return 0;
    long long best=-1; int besti=1;
    for(int i=1;i<=N;i++){
        long long A,B; cin>>A>>B;
        long long cur=0;
        long long mx=M/B;
        for(long long d=0; d<=20; d++){
            long long x=mx>=d?mx-d:0;
            cur=max(cur, 12*x + (M-B*x)/A);
        }
        cur=max(cur, M/A);
        if(cur>best){ best=cur; besti=i; }
    }
    cout<<best<<" "<<besti<<"\n";
    return 0;
}
