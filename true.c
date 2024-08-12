#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
/*
En C, el tipo de datos bool no es un tipo integrado, es una macro definida en el archivo de encabezado stdbool.h
*/
int main() {
    bool x = true ;
    bool y = false ;
    system("clear");
    printf("%d \n", x );
    printf("%d \n", y );
    return 0;
}