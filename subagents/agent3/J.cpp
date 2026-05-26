#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int N; long long M; if(!(cin>>N>>M)) return 0;
    long long best=-1; int bi=1;
    for(int i=1;i<=N;i++){
        long long A,B; cin>>A>>B; long long cur;
        if(B>=12*A) cur=M/A;
        else{ long long q=M/B, rem=M%B; cur=q*12+rem/A; if(q>0) cur=max(cur,(q-1)*12+(rem+B)/A); }
        if(cur>best){best=cur;bi=i;}
    }
    cout<<best<<" "<<bi<<"\n";
}
