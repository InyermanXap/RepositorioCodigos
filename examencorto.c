#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<math.h>
int main(){
    FILE*archivo;
    if(archivo==NULL){
        printf("Error en la apertura de archivo\n");
    }
    system("clear");
    int opcion = 0;
    while (opcion !=4){
        system("clear");
        printf("Menu:\n");
        printf("1.Cobrar Parqueo\n");
        printf("2.Mostrar Historial\n");
        printf("3.Borrar Historial\n");
        printf("4.Salir\n");
        printf("Seleccione una opcion:");
        scanf("%d",&opcion);
        switch (opcion) {
            case 1:
                char nombre [50];
                char placa [6];
                char NIT [10];
                double entrada,salida,totalhoras,total,horasporcobrar;
                printf("Ingrese Su Nombre De Usuario\n");
                scanf("%s",nombre);
                printf("Ingrese Su Numero De Placa\n");
                scanf("%s",placa);
                printf("Ingrese su numero de NIT\n");
                scanf("%s",NIT);
                printf("Ingrese la hora de entrada del vehiculo\n");
                scanf("%lf", &entrada);
                printf("Ingrese la hora de salida del vehiculo\n");
                scanf("%lf", &salida);
                /*Calculo de parqueo*/
                if (entrada<0){
                    printf("Favor verifique su hora de entrada\n");
                }else if (salida<0){
                    printf("Favor verifique su hora de salida\n");
                }
                totalhoras=(salida-entrada);
                horasporcobrar=ceil(totalhoras);
                if (totalhoras>0){
                total=(((horasporcobrar-1)*20)+15);
                printf("totalhoras:%.2lf",totalhoras);} else if(totalhoras<0){
                    double dia;
                    dia=((24+salida)-entrada);
                    horasporcobrar=ceil(dia);
                    printf("totalhoras:%.2lf",totalhoras);
                    total=(((horasporcobrar-1)*20)+15);
                }
                        //Ingreso de datos al sistema//
                        archivo=fopen("salida.txt","a+t");
                        fprintf(archivo,"Nombre:    %s\n",nombre);
                        fprintf(archivo,"Placa: %s\n",placa);
                        fprintf(archivo,"Total de compra:   %.2lf\n",total);
                        fprintf(archivo,"Nit:   %s\n",NIT);
                        fprintf(archivo,"Estancia en el parqueo:    %.2lf horas\n",totalhoras);

                        fclose(archivo);
                        printf("Datos guardados\n");
                        printf("Gracias por visitarnos\n");
                        break;
            case 2:
                char caracter;
                archivo=fopen("salida.txt","r");
                printf("Facturas:");
                while(feof(archivo)==0){
                    caracter=fgetc(archivo);
                    printf("%c",caracter);
                }
                break;
            case 3:
                printf("Seguro que desea borrar el historial de compras esta accion no se puede deshacer\n");
                printf("Presione 1. Para continuar\n");
                printf("Presione 2. Para cancelar\n");
                int verificacion;
                scanf("%d",&verificacion);
                switch(verificacion){
                    case 1:
                            FILE*archivo=fopen("salida.txt", "w+t");
                            system("clear");
                            printf("Datos Borrados\n");
                            fclose(archivo);
                            sleep(5);
                            break;
                        
                    case 2:
                        printf("Saliendo");
                        sleep(5);
                        break;
                     
                    default:
                    printf("Por favor escoja una de las opciones\n");
                }
                
            case 4: 
                printf("Saliendo\n");
                sleep(3);
                break;
            default:
            printf("Por favor seleccione una de las opciones\n");
            sleep(3);
            break;
        }
    return 0;
}
}
