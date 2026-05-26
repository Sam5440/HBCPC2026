#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    vector<long long> res;
    for(int b=0;b<17;b++){
        vector<int> pos;
        for(int i=1;i<=n;i++) if((i>>b)&1) pos.push_back(i);
        if(pos.empty()) pos.push_back(1);
        cout << "? " << pos.size();
        for(int x:pos) cout << ' ' << x;
        cout << endl;
        long long v; if(!(cin>>v)) return 0;
        res.push_back(v);
    }
    int answer=1;
    for(int s=1;s<=n;s++){
        bool ok=true;
        for(long long p:res){
            long long d=1LL*s*s-4*p;
            if(d<0){ok=false;break;}
            long long rt=sqrt((long double)d);
            while(rt*rt<d) rt++;
            while(rt*rt>d) rt--;
            if(rt*rt!=d || ((s+rt)&1)){ok=false;break;}
        }
        if(ok){answer=s;break;}
    }
    cout << "! " << answer << endl;
}
