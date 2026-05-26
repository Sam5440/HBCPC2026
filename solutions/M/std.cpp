#include <bits/stdc++.h>
using namespace std;
bool dog(char c){return c=='U'||c=='D'||c=='L'||c=='R';}
int dr(char c){return c=='D'?1:c=='U'?-1:0;}
int dc(char c){return c=='R'?1:c=='L'?-1:0;}
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; if(!(cin>>T)) return 0;
    while(T--){
        int n,m; cin>>n>>m; vector<string> grid(n);
        for(auto &row:grid) cin>>row;
        vector<pair<int,int>> dogs; pair<int,int>S,E;
        for(int i=0;i<n;i++)for(int j=0;j<m;j++){
            if(dog(grid[i][j])) dogs.push_back({i,j});
            if(grid[i][j]=='S') S={i,j};
            if(grid[i][j]=='E') E={i,j};
        }
        auto can=[&](int sleep)->bool{
            vector<vector<int>> seen(n, vector<int>(m,0));
            for(int idx=0; idx<(int)dogs.size(); ++idx) if(idx!=sleep){
                auto [r,c]=dogs[idx]; char d=grid[r][c]; int nr=r+dr(d), nc=c+dc(d);
                while(nr>=0&&nr<n&&nc>=0&&nc<m && grid[nr][nc]!='#' && !dog(grid[nr][nc])){
                    seen[nr][nc]++;
                    nr+=dr(d); nc+=dc(d);
                }
            }
            queue<pair<int,int>> q; vector<vector<char>> vis(n, vector<char>(m,0));
            auto freecell=[&](int r,int c){
                if(r<0||r>=n||c<0||c>=m) return false;
                if(grid[r][c]=='#'||dog(grid[r][c])||seen[r][c]) return false;
                return true;
            };
            if(!freecell(S.first,S.second)||!freecell(E.first,E.second)) return false;
            q.push(S); vis[S.first][S.second]=1;
            int rr[4]={1,-1,0,0}, cc[4]={0,0,1,-1};
            while(!q.empty()){
                auto [r,c]=q.front(); q.pop();
                if(make_pair(r,c)==E) return true;
                for(int z=0;z<4;z++){int nr=r+rr[z],nc=c+cc[z]; if(freecell(nr,nc)&&!vis[nr][nc]){vis[nr][nc]=1;q.push({nr,nc});}}
            }
            return false;
        };
        if(can(-1)){ cout<<dogs[0].first+1<<" "<<dogs[0].second+1<<"\n"; continue; }
        pair<int,int> ans={-1,-1};
        for(int i=0;i<(int)dogs.size();i++) if(can(i)){ ans={dogs[i].first+1,dogs[i].second+1}; break; }
        cout<<ans.first<<" "<<ans.second<<"\n";
    }
}
