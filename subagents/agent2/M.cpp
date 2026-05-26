#include <bits/stdc++.h>
using namespace std;
struct Dog{int r,c;char ch;};
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; if(!(cin>>T)) return 0;
    int dr[4]={-1,1,0,0}, dc[4]={0,0,-1,1};
    while(T--){
        int n,m; cin>>n>>m;
        vector<string> g(n);
        vector<Dog> dogs(1);
        pair<int,int>S,E;
        for(int i=0;i<n;i++){
            cin>>g[i];
            for(int j=0;j<m;j++){
                char ch=g[i][j];
                if(ch=='S') S={i,j};
                else if(ch=='E') E={i,j};
                else if(ch=='U'||ch=='D'||ch=='L'||ch=='R') dogs.push_back({i,j,ch});
            }
        }
        int N=n*m, D=dogs.size()-1;
        vector<int> cnt(N,0), own(N,0);
        auto inside=[&](int r,int c){return r>=0&&r<n&&c>=0&&c<m;};
        auto block=[&](char ch){return ch=='#'||ch=='U'||ch=='D'||ch=='L'||ch=='R';};
        for(int d=1;d<=D;d++){
            int r=dogs[d].r, c=dogs[d].c, k=0;
            if(dogs[d].ch=='D') k=1; else if(dogs[d].ch=='L') k=2; else if(dogs[d].ch=='R') k=3;
            r+=dr[k]; c+=dc[k];
            while(inside(r,c) && !block(g[r][c])){
                int idx=r*m+c; cnt[idx]++; if(cnt[idx]==1) own[idx]=d; else own[idx]=-1;
                r+=dr[k]; c+=dc[k];
            }
        }
        auto pass0=[&](int r,int c){
            char ch=g[r][c];
            return ch!='#'&&ch!='U'&&ch!='D'&&ch!='L'&&ch!='R'&&cnt[r*m+c]==0;
        };
        vector<int> comp(N,-1), compSize;
        int sc=-1, ec=-1, cc=0;
        queue<pair<int,int>> q;
        for(int i=0;i<n;i++)for(int j=0;j<m;j++) if(pass0(i,j)&&comp[i*m+j]<0){
            comp[i*m+j]=cc; q.push({i,j});
            while(!q.empty()){
                auto [r,c]=q.front(); q.pop();
                for(int z=0;z<4;z++){int nr=r+dr[z],nc=c+dc[z]; if(inside(nr,nc)&&pass0(nr,nc)&&comp[nr*m+nc]<0){comp[nr*m+nc]=cc;q.push({nr,nc});}}
            }
            cc++;
        }
        sc=comp[S.first*m+S.second]; ec=comp[E.first*m+E.second];
        if(sc==ec){ cout<<dogs[1].r+1<<" "<<dogs[1].c+1<<"\n"; continue; }
        vector<vector<int>> cells(D+1);
        for(int i=0;i<n;i++)for(int j=0;j<m;j++){
            int idx=i*m+j;
            if(cnt[idx]==1 && own[idx]>0 && g[i][j]!='#') cells[own[idx]].push_back(idx);
        }
        pair<int,int> answer={INT_MAX,INT_MAX};
        vector<int> seen(N,0); int stamp=0;
        for(int d=1;d<=D;d++){
            bool good=false; stamp++;
            for(int start:cells[d]) if(seen[start]!=stamp){
                bool hasS=false, hasE=false;
                queue<int> qq; qq.push(start); seen[start]=stamp;
                while(!qq.empty()){
                    int v=qq.front(); qq.pop(); int r=v/m,c=v%m;
                    for(int z=0;z<4;z++){
                        int nr=r+dr[z],nc=c+dc[z]; if(!inside(nr,nc)) continue;
                        int ni=nr*m+nc;
                        if(comp[ni]==sc) hasS=true;
                        if(comp[ni]==ec) hasE=true;
                        if(cnt[ni]==1 && own[ni]==d && !block(g[nr][nc]) && seen[ni]!=stamp){seen[ni]=stamp;qq.push(ni);}
                    }
                }
                if(hasS&&hasE){good=true;break;}
            }
            if(good) answer=min(answer,{dogs[d].r+1,dogs[d].c+1});
        }
        if(answer.first==INT_MAX) cout<<"-1 -1\n"; else cout<<answer.first<<" "<<answer.second<<"\n";
    }
}
