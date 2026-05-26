#include <bits/stdc++.h>
using namespace std;
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);
 int n,q; string s; if(!(cin>>n>>q>>s)) return 0;
 while(q--){int l,r;cin>>l>>r; string t=s.substr(l-1,r-l+1); int len=t.size(),ans=1; unordered_map<string,int> mp; mp.reserve((size_t)len*len/2+1); for(int i=0;i<len;i++){string cur; for(int j=i;j<len;j++){cur.push_back(t[j]); ans=max(ans,++mp[cur]);}} cout<<ans<<"\n";}
}
