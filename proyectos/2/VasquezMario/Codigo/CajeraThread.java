// Cajera con hilos (Hereda de Thread)
// Tiene un nombre, un objeto Cliente (Que contiene el carrito de compras)
public class CajeraThread extends Thread {

	private String nombre;

	private Cliente cliente;

	private long initialTime;


	public CajeraThread() {
	}

	public CajeraThread(String nombre, Cliente cliente,long initialTime) {
		this.setCliente(cliente);
		this.nombre = nombre;
		this.initialTime = initialTime;
	}

	public String getNombre() {
		return nombre;
	}

	public void setNombre(String nombre) {
		this.nombre = nombre;
	}

	public long getInitialTime() {
		return initialTime;
	}

	public void setInitialTime(long initialTime) {
		this.initialTime = initialTime;
	}

	public Cliente getCliente() {
		return cliente;
	}

	public synchronized void setCliente(Cliente cliente) {
		this.cliente = cliente;
	}

	// Metodo run para procesar una compra (Se reemplaza por el de procesarCompra de Cajera)
	@Override
	public synchronized void run() {

		// Imprime que comienza con el cliente con n producto
		System.out.println("La cajera " + this.nombre + " COMIENZA A PROCESAR LA COMPRA DEL CLIENTE " 
					+ this.cliente.getNombre() + " EN EL TIEMPO: " 
					+ (System.currentTimeMillis() - this.initialTime) / 1000 
					+ "seg");


		// Va atendiendo al cliente y mostrando los articulos que tiene
		for (int i = 0; i < this.cliente.getSizeCarroCompra(); i++) {
			// Se procesa el pedido en X segundos
			this.esperarXsegundos(cliente.getCarroCompra().get(i));
			System.out.println("Cajera: " + this.nombre +
						" Procesado el producto " + (i + 1) 
						+ " del cliente " + this.cliente.getNombre() + "->Tiempo: " 
						+ (System.currentTimeMillis() - this.initialTime) / 1000 
						+ "seg");
		}

		// Imprime que acabo
		System.out.println("La cajera " + this.nombre + " HA TERMINADO DE PROCESAR " 
						+ this.cliente.getNombre() + " EN EL TIEMPO: " 
						+ (System.currentTimeMillis() - this.initialTime) / 1000 
						+ "seg");
	}

	// Duerme el hilo X segundos
	private void esperarXsegundos(int segundos) {
		try {
			Thread.sleep(segundos * 1000);
		} catch (InterruptedException ex) {
			Thread.currentThread().interrupt();
		}
	}

}