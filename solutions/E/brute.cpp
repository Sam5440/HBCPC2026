#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    vector<vector<pair<int,int>>> byColor;
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>> pq;
    for(int l=1;l<=n;l++){
        for(int r=l+1;r<=n;r++){
            int c;
            if(!pq.empty() && pq.top().first<=l){
                c=pq.top().second; pq.pop();
            }else{
                c=byColor.size(); byColor.push_back({});
            }
            byColor[c].push_back({l,r});
            pq.push({r,c});
        }
    }
    cout << byColor.size() << "\n";
    for(auto &vec: byColor){
        vector<int> stops; stops.push_back(1);
        for(auto [l,r]: vec){
            if(stops.back()!=l) stops.push_back(l);
            if(stops.back()!=r) stops.push_back(r);
        }
        if(stops.back()!=n) stops.push_back(n);
        for(size_t i=0;i<stops.size();++i){ if(i) cout << ' '; cout << stops[i]; }
        cout << "\n";
    }
}
