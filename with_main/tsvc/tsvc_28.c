int main() {
for (int nl = 0; nl < 200 * (ntimes / (LEN2)); nl++) {
    for (int i = 1; i < LEN2; i++) {
        for (int j = 1; j < LEN2; j++) {
            aa[i][j] = aa[i - 1][j - 1] + bb[i][j];
        }
    }
    dummy(a, b, c, d, e, aa, bb, cc, 0.);
}}