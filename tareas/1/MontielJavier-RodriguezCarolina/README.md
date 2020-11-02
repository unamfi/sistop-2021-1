# Tarea 1

## Problema desarrollado: Los alumnos y el asesor

### Integrantes 

- Montiel Martínez Luis Javier
- Rodríguez Dávalos Carolina

#### Razonamiento
Inicialmente se abordo el caso del profesor. 

Tomando en cuenta el número de sillas en el cubículo del profesor, realizamos una lista en la cual se encontraban los id's de los alumnos que las ocupaban; en caso de no haber alumno alguno, el hilo llamado 'profe' dormía.

Continuando con los alumnos. 

Generamos un número de preguntas aleatorio para cada alumno, posteriormente se realiza un decremento al semáforo 'sillas', derivado de esto pueden ocurrir uno de dos casos: El hilo continua su ejecución o se mantiene en espera, si se cumple el primer caso el hilo 'profe' resolvía la duda, terminado esto, el semáforo 'sillas' incrementa mientras que el número de preguntas del hilo alumno decrementa en una unidad, esto se repite hasta que su número de dudas sea cero.   

   
