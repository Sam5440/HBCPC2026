#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int N; long long M; if(!(cin>>N>>M)) return 0;
    long long best=-1; int idx=1;
    for(int i=1;i<=N;i++){
        long long A,B; cin>>A>>B;
        long long cur=0;
        if(B>=12*A) cur=M/A;
        else{
            long long p=M/B;
            long long st=max(0LL,p-20);
            for(long long q=st;q<=p;q++) cur=max(cur, q*12+(M-q*B)/A);
        }
        if(cur>best){best=cur; idx=i;}
    }
    cout<<best<<" "<<idx<<"\n";
}
