#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
int main(){
    FILE*archivo=fopen("salida.txt","a+t");
    system("clear");
    if (archivo == NULL){
        printf("No se pudo abrir el archivo.\n");
        return 1;
    }
    int opcion = 0;
    while (opcion !=4){
        system("clear");
        printf("Menu:\n");
        printf("1.Comprar Gasolina\n");
        printf("2.Mostrar Historial\n");
        printf("3.Borrar Historial\n");
        printf("4.Salir\n");
        printf("Seleccione una opcion:");
        scanf("%d",&opcion);
        switch (opcion) {
            case 1:{
                char nombre [50];
                char placa [6];
                int litros;
                printf("Ingrese Su Nombre De Usuario\n");
                scanf("%s",nombre);
                printf("Ingrese Su Numero De Placa\n");
                scanf("%s",placa);
                printf("Ingrese la cantidad de litros que desea comprar\n");
                scanf("%d",&litros);
                //Seleccion de Gasolina//
                printf("Seleccione el tipo de gasolina que desea\n");
                printf("1.Diesel Q28.00\n");
                printf("2.Regular Q30.00\n");
                printf("3.Super Q32.00\n");
         

                int gasolina = 0;
                while (gasolina !=4) {
               
                double precioD, precioR, precioS;
                scanf("%d",&gasolina);
                switch (gasolina) {
                    case 1:{
                        precioD = ( litros * 29 );
                        printf("%.2lf",precioD);
                        fprintf(archivo,"Nombre:%s\n",nombre);//Ingreso de datos al sistema//
                        fprintf(archivo,"Placa:%s\n",placa);
                        fprintf(archivo,"Total de compra:%.2lf\n",precioD);
                        printf("Datos guardados\n");
                        printf("Gracias por su compra\n");
                        printf("Presione 4 para finalizar");
                    
                    }
                    case 2:{
                        precioR=(litros*30);
                        fprintf(archivo,"Nombre:%s\n",nombre);//Ingreso de datos al sistema//
                        fprintf(archivo,"Placa:%s\n",placa);
                        fprintf(archivo,"Total de compra:%.2lf\n",precioR);
                        printf("Datos guardados\n");
                        printf("Gracias por su compra\n");
                        printf("Presione 4 para finalizar");
                    
                    }
                    case 3:{
                        precioS=(litros*32);
                        fprintf(archivo,"Nombre:%s\n",nombre);//Ingreso de datos al sistema//
                        fprintf(archivo,"Placa:%s\n",placa);
                        fprintf(archivo,"Total de compra:%.2lf\n",precioS);
                        printf("Datos guardados\n");
                        printf("Gracias por su compra\n");
                        printf("Presione 4 para finalizar");
                    }
                
                }
                }

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
            case 3:{
                printf("Seguro que desea borrar el historial de compras esta accion no se puede deshacer\n");
                printf("Presione 1. Para continuar\n");
                printf("Presione 2. Para cancelar\n");
                int verificacion;
                scanf("%d",&verificacion);
                switch(verificacion){
                    case 1:{
                            FILE*archivo=fopen("salida.txt", "w+t");
                            system("clear");
                            printf("Datos Borrados\n");
                            sleep(5);
                            break;
                        }
                    case 2:{
                        printf("Regresando al menu");
                        sleep(5);
                        break;
                     }
                    default:
                    printf("Por favor escoja una de las opciones\n");
                    }
                }
            case 4: {
                printf("Saliendo\n");
                sleep(5);
                break;
            }
            }
        }
        
    fclose(archivo);
    return 0;
}