for (int nl = 0; nl < 4 * ntimes; nl++) {
    for (int i = 0; i < LEN; i++) {
        if (a[i] > b[i]) {
            a[i] += b[i] * c[i];
        }
    }
    dummy(a, b, c, d, e, aa, bb, cc, 0.);
}