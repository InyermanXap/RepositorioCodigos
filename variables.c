#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
/*
En C, el tipo de datos bool no es un tipo integrado, es una macro definida en el archivo de encabezado stdbool.h
*/
int main(){
    int i = 11;
    int j = 12;
    char c ='A';
    float n=40.791512;
    system("clear");
    printf("%x %3d %c %.3f \n",i,j,c,n);
    return 0;
}