#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    vector<vector<int>> rows;
    for(int d=1;d<n;d++){
        for(int r=1;r<=d;r++){
            vector<int> v; v.push_back(1);
            for(int x=r; x<=n; x+=d) if(x!=1 && x!=n) v.push_back(x);
            if(v.back()!=n) v.push_back(n);
            sort(v.begin(),v.end()); v.erase(unique(v.begin(),v.end()),v.end());
            bool useful=false; for(int i=1;i<(int)v.size();i++) if(v[i]-v[i-1]==d) useful=true;
            if(useful) rows.push_back(v);
        }
    }
    cout<<rows.size()<<"\n";
    for(auto &v:rows){ for(int i=0;i<(int)v.size();i++){ if(i) cout<<' '; cout<<v[i]; } cout<<"\n"; }
}
