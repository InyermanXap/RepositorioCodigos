#include <stdio.h>
int main() {
    double num1, num2;

    printf("Ingrese el primer número: no un caracter ");
    scanf("%lf", &num1);

    printf("Ingrese el segundo número: no un caracter ");
    scanf("%lf", &num2);

    double suma = num1 + num2;
    double resta =num1 - num2;
    double multiplicacion = num1 * num2;
    
    printf("\nResultados:\n");
    printf("Suma: %.4lf\n", suma);
    printf("Resta: %.4lf\n", resta);
    printf("Multiplicación: %.4lf\n", multiplicacion);

    if (num2 == 0) {
        printf("Error: No se puede dividir entre cero. \n");
    } 
        else {        double division = num1 / num2;
            printf("División: %.4lf\n", division);
            }

    return 0;   
}