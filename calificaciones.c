#include<stdio.h>
#include<stdlib.h>
int main () {
    double cal1, cal2, cal3, cal4, cal5;
    printf("Este programa ayuda a calcular su rendimiento calculando algunos datos estadististcos tales como la\n ");
    printf(" media, mediana, moda, rango, desviacion estandar, y varianza de sus ultimas 5 notas.\n");
    printf("Para continuar por favor\n");
    /*ingreso de datos*/
    printf("Ingrese su primera calificacion en numeros\n");
    scanf("%lf",&cal1);
    printf("Ingrese su segunda calificacion en numeros\n");
    scanf("%lf",&cal2);
    printf("Ingrese su tercera calificacion en numeros\n");
    scanf("%lf",&cal3);
    printf("Ingrese su cuarta calificacion en numeros\n");
    scanf("%lf",&cal4);
    printf("Ingrese su quinta calificacion en numeros\n");
    scanf("%lf",&cal5);
    /*Calculo de media*/
    double media, mediana, moda, rango, desviacion, varianza;
    double sumatoria= (cal1 + cal2 + cal3 + cal4 + cal5 );
    media = (sumatoria / 5 );
    printf("Media:%.2lf\n",media);
    /*Calculo de mediana*/
    double arreglo[5]={cal1,cal2,cal3,cal4,cal5};
    int ordenado;
    do{
        ordenado =1;
    for (int i =0; i<5; i++){
        if(arreglo[i]>arreglo[i+1]){
            double aux =arreglo[i];
            arreglo[i+1]=aux;
            ordenado=0;
        }
    }
    }
    while(ordenado==0);
    for(int i = 0; i <5; i ++){
         printf("%.2lf\n",arreglo[i]);
    }
    return 0;
}