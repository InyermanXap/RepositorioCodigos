#include<stdio.h>
int main() {
    printf("Este programa se encarga de calcular el iva de un producto\n");
    printf("Por favor Ingrese el precio de su articulo \n");
    double precio;
    double iva;
    double preciolibre;
    scanf("%lf",&precio);
    /*calculo*/
    iva = (precio*0.12);
    preciolibre= precio-iva;
    printf("Precio total :%.2lf\n", precio);
    printf("IVA :%.2lf\n", iva);
    printf("Precio sin IVA :%.2lf\n", preciolibre);

    return 0;
}