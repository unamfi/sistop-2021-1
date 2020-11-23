import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.ArrayList;

public class Cajeras {

  // Duerme el hilo X segundos
  private void esperarXsegundos(int segundos) {
    try {
      Thread.sleep(segundos * 1000);
    } catch (InterruptedException ex) {
      System.out.println("El cliente era un ladron y se fue sin pagar (Protocolo cerrar Changarro)");
      Thread.currentThread().interrupt();
    }
  }

  public void Comprar(int idClliente,ArrayList <Integer> carroCompra) {
    int tiempoNecesitado = 0;
      System.out.println("El cliente " + idClliente + " acaba de pasar a una caja");
      for (int i = 1; i <= carroCompra.size(); i++) 
      {
      // Se procesa el pedido en X segundos
        this.esperarXsegundos(carroCompra.get(i-1));
        System.out.println("Cajera: " + Thread.currentThread().getId() +
            " Procesado el producto " + (i) 
            + " del cliente " + idClliente + "->Tiempo: ");
        tiempoNecesitado += carroCompra.get(i-1);
      }

      System.out.println("El cliente " + idClliente + " ha terminado en un tiempo de" + tiempoNecesitado + "seg");
  }

  public static void main(String[] args) {
    Cajeras cajeras = new Cajeras(); // Usaremos la misma referencia para que todos accedan a la misma tienda.
    ExecutorService ejecutor = Executors.newFixedThreadPool(3);
    for (int i = 1; i <= 10; i++) {
      ejecutor.execute(new Clientes(i, cajeras));
    }
    ejecutor.shutdown();
    while (!ejecutor.isTerminated())
      ;
  }
}