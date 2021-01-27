class Muestras{
	//ATRIBUTOS
	private int []muestras;
	private int indice, espacio, contador;
	private int name;
	
	//CONSTRUCTOR
	public Muestras(int n){
		muestras = new int [n];
		espacio = n;
		indice = -1;
	}

	public void ImprimeDatos(){
		for (int i = 0; i <= indice; i++) {
			System.out.print("[" + i + "] "+ muestras[i] + "\t");

		}
		System.out.println();
	}

	public synchronized void AlmacenaMuestra(int date, String hilo){
		name = date;
		while (indice == muestras.length-1) {
			try{
				wait(); //se pone a dormir y cede el monitor
			} catch (InterruptedException e){}
		}
		indice++;
		muestras[indice] = date;//(int)(Math.random()*100);
		System.out.println("Por la entrada" + hilo + " entra el automovil " + date + " y quedan " + (espacio-indice-1) + " lugares disponibles en el estacionamiento.");
		ImprimeDatos();
		notifyAll();
	}

	public synchronized void DespachaMuestra(String nombre){
		//name = nombre;
		while (indice < 0){
			//no hay datos
			try{
				wait(); //se pone a dormir y cede el monitor
			} catch (InterruptedException e){}
		}
		System.out.println("\nSalida" + nombre + ": sale el automovil " + muestras[0] + " y quedan " + (espacio-indice) + " lugares disponibles en el estacionamiento.");
		for (int i = 0; i < indice; i++) {
			muestras[i] = muestras[i+1];
		}
		indice--;
		ImprimeDatos();
		notifyAll();
	}
}