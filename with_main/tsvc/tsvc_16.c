int main() {
for (int nl = 0; nl < 2 * ntimes; nl++) {
    for (int i = 0; i < lll; i++) {
        a[i] = b[i] + c[i];
        X[i] = (Y[i] * Z[i]) + (U[i] * V[i]);
        X[i] = Y[i] + 1;
    }
    dummy((float *) X, (float *) Y, (float *) Z, (float *) U, (float *) V, aa, bb, cc, 0.);
}}
