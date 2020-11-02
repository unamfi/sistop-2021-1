##Tarea 1
###Problema desarrollado: Los alumnos y el asesor
####Integrantes 
- Montiel Martinez Luis Javier
- Rodríguez Dávalos Carolina
####Razonamiento
Inicialmente se abordo el caso del profesor. 

Tomando en cuenta el número de sillas en el cubículo del profesor realizamos una lista en la cual se encontrabas los id's de los alumnos que las ocupaban; en caso de no haber alumno alguno el hilo llamado 'profe' dormia.

Continuando con los alumnos. 

Generamos un número de preguntas aleatorio para cada alumno, posteriormente realiza un decremento al semáforo 'sillas', derivado de esto pueden ocurrir uno de dos casos: El hilo continuaba su ejecución o se mantenia en espera, si se cumple el primer caso el hilo 'profe' resolvía la duda, terminado esto, el semáforo 'sillas' incrementa mientras que el número de preguntas del este hilo alumno decrementa en una unidad, esto se repite hasta que su número de dudas sea cero.   

   
