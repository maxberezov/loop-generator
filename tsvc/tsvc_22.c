for (int nl = 0; nl < 2 * ntimes; nl++) {
    for (int i = 0; i < LEN; i++) {
        a[i] = a[LEN / 2] + b[i];
    }
    dummy(a, b, c, d, e, aa, bb, cc, 0.);
}