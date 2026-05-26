#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;
    string s; if(cin>>s){
        cout << count(s.begin(), s.end(), '1') << "\n";
    }
    return 0;
}
