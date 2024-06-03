int n, m, d;
cin >> n >> m >> d;

vector<int> c(m);
for (int i = 0; i < m; ++i) {
    cin >> c[i];
}

int currPos = 0;
vector<int> res(n);

for (int i = 0; i < m; ++i) {
    if (currPos + d > n) {
        cout << "NO" << endl;
        return 0;
    }

    for (int j = 0; j < c[i]; ++j) {
        for (int k = 0; k < d && currPos + k < n; ++k) {
            res[currPos + k] = i + 1;
        }
        currPos += d;
    }
}

cout << "YES" << endl;
for (int i = 0; i < n; ++i) {
    cout << res[i] << " ";
}
cout << endl;