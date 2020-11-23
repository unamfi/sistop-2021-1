import java.util.concurrent.Semaphore;
import java.util.ArrayList;

public class Clientes implements Runnable{
  int idCliente;
  Cajeras cajeras;
  ArrayList <Integer> carroCompra; // Arreglo con cantidad en segundos que se tarda la cajera en registrar el producto
  static int numeroCajeras = 3; // Numero de Cajeras.
  static Semaphore semaforo = new Semaphore(numeroCajeras);

  public Clientes(int id, Cajeras cajera){
    this.idCliente = id;
    this.cajeras = cajera;
    // Se crea la lista del carro de compras
    this.carroCompra= new ArrayList<Integer>();
    // Se agregan 1 o 5 elementos a su carrito de compras
    for (int j = 0; j< (int)(Math.random() * 4 + 1); j++ )
      // Tiempo que la cajera se tardara en cada elemento del carrito de compras 
      this.carroCompra.add((int)(Math.random() * 5 + 1));
  }

  public void run(){
    try {
      semaforo.acquire(); // El cliente (Hilo) va con una cajera, si es que esta desocupada
      this.cajeras.Comprar(this.idCliente,this.carroCompra); // La cajera empieza a comprar 
      } catch (InterruptedException E) {}
    semaforo.release(); // Se notifica que acabo de comprar y la Cajera esta libre
  }

}
