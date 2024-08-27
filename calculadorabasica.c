#include<stdio.h> //incluye la biblioteca para las funciones basicas de entrada y salida
#include<stdlib.h> //incluye la biblioteca para la funcion system ("clear");
#include<unistd.h> //incluye la biblioteca para la funcion sleep

/*Este programa genera una calculadora basica.*/

int main(){
    int op,uno,dos;
    do{
        system("cls");
        printf("---Calculadora---\n");
        printf("\n¿Que desea hacer\n");
        printf("1) Sumar\n");
        printf("2) Restar\n");
        printf("3) Multiplicar\n");
        printf("4) Dividir\n");
        printf("5) Salir\n");
        scanf("%d",&op);
        switch(op){
        case 1:
            printf("\tSumar\n");
            printf("Introduzca los numeros a sumar separados por comas\n");
            scanf("%d,%d",&uno,&dos);
            printf("%d+%d=%d\n",uno,dos,(uno+dos));
            sleep(5);// Pausa el programa durante 5 segundos 
            break;
        case 2:
            printf("\tRestar\n");
            printf("Introduzca los numeros a restar separados por comas\n");
            scanf("%d,%d",&uno,&dos);
            printf("%d-%d=%d\n",uno,dos,(uno-dos));
            sleep(5);// Pausa el programa durante 5 segundos 
            break;
        case 3:
            printf("\tMultiplicar\n");
            printf("Introduzaca los numeros a multiplicar separados por comas\n");
            scanf("%d,%d",&uno,&dos);
            printf("%d*%d=%d\n",uno,dos,(uno*dos));
            sleep(5);// Pausa el programa durante 5 segundos 
            break;
        case 4:
            printf("\tDividir\n");
            printf("Introduzaca los numeros a Dividir separados por comas\n");
            scanf("%d,%d",&uno,&dos);
            printf("%d/%d=%.2lf\n",uno,dos,((double)uno/dos));
            sleep(5);// Pausa el programa durante 5 segundos 
            break;
        case 5:
            printf("\tSalir\n");
            sleep(5);// Pausa el programa durante 5 segundos
            break;
        default:
            printf("\tOpcion invalida.\n");
            sleep(5);// Pausa el programa durante 5 segundos
        }
    }while (op !=5);
    system("clear");
    return 0;
}