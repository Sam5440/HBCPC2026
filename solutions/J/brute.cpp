#include <bits/stdc++.h>
using namespace std; using ll=long long;
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n;ll M;if(!(cin>>n>>M))return 0;ll bc=-1;int bi=1;for(int i=1;i<=n;i++){ll A,B;cin>>A>>B;ll cur=0;for(ll d=0;d*B<=M && d<=100000;d++)cur=max(cur,12*d+(M-d*B)/A); if(cur>bc){bc=cur;bi=i;}}cout<<bc<<" "<<bi<<"\n";}
