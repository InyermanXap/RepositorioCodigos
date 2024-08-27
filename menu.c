#include<stdio.h>
#include<stdlib.h>/*libreria para ejecutar instrucciones del SO*/
#include<unistd.h>/*Incluye la biblioteca para la funcion sleep*/
long long calcularFactorial(int num){
    if (num <= 1){
        return 1;
    }
    return num*calcularFactorial(num -1);
}
int main(){
    FILE*archivo=fopen("salida.txt", "a+t");
    system("clear");
    if (archivo == NULL){
        printf("No se pudo abrir el archivo.\n");
        return 1;
    }
    int opcion = 0;
    while (opcion !=3){
        system("clear");
        printf("Menú:\n");
        printf("1.Ingresar datos\n");
        printf("2Mostrar historia\n");
        printf("3.Salir\n");
        printf("Seleccione una opción:");
        scanf("%d",&opcion);
        switch (opcion) {
            case 1:{
                char nombre [50];
                int numero;

                printf("Ingrese su nombre: ");
                scanf("%s", nombre);

                printf("Ingrese un número entero:");
                scanf("%d", &numero);
                long long factorial = calcularFactorial(numero);
                fprintf(archivo,"Nombre:%s\n",factorial);
                fprintf(archivo,"Número ingresado:%d\n",numero);
                fprintf(archivo,"Factorial:%lld\n\n",factorial);
                printf("Datos guardados en el archivo salida.txt.\n");
                sleep(5); /*Pausa el programa durante 5 segundos*/
                break;
            }
            case 2:{
                char c;
                fseek(archivo,0,SEEK_SET);/*Coloca el puntero al principio del archivo*/
                while((c=fgetc(archivo))!=EOF){
                    printf("%c",c);
                }
                printf("\n\n");
                printf("Datos almacenados en el archivo salida.txt.\n");
                sleep(5);/*Pausa el programa durante 5 segundos*/
                break;
            }
            case 3:
                printf("Saliendo del programa.\n");
                break;
                default:
                printf("Opción no válida.\n");
                break;
            
        }
    }
    fclose(archivo);
    return 0;
}