#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    vector<vector<int>> rows;
    if(n==2){
        rows.push_back({1,2});
    }else{
        rows.push_back({1,n});
        for(int mid=2; mid<=n-1; mid++){
            rows.push_back({1,mid,n});
        }
        vector<int> all(n); iota(all.begin(),all.end(),1);
        rows.push_back(all);
        for(int skip=2; skip<=n-1; skip++){
            vector<int> v;
            for(int i=1;i<=n;i++) if(i!=skip) v.push_back(i);
            rows.push_back(v);
        }
    }
    cout<<rows.size()<<"\n";
    for(auto &v:rows){
        for(size_t i=0;i<v.size();i++){ if(i) cout<<" "; cout<<v[i]; }
        cout<<"\n";
    }
    return 0;
}
