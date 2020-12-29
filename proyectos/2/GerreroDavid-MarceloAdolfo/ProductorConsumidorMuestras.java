import java.util.Scanner;
class ProductorConsumidorMuestras{
	public static void main(String[] args) {
		//variables
		int espacio, entradas, salidas, numhilos, pilaentradas, contaentradas;
		int []A;
		int []entrance;
		Muestras lugares;
		ProductorMuestras in;
		CConsumidorMuestras out;

		//Peticion de datos
		Scanner entrada = new Scanner(System.in);
		System.out.print("Ingrese un numero de entradas para el estacionamiento: ");
		entradas = entrada.nextInt();

		Scanner salida = new Scanner(System.in);
		System.out.print("Ingrese un numero de salidas del estacionamiento: ");
		salidas = salida.nextInt();

		Scanner capadidad = new Scanner(System.in);
		System.out.print("Ingrese cuantos lugares quiere en el estacionamiento: ");
		espacio = capadidad.nextInt();

		Scanner numero = new Scanner(System.in);
		System.out.print("Ingrese el numero de hilos: ");
		numhilos = numero.nextInt();

		entrance = new int [1000];
		for (int i = 0; i < 1000; i++) {
			entrance[i] = -1;
		}
		contaentradas = 0;

		//creacion de los hilos
		lugares = new Muestras(espacio);//cuantos lugares hay en el estacionamiento
		
		while (true) {
			
			for (int i = 1; i < entradas + 1 ; i++) {
				for (int j = 0; j < numhilos; j++) {

					in = new ProductorMuestras((" " + i), lugares,(i+1),(j+1),contaentradas, entrance);
					contaentradas++;
					in.start();	
				}
				
			}
			
			for (int i = 1; i < salidas + 1; i++) {
				out = new CConsumidorMuestras((" " + i), lugares);
				out.start();
			}

			
		}


		

		//System.out.println("Termino el hilo...");
	}
}