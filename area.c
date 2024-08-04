#include <stdio.h>
#include <stdlib.h>
/*
Calcula el area de un circulo cuyo radio es de 8.9 cm. Tome pi = 3.14 */

int main() {
    double pi = 3.14;
    double radius = 8.9;
    double area = pi * radius * radius;
    system("cls");
    printf("El valor del Area es %lf \n", area);
    return 0;
}