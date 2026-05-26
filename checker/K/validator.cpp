#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){
    if(argc<3){cerr<<"usage: validator input output\n";return 2;}
    ifstream in(argv[1]), out(argv[2]);
    int T; in>>T;
    while(T--){
        int n,m,r,g,b; in>>n>>m>>r>>g>>b;
        vector<pair<int,int>> seg(m); for(auto &p:seg) in>>p.first>>p.second;
        string s; if(!(out>>s)) return 1;
        if(s=="-1") continue;
        if((int)s.size()!=n) return 1;
        int cr=0,cg=0,cb=0;
        for(char c:s){ if(c=='R')cr++; else if(c=='G')cg++; else if(c=='B')cb++; else return 1; }
        if(cr!=r||cg!=g||cb!=b) return 1;
        for(auto [l,rr]:seg){
            set<char> st; for(int i=l-1;i<=rr-1;i++) st.insert(s[i]);
            if(st.size()>2) return 1;
        }
    }
    return 0;
}
