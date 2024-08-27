#include<stdio.h>
#include<stdlib.h>
void main()
{
    float*pesos,temp;
    int i,j,nest;
    printf("Cuantos estudiantes son?:");
    scanf("%d",&nest);
    pesos=(float*)malloc(nest*sizeof(float));
    if (pesos==NULL)
    {
        printf("Insuficiente Espacio de Memoria\n");
        exit(-1);//Salir del Programa
    }
    for (i=0;i<nest;i++)
    {
        printf("Peso del Estudiante[%d]:",i+1);
        scanf("%f",(pesos+i));
    }
    printf("\n***ARRAY ORIGINAL***\n");
    for (i=0;i<nest;i++)
    printf("Peso[%d]:%.1f\n",i+1,*(pesos+i));
    for(i=0;i<nest;i++){
    for(j=0;j<(nest-1);j++)
    if(pesos[i]>pesos[j+1])
        {
            temp=pesos[i];
            pesos[j]=pesos[j+1];
            pesos[j+1]=temp;
        }
        }
    printf("\n***ARRAY ORDENADO EN FORMATO ASCENDENTE***\n");
    for(i=0;i<nest;i++)
    printf("Peso[%d]:%.1f\n",i+1,*(pesos+i));
}