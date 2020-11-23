import java.util.ArrayList;
import java.util.LinkedList; 
import java.util.Queue; 

public class MainThread {

	public static void main(String[] args) {

		// Programa concurrente
		// Clientes con n productos

		Queue<Cliente> clientes = new LinkedList<>(); 

		for (int i = 0;i < 5 ;i++ ) 
		{
			ArrayList <Integer> productos = new ArrayList<Integer>();
			for (int j =0; j<(int)(Math.random() * 4 + 1); j++ ) {
				productos.add((int)(Math.random() * 5 + 1));
			}
			clientes.add( new Cliente("Cliente " + (i+1), productos));
		}

		for (Cliente cl : clientes) {
			System.out.println(cl.getCarroCompra());
		}
		
		/*
		//Cliente cliente1 = new Cliente("Cliente 1", productos);
		//Cliente cliente2 = new Cliente("Cliente 2", new int[] { 1, 3, 5, 1, 1 });

		// Tiempo inicial de referencia
		long initialTime = System.currentTimeMillis();
		// Cajeras qcon hilos

		CajeraThread cajera1 = new CajeraThread("Cajera 1", initialTime);
		cajera1.setCliente(clientes.remove());
		//CajeraThread cajera2 = new CajeraThread("Cajera 2", cliente2, initialTime);


		// Inician
		cajera1.start();
		//cajera2.start();*/
		long initialTime = System.currentTimeMillis();
		while(!clientes.isEmpty())
		{
			new CajeraThread("Juanita",clientes.remove(),initialTime).start();
			new CajeraThread("Carmen",clientes.remove(),initialTime).start();
		}

	}
}