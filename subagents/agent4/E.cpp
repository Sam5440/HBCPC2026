#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    vector<vector<int>> rows;
    for(int l=1;l<n;l++) for(int r=l+1;r<=n;r++){
        vector<int> v={1};
        if(l!=1) v.push_back(l);
        if(r!=n) v.push_back(r);
        v.push_back(n);
        sort(v.begin(),v.end()); v.erase(unique(v.begin(),v.end()),v.end());
        rows.push_back(v);
    }
    cout<<rows.size()<<"\n";
    for(auto &v: rows){ for(int i=0;i<(int)v.size();i++){ if(i) cout<<' '; cout<<v[i]; } cout<<"\n"; }
}
