// Cliente
import java.util.ArrayList;

public class Cliente {

	private String nombre;
	private ArrayList <Integer> carroCompra; // Arreglo con cantidad en segundos que se tarda la cajera en registrar el producto

	public Cliente() {
	}

	public Cliente(String nombre, ArrayList <Integer> carroCompra) {
		this.nombre = nombre;
		this.carroCompra = carroCompra;
	}

	public String getNombre() {
		return nombre;
	}

	public void setNombre(String nombre) {
		this.nombre = nombre;
	}

	public ArrayList <Integer> getCarroCompra() {
		return carroCompra;
	}

	public void setCarroCompra(ArrayList <Integer> carroCompra) {
		this.carroCompra = carroCompra;
	}

	public int getSizeCarroCompra()
	{
		return carroCompra.size();
	}

}
