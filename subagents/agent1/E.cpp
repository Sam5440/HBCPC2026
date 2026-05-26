#include <bits/stdc++.h>
using namespace std;
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);
 int n; if(!(cin>>n)) return 0;
 vector<vector<int>> ans;
 for(int i=1;i<=n;i++) for(int j=i+1;j<=n;j++){
     vector<int> v={1};
     if(i!=1) v.push_back(i);
     if(j!=n) v.push_back(j);
     v.push_back(n);
     v.erase(unique(v.begin(),v.end()),v.end());
     ans.push_back(v);
 }
 cout<<ans.size()<<"\n";
 for(auto &v:ans){for(size_t i=0;i<v.size();i++){if(i)cout<<' ';cout<<v[i];}cout<<"\n";}
}
