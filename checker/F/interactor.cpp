#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){
    if(argc<2){cerr<<"usage: interactor data.in\n";return 2;}
    ifstream fin(argv[1]);
    int n; string s; fin>>n>>s;
    int total=0; for(char c:s) total+=c=='1';
    cerr<<"This standalone interactor expects to be connected to a contestant process via stdin/stdout.\n";
    cout<<n<<endl;
    int queries=0;
    string tag;
    while(cin>>tag){
        if(tag=="?"){
            int k; cin>>k; vector<int> used(n+1,0); int inside=0;
            for(int i=0;i<k;i++){int p;cin>>p; if(p<1||p>n||used[p]) return 1; used[p]=1; inside+=s[p-1]=='1';}
            if(++queries>17) return 1;
            cout << 1LL*inside*(total-inside) << endl;
        }else if(tag=="!"){
            int ans; cin>>ans; return ans==total?0:1;
        }else return 1;
    }
    return 1;
}
