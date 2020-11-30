class ProductorMuestras extends Thread{
	private Muestras m;
	private int entrada, hilo, aleatorio, contador;
	private int []arreglo;

	public ProductorMuestras(String name, Muestras m, int entrada,int hilo, int contador, int []x){
		this.m = m;
		setName(name);
		this.entrada = entrada;
		this.hilo = hilo;
		this.contador = contador;
		arreglo = x;
		arreglo[contador] = entrada;
	}

	public void run(){ //Los autos se generan de manera aleatoria entre 0 y 100 y si el hilo genera un numero aleatorio entre el 0 y 30 este ingresa(no todos los autos circulando quieres estacionarse 😜)
		aleatorio = (int)(Math.random()*100);
		if (aleatorio <= 30) {	
			System.out.println("El hilo " + hilo + " genero el automovil " + aleatorio + " en la fila de la entrada " + (entrada-1));
			while (true) {
					m.AlmacenaMuestra(aleatorio, getName());
					try{
						sleep((int)(Math.random()*299)+1);
					} catch (InterruptedException e){}
			}
		}
	}
}