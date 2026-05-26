#include <bits/stdc++.h>
using namespace std;
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);
 int T; if(!(cin>>T)) return 0; int dr[4]={-1,1,0,0}, dc[4]={0,0,-1,1};
 string dogs="UDLR";
 while(T--){int n,m;cin>>n>>m; vector<string> g(n); for(auto &r:g)cin>>r; vector<pair<int,int>> dog; pair<int,int>S,E; for(int i=0;i<n;i++)for(int j=0;j<m;j++){if(dogs.find(g[i][j])!=string::npos)dog.push_back({i,j}); if(g[i][j]=='S')S={i,j}; if(g[i][j]=='E')E={i,j};}
 auto ok=[&](int sleep)->bool{vector<vector<char>> bad(n, vector<char>(m)); for(int i=0;i<n;i++)for(int j=0;j<m;j++) if(g[i][j]=='#'||dogs.find(g[i][j])!=string::npos) bad[i][j]=1; for(size_t id=0;id<dog.size();id++) if((int)id!=sleep){auto [r,c]=dog[id]; int dir=dogs.find(g[r][c]); int nr=r+dr[dir],nc=c+dc[dir]; while(nr>=0&&nr<n&&nc>=0&&nc<m&&g[nr][nc]!='#'&&dogs.find(g[nr][nc])==string::npos){bad[nr][nc]=1; nr+=dr[dir]; nc+=dc[dir];}} queue<pair<int,int>>q; vector<vector<char>> vis(n, vector<char>(m)); if(bad[S.first][S.second])return false; q.push(S); vis[S.first][S.second]=1; while(!q.empty()){auto [r,c]=q.front();q.pop(); if(make_pair(r,c)==E)return true; for(int z=0;z<4;z++){int nr=r+dr[z],nc=c+dc[z]; if(nr>=0&&nr<n&&nc>=0&&nc<m&&!bad[nr][nc]&&!vis[nr][nc])vis[nr][nc]=1,q.push({nr,nc});}} return false;};
 int ans=-1; for(size_t i=0;i<dog.size();i++) if(ok(i)){ans=i;break;} if(ans<0) cout<<"-1 -1\n"; else cout<<dog[ans].first+1<<" "<<dog[ans].second+1<<"\n";
 }
}
