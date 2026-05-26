#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    struct Color{int end; vector<pair<int,int>> seg;};
    vector<Color> colors;
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>> pq;
    vector<pair<int,int>> intervals;
    for(int l=1;l<=n;l++) for(int r=l+1;r<=n;r++) intervals.push_back({l,r});
    sort(intervals.begin(), intervals.end());
    for(auto [l,r]:intervals){
        int id;
        if(!pq.empty() && pq.top().first<=l){
            id=pq.top().second; pq.pop();
        }else{
            id=colors.size(); colors.push_back({0,{}});
        }
        colors[id].end=r;
        colors[id].seg.push_back({l,r});
        pq.push({r,id});
    }
    cout<<colors.size()<<"\n";
    for(auto &co:colors){
        vector<int> v={1,n};
        for(auto [l,r]:co.seg){ v.push_back(l); v.push_back(r); }
        sort(v.begin(),v.end());
        v.erase(unique(v.begin(),v.end()),v.end());
        for(size_t i=0;i<v.size();i++){ if(i) cout<<" "; cout<<v[i]; }
        cout<<"\n";
    }
}
