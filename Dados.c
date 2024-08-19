#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int main () {
    int dado1, dado2, resultado;
    srand(time(NULL));
    dado1=rand() % 6 + 1;
    dado2=rand() % 6 + 1;
    resultado = dado1 + dado2;
    /*(0 a 6)*/
    printf("Juego del 8\n");
    printf("Reglas lanzas 2 dados y si sumas 8 ganas\n");
    printf("Si sacas 7 pierdes\n");
    printf("Si sacas cualquier otro numero puedes seguir jugando\n");
    /*Reglas del juego */
    printf("Tus dados dieron:\n");
    printf("Dado 1: %i\n", dado1);
    printf("Dado 2: %i\n", dado2);
    printf("Resultado: %i\n", resultado);
    if(resultado==7) {
       printf("Lo lamento perdiste\n");
    }
    if(resultado==8) {
            printf("Felicidades Ganaste\n");
        }
        else {
            printf("Sigue participando\n");
        }
    return 0;
}