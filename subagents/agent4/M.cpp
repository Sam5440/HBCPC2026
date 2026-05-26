#include <bits/stdc++.h>
using namespace std;
struct DSU{vector<int> p; DSU(int n=0):p(n){iota(p.begin(),p.end(),0);} int f(int x){return p[x]==x?x:p[x]=f(p[x]);} void u(int a,int b){a=f(a);b=f(b);if(a!=b)p[b]=a;}};
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; if(!(cin>>T)) return 0;
    string dogs="UDLR";
    int dr[4]={-1,1,0,0}, dc[4]={0,0,-1,1};
    while(T--){
        int n,m; cin>>n>>m; vector<string> g(n);
        for(auto &s:g) cin>>s;
        vector<pair<int,int>> dog(1); vector<vector<int>> id(n, vector<int>(m));
        pair<int,int>S,E;
        for(int i=0;i<n;i++)for(int j=0;j<m;j++){
            if(g[i][j]=='S') S={i,j}; if(g[i][j]=='E') E={i,j};
            if(dogs.find(g[i][j])!=string::npos){id[i][j]=dog.size(); dog.push_back({i,j});}
        }
        int D=dog.size()-1, N=n*m;
        vector<int> cnt(N), uid(N);
        auto add=[&](int r,int c,int who){
            int x=r*m+c; if(g[r][c]=='#'||id[r][c]) return;
            if(cnt[x]==0) uid[x]=who; else uid[x]=-1; cnt[x]++;
        };
        for(int i=0;i<n;i++){
            int who=0;
            for(int j=0;j<m;j++){ char ch=g[i][j]; if(ch=='#'||id[i][j]) who=(ch=='R'?id[i][j]:0); else if(who) add(i,j,who); }
            who=0;
            for(int j=m-1;j>=0;j--){ char ch=g[i][j]; if(ch=='#'||id[i][j]) who=(ch=='L'?id[i][j]:0); else if(who) add(i,j,who); }
        }
        for(int j=0;j<m;j++){
            int who=0;
            for(int i=0;i<n;i++){ char ch=g[i][j]; if(ch=='#'||id[i][j]) who=(ch=='D'?id[i][j]:0); else if(who) add(i,j,who); }
            who=0;
            for(int i=n-1;i>=0;i--){ char ch=g[i][j]; if(ch=='#'||id[i][j]) who=(ch=='U'?id[i][j]:0); else if(who) add(i,j,who); }
        }
        auto open0=[&](int r,int c){return g[r][c]!='#'&&!id[r][c]&&cnt[r*m+c]==0;};
        DSU base(N);
        for(int i=0;i<n;i++)for(int j=0;j<m;j++) if(open0(i,j)){
            if(i+1<n&&open0(i+1,j)) base.u(i*m+j,(i+1)*m+j);
            if(j+1<m&&open0(i,j+1)) base.u(i*m+j,i*m+j+1);
        }
        int cs=base.f(S.first*m+S.second), ce=base.f(E.first*m+E.second);
        if(cs==ce){ cout<<dog[1].first+1<<" "<<dog[1].second+1<<"\n"; continue; }
        vector<vector<vector<int>>> lists(D+1);
        vector<char> vis(N);
        queue<int> q;
        for(int i=0;i<n;i++)for(int j=0;j<m;j++){
            int start=i*m+j, lab=(cnt[start]==1?uid[start]:0);
            if(lab<=0||vis[start]||g[i][j]=='#'||id[i][j]) continue;
            vis[start]=1; q.push(start); vector<int> comps;
            while(!q.empty()){
                int x=q.front(); q.pop(); int r=x/m,c=x%m;
                for(int z=0;z<4;z++){
                    int nr=r+dr[z], nc=c+dc[z]; if(nr<0||nr>=n||nc<0||nc>=m) continue;
                    int y=nr*m+nc;
                    if(open0(nr,nc)) comps.push_back(base.f(y));
                    else if(!vis[y] && cnt[y]==1 && uid[y]==lab && g[nr][nc]!='#' && !id[nr][nc]) vis[y]=1,q.push(y);
                }
            }
            sort(comps.begin(),comps.end()); comps.erase(unique(comps.begin(),comps.end()),comps.end());
            lists[lab].push_back(move(comps));
        }
        int answer=0;
        vector<pair<int,int>> order;
        for(int d=1;d<=D;d++) order.push_back({dog[d].first*m+dog[d].second,d});
        sort(order.begin(),order.end());
        for(auto [_,d]:order){
            unordered_map<int,int> mp; vector<int> par;
            auto get=[&](int c)->int{
                auto it=mp.find(c); if(it!=mp.end()) return it->second;
                int z=par.size(); mp[c]=z; par.push_back(z); return z;
            };
            function<int(int)> ff=[&](int x){return par[x]==x?x:par[x]=ff(par[x]);};
            auto uu=[&](int a,int b){a=ff(a);b=ff(b);if(a!=b)par[b]=a;};
            get(cs); get(ce);
            for(auto &vec:lists[d]) if(!vec.empty()){
                int first=get(vec[0]);
                for(int c:vec) uu(first,get(c));
            }
            if(ff(get(cs))==ff(get(ce))){answer=d;break;}
        }
        if(!answer) cout<<"-1 -1\n"; else cout<<dog[answer].first+1<<" "<<dog[answer].second+1<<"\n";
    }
}
