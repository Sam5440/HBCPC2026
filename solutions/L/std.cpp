#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Group {
    long double ang;
    long double r2;
    int cnt;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.setf(ios::fixed);
    cout << setprecision(12);

    int T;
    if (!(cin >> T)) return 0;
    const long double PI = acosl(-1.0L);

    while (T--) {
        int n, k;
        cin >> n >> k;

        map<pair<ll, ll>, Group> mp;
        for (int i = 0; i < n; i++) {
            ll x, y;
            cin >> x >> y;
            ll g = std::gcd(llabs(x), llabs(y));
            pair<ll, ll> key = {x / g, y / g};

            long double ang = atan2l((long double)y, (long double)x);
            if (ang < 0) ang += 2 * PI;
            long double r2 = (long double)x * x + (long double)y * y;

            auto &grp = mp[key];
            if (grp.cnt == 0) {
                grp.ang = ang;
                grp.r2 = r2;
            } else {
                grp.r2 = max(grp.r2, r2);
            }
            grp.cnt++;
        }

        vector<Group> a;
        for (auto &kv : mp) a.push_back(kv.second);
        sort(a.begin(), a.end(), [](const Group &x, const Group &y) {
            return x.ang < y.ang;
        });

        int g = (int)a.size();
        long double best = 1e100L;
        deque<int> dq;
        int r = 0;
        int have = 0;

        auto angle_at = [&](int idx) {
            return a[idx % g].ang + (idx >= g ? 2 * PI : 0);
        };
        auto r2_at = [&](int idx) {
            return a[idx % g].r2;
        };
        auto cnt_at = [&](int idx) {
            return a[idx % g].cnt;
        };

        for (int l = 0; l < g; l++) {
            if (r < l) r = l;
            while (r < l + g && have < k) {
                while (!dq.empty() && r2_at(dq.back()) <= r2_at(r)) dq.pop_back();
                dq.push_back(r);
                have += cnt_at(r);
                r++;
            }

            if (have >= k) {
                long double width = angle_at(r - 1) - angle_at(l);
                best = min(best, 0.5L * width * r2_at(dq.front()));
            }

            if (r > l) {
                have -= cnt_at(l);
                if (!dq.empty() && dq.front() == l) dq.pop_front();
            }
        }

        cout << (double)best << "\n";
    }
}
