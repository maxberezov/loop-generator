int main() {
for (int nl = 0; nl < ntimes / 2; nl++) {
    for (int i = 0; i < LEN - 1; ++i) {
        if (b[i] < (float) 0.) {
            goto L20;
        }
        a[i] = c[i] + d[i] * e[i];
        goto L10;
        L20:
        c[i + 1] = a[i] + d[i] * d[i];
        L10:;
    }
    dummy(a, b, c, d, e, aa, bb, cc, 0.);
}}
