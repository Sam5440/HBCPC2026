#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; if(!(cin>>T)) return 0;
    int dr[4]={-1,1,0,0}, dc[4]={0,0,-1,1};
    string dirs="UDLR";
    while(T--){
        int n,m; cin>>n>>m; vector<string> g(n);
        vector<pair<int,int>> dogs; pair<int,int>S,E;
        for(int i=0;i<n;i++){cin>>g[i];for(int j=0;j<m;j++){char c=g[i][j]; if(c=='S')S={i,j}; else if(c=='E')E={i,j}; else if(dirs.find(c)!=string::npos) dogs.push_back({i,j});}}
        sort(dogs.begin(),dogs.end());
        auto can=[&](pair<int,int> sleep){
            vector<vector<char>> bad(n, vector<char>(m,0));
            for(int i=0;i<n;i++)for(int j=0;j<m;j++) if(g[i][j]=='#'||dirs.find(g[i][j])!=string::npos) bad[i][j]=1;
            for(auto [r,c]:dogs) if(make_pair(r,c)!=sleep){
                int d=dirs.find(g[r][c]); int nr=r+dr[d], nc=c+dc[d];
                while(nr>=0&&nr<n&&nc>=0&&nc<m&&g[nr][nc]!='#'&&dirs.find(g[nr][nc])==string::npos){bad[nr][nc]=1; nr+=dr[d]; nc+=dc[d];}
            }
            if(bad[S.first][S.second]||bad[E.first][E.second]) return false;
            queue<pair<int,int>> q; vector<vector<char>> vis(n, vector<char>(m)); q.push(S); vis[S.first][S.second]=1;
            while(!q.empty()){auto [r,c]=q.front();q.pop(); if(make_pair(r,c)==E) return true; for(int z=0;z<4;z++){int nr=r+dr[z],nc=c+dc[z]; if(nr>=0&&nr<n&&nc>=0&&nc<m&&!bad[nr][nc]&&!vis[nr][nc]) vis[nr][nc]=1,q.push({nr,nc});}}
            return false;
        };
        pair<int,int> ans={-2,-2};
        for(auto d:dogs) if(can(d)){ans=d;break;}
        if(ans.first<0) cout<<"-1 -1\n"; else cout<<ans.first+1<<" "<<ans.second+1<<"\n";
    }
}
