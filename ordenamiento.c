#include <stdio.h>

int main()
{
  int n, arreglo[5], c, d, t, flag = 0;

  printf("Introduce el numero de estudiantes\n");
  scanf("%d", &n);

  printf("Introduce %d pesos enteros\n", n);

  for (c = 0; c < n; c++)
    scanf("%d", &arreglo[c]);

  for (c = 1 ; c <= n - 1; c++) {
    t = arreglo[c];

    for (d = c - 1 ; d >= 0; d--) {
      if (arreglo[d] > t) {
        arreglo[d+1] = arreglo[d];
        flag = 1;
      }
      else
        break;
    }
    if (flag)
      arreglo[d+1] = t;
  }

  printf("La lista ordenada ascendentemente es:\n");

  for (c = 0; c <= n - 1; c++) {
    printf("%d\n", arreglo[c]);
  }

  return 0;
}