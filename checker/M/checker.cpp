#include <bits/stdc++.h>
using namespace std;
bool dog(char c){return c=='U'||c=='D'||c=='L'||c=='R';}
int dr(char c){return c=='D'?1:c=='U'?-1:0;}
int dc(char c){return c=='R'?1:c=='L'?-1:0;}
bool can_sleep(const vector<string>&grid, int sleepR, int sleepC){
    int n=grid.size(), m=grid[0].size(); vector<pair<int,int>> dogs; pair<int,int>S,E;
    for(int i=0;i<n;i++)for(int j=0;j<m;j++){ if(dog(grid[i][j])) dogs.push_back({i,j}); if(grid[i][j]=='S')S={i,j}; if(grid[i][j]=='E')E={i,j}; }
    vector<vector<int>> seen(n, vector<int>(m,0));
    for(auto [r,c]:dogs) if(!(r==sleepR&&c==sleepC)){
        char d=grid[r][c]; int nr=r+dr(d), nc=c+dc(d);
        while(nr>=0&&nr<n&&nc>=0&&nc<m && grid[nr][nc]!='#' && !dog(grid[nr][nc])){ seen[nr][nc]++; nr+=dr(d); nc+=dc(d); }
    }
    auto freecell=[&](int r,int c){return r>=0&&r<n&&c>=0&&c<m&&grid[r][c]!='#'&&!dog(grid[r][c])&&!seen[r][c];};
    if(!freecell(S.first,S.second)||!freecell(E.first,E.second)) return false;
    queue<pair<int,int>> q; vector<vector<char>> vis(n, vector<char>(m,0)); q.push(S); vis[S.first][S.second]=1;
    int rr[4]={1,-1,0,0}, cc[4]={0,0,1,-1};
    while(!q.empty()){auto [r,c]=q.front();q.pop(); if(make_pair(r,c)==E)return true; for(int k=0;k<4;k++){int nr=r+rr[k],nc=c+cc[k]; if(freecell(nr,nc)&&!vis[nr][nc]){vis[nr][nc]=1;q.push({nr,nc});}}}
    return false;
}
int main(int argc,char**argv){
    if(argc<3){cerr<<"usage: checker input output\n";return 2;}
    ifstream in(argv[1]), out(argv[2]);
    int T; in>>T;
    while(T--){
        int n,m; in>>n>>m; vector<string> grid(n); for(auto &s:grid) in>>s;
        int x,y; if(!(out>>x>>y)) return 1;
        vector<pair<int,int>> dogs; for(int i=0;i<n;i++)for(int j=0;j<m;j++) if(dog(grid[i][j])) dogs.push_back({i,j});
        if(x==-1&&y==-1){
            for(auto [r,c]:dogs) if(can_sleep(grid,r,c)) return 1;
        }else{
            --x;--y; if(x<0||x>=n||y<0||y>=m||!dog(grid[x][y])) return 1;
            if(!can_sleep(grid,x,y)) return 1;
        }
    }
    return 0;
}
