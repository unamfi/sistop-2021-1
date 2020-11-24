/*
  Clase Cajeras
  Esta Clase nos indica las tareas que realizan los Clientes (hilos).
  - esperarXsegundos: Duerme el Hilo x cantidad de segundos
  - Comprar: Indica cuanto tiempo se duerme el hilo segun el carro de compras del cliente
  Nota: El id de las Cajeras es el id del hilo que esta corriendo esa tarea
*/

// Paquetes
import java.util.ArrayList;

public class Cajeras {

  // Duerme el hilo X segundos, para simular el tiempo que tardo en registrar el producto en la compra final
  private void esperarXsegundos(int segundos) {
    try {
      Thread.sleep(segundos * 1000);
    } catch (InterruptedException ex) {
      System.out.println("El cliente era un ladron y se fue sin pagar (Protocolo cerrar Changarro)");
      Thread.currentThread().interrupt();
    }
  }

  // Recibe el id del cliente para identificarlo y tambien recibe el carro de compras
  // que inidca cuanto tiempo se duerme el hilo en cada producto simulando lo que se tarda la cajera en agregarlos a la compra
  public void Comprar(int idClliente,ArrayList <Integer> carroCompra) {
    int tiempoNecesitado = 0; // Tiempo que se tardara en procesar toda la compra del cliente
    System.out.println("\n ---------------------------------------------");
    System.out.println("| El cliente " + idClliente + " acaba de pasar a una caja      |");
    System.out.println("| Cajera " + Thread.currentThread().getId() + " : Hola, Encontro lo que buscaba?  |");
    System.out.println(" --------------------------------------------- \n");
    // Recorre todo el carro simulando el escaneo de la caja
    for (int i = 1; i <= carroCompra.size(); i++) 
    {
      // Se procesa el pedido en X segundos
      this.esperarXsegundos(carroCompra.get(i-1));
      System.out.println("Cajera " + Thread.currentThread().getId() + " : " +
          " Procesado el producto " + (i) 
          + " del cliente " + idClliente + " -> Tiempo: " + carroCompra.get(i-1) + " seg");
          tiempoNecesitado += carroCompra.get(i-1);
    }
    // Indican que termino la compra
    System.out.println("\n>>>> El cliente " + idClliente + " ha terminado en un tiempo de " + tiempoNecesitado + " seg");
    System.out.println(">>>> Cajera " + Thread.currentThread().getId() + " : SIGUIENTE!\n");
  }
}