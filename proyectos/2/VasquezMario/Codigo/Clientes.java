/* 
  Clase Clientes (implementa la Interfaz Runnable que nos permite manejar Hilos con su metodo run)
  Los clientes tienen:
  - id asignado automaticamente por la empresa,
  - Carro de compras: Se definio que los clientes tendran entre 1 a 10 productos en su carro de compras
  - Contiene un semafaro que le indicara la disponibilidad de las cajeras
  - Todos los clientes tendran el mismo objeto Cajeras (Para simular que son las mismas cajeras que los atienden)
*/

// Paquetes
import java.util.concurrent.Semaphore;
import java.util.ArrayList;

public class Clientes implements Runnable
{
  // Atributos
  int idCliente;
  Cajeras cajeras;
  ArrayList <Integer> carroCompra; // Arreglo con cantidad en segundos que se tarda la cajera en registrar el producto
  static int numeroCajeras = 3; // Numero de Cajeras.
  static Semaphore semaforo = new Semaphore(numeroCajeras);

  // Metodos
  // Constructor: Genera los clientes con su respectivo Carrito de Compras
  public Clientes(int id, Cajeras cajera){
    this.idCliente = id;
    this.cajeras = cajera;
    // Se crea la lista del carro de compras
    this.carroCompra= new ArrayList<Integer>();
    // Se agregan 1 o 10 elementos a su carrito de compras
    for (int j = 0; j< (int)(Math.random() * 10 + 1); j++ )
      // Tiempo que la cajera se tardara en cada elemento del carrito de compras (entre 1 y 8 seg)
      this.carroCompra.add((int)(Math.random() * 8 + 1));
  }

  // Metodo run (Nos permite indicar que hacen los clientes (hilos) una vez creados)
  public void run(){
    try {
      semaforo.acquire(); // El cliente (Hilo) va con una cajera, si es que esta desocupada
      this.cajeras.Comprar(this.idCliente,this.carroCompra); // La cajera empieza a comprar 
      } catch (InterruptedException E) {}
    semaforo.release(); // Se notifica que acabo de comprar y la Cajera esta libre
  }

}
