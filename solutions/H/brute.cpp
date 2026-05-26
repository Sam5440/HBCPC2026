#include <bits/stdc++.h>
using namespace std;
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n,q;if(!(cin>>n>>q))return 0;string s;cin>>s;while(q--){int l,r;cin>>l>>r;int cnt[26]={0};for(int i=l-1;i<r;i++)cnt[s[i]-'a']++;cout<<*max_element(cnt,cnt+26)<<"\n";}}
