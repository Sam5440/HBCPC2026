#include <bits/stdc++.h>
using namespace std;
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);
 int T; if(!(cin>>T)) return 0; while(T--){int n,m; int cnt[3]; cin>>n>>m>>cnt[0]>>cnt[1]>>cnt[2]; vector<pair<int,int>> seg(m); for(auto &p:seg)cin>>p.first>>p.second; string ans; ans.reserve(n); for(int c=0;c<3;c++) ans.append(cnt[c], "RGB"[c]); cout<<ans<<"\n"; }
}
