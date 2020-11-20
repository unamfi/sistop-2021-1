#include <omp.h>
#include <stdio.h>
#define N 100
float A[N], B[N], pe;
void AporB()
{
 int j;
 #pragma omp for reduction(+:pe)
 for (j=0; j<N; j++) pe += A[j] * B[j];
}
main ()
{
 int i;
 for (i=0; i<N; i++)
 {
 A[i] = i;
 B[i] = N-i;
 }
 pe = 0.0;
 #pragma omp parallel
 {
 AporB();
 }
 printf("\n\n >> PE = %10.0f\n\n", pe);
} 
