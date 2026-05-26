#include <bits/stdc++.h>
using namespace std;
struct Dog{int x,y,dx,dy;};
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; if(!(cin>>T)) return 0;
    while(T--){
        int n,m; cin>>n>>m;
        vector<string> g(n);
        for(auto &s:g) cin>>s;
        vector<Dog> dogs; pair<int,int>S,E;
        auto isdog=[&](char c){return c=='U'||c=='D'||c=='L'||c=='R';};
        auto block=[&](char c){return c=='#'||isdog(c);};
        for(int i=0;i<n;i++) for(int j=0;j<m;j++){
            char c=g[i][j];
            if(c=='S') S={i,j};
            if(c=='E') E={i,j};
            if(isdog(c)){
                int dx=0,dy=0;
                if(c=='U') dx=-1; if(c=='D') dx=1; if(c=='L') dy=-1; if(c=='R') dy=1;
                dogs.push_back({i,j,dx,dy});
            }
        }
        int D=dogs.size();
        vector<vector<int>> cnt(n, vector<int>(m,0)), first(n, vector<int>(m,-1));
        for(int id=0;id<D;id++){
            auto d=dogs[id];
            int x=d.x+d.dx, y=d.y+d.dy;
            while(x>=0&&x<n&&y>=0&&y<m&&!block(g[x][y])){
                cnt[x][y]++;
                if(cnt[x][y]==1) first[x][y]=id; else first[x][y]=-2;
                x+=d.dx; y+=d.dy;
            }
        }
        auto can=[&](int id){
            vector<vector<char>> vis(n, vector<char>(m,0));
            queue<pair<int,int>> q;
            auto safe=[&](int x,int y){
                if(x<0||x>=n||y<0||y>=m) return false;
                if(block(g[x][y])) return false;
                if(cnt[x][y]==0) return true;
                return cnt[x][y]==1 && first[x][y]==id;
            };
            if(!safe(S.first,S.second)) return false;
            vis[S.first][S.second]=1; q.push(S);
            int dx[4]={1,-1,0,0}, dy[4]={0,0,1,-1};
            while(!q.empty()){
                auto [x,y]=q.front(); q.pop();
                if(make_pair(x,y)==E) return true;
                for(int z=0;z<4;z++){
                    int nx=x+dx[z], ny=y+dy[z];
                    if(nx>=0&&nx<n&&ny>=0&&ny<m&&!vis[nx][ny]&&safe(nx,ny)){
                        vis[nx][ny]=1; q.push({nx,ny});
                    }
                }
            }
            return false;
        };
        int ans=-1;
        for(int i=0;i<D;i++) if(can(i)){ ans=i; break; }
        if(ans<0) cout<<"-1 -1\n";
        else cout<<dogs[ans].x+1<<" "<<dogs[ans].y+1<<"\n";
    }
    return 0;
}
