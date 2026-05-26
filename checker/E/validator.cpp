#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){
    if(argc<3){cerr<<"usage: validator input output\n";return 2;}
    ifstream in(argv[1]), out(argv[2]);
    int n; in>>n;
    long long expected=1LL*(n/2)*(n-n/2);
    int m; if(!(out>>m)) return 1;
    if(m!=expected) return 1;
    vector<vector<char>> cov(n+1, vector<char>(n+1,0));
    long long total=0;
    string line; getline(out,line);
    for(int i=0;i<m;i++){
        if(!getline(out,line)) return 1;
        stringstream ss(line); vector<int> a; int x;
        while(ss>>x) a.push_back(x);
        if(a.size()<2 || a.front()!=1 || a.back()!=n) return 1;
        total += a.size();
        for(int j=1;j<(int)a.size();j++){
            if(a[j-1]>=a[j] || a[j]<1 || a[j]>n) return 1;
            cov[a[j-1]][a[j]]=1;
        }
    }
    if(total>2000000) return 1;
    for(int l=1;l<=n;l++) for(int r=l+1;r<=n;r++) if(!cov[l][r]) return 1;
    return 0;
}
