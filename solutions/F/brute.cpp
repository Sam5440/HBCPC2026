#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    string s; cin>>s;
    long long ans=0; for(char c:s) if(c=='1') ans++;
    cout<<ans<<"\n";
}
