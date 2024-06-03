
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, m, k;
    cin >> n >> m >> k;

    vector<vector<int>> spiders(n, vector<int>(m, 0));

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            char c;
            cin >> c;
            if (c != '.') {
                int direction = 0;
                if (c == 'L') direction = 1;
                else if (c == 'R') direction = 2;
                else if (c == 'U') direction = 3;
                else if (c == 'D') direction = 4;

                int pos = j;
                for (int t = 0; t < k; ++t) {
                    if (i + t >= n) break;
                    if (direction == 1) pos--;
                    else if (direction == 2) pos++;
                    if (pos < 0 || pos >= m) break;
                    spiders[i + t][pos]++;
                }
            }
        }
    }

    for (int j = 0; j < m; ++j) {
        cout << spiders[0][j] << " ";
    }

    return 0;
}
