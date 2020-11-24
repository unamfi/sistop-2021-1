/*
	Clase Main
	Controla el flujo del programa como el semaforo de hilos
*/

// Paquetes
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.util.Scanner;

public class Main 
{

	// Metodo para simular limpiar la pantalla
	public void cls()
	{
		System.out.print("\033[H\033[2J");  
    	System.out.flush();
	}

	// Metodo para imprimir paralabras en AsciiArt
	// Obtenido de: https://mkyong.com/java/ascii-art-java-example/
	public void asciiArt(String palabra)
	{
		this.cls();
		System.out.println("*******************************************************************");
		int width = 50;
        int height = 150;
        //BufferedImage image = ImageIO.read(new File("/Users/mkyong/Desktop/logo.jpg"));
        BufferedImage image = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        Graphics g = image.getGraphics();
        g.setFont(new Font("SansSerif", Font.BOLD, 14));

        Graphics2D graphics = (Graphics2D) g;
        graphics.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING,
                RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        graphics.drawString(palabra, 10, 20);

        for (int y = 0; y < height; y++) {
            StringBuilder sb = new StringBuilder();
            for (int x = 0; x < width; x++) {

                sb.append(image.getRGB(x, y) == -16777216 ? " " : "$");

            }

            if (sb.toString().trim().isEmpty()) {
                continue;
            }

            System.out.println(sb);
        }
        System.out.println("*******************************************************************");
      
	}

	// Metodo que cuenta con el ExecutorService que es el encargado de controlar el semaforo
	// que siguen los hilos (clientes) para realizar sus tareas (pasar con las cajeras)
	public void inicio(int numClientes)
	{
		long initialTime = System.currentTimeMillis(); // Tiempo inicial
    	Cajeras cajeras = new Cajeras(); // Usaremos la misma referencia para que todos accedan a la misma tienda.
    	ExecutorService ejecutor = Executors.newFixedThreadPool(3); // Se define que son 3 cajeras
    	// Se forman los clientes y esperan su turno segun las cajeras se desocupan
    	for (int i = 1; i <= numClientes; i++) 
      		ejecutor.execute(new Clientes(i, cajeras));
   		ejecutor.shutdown(); // Una vez sin clientes, se apaga el semaforo
    	while (!ejecutor.isTerminated()); // Todo esto se realiza mientras el executor no haya termindado

    	System.out.println("\n >>> Tiempo Transcurrido Total: " + (System.currentTimeMillis() - initialTime) / 1000 + " seg <<<");
	}

	// Funcion principal que permite simular cuantas veces uno quiera
	public static void main (String[] args)
	{
		Main superMercado = new Main();
		Scanner sc = new Scanner(System.in);
		int opc = 0;
		int numClientes = 0;

		while(opc == 0)
		{
			try
			{
				superMercado.asciiArt("Super");
				System.out.println(" >>> Hola!, Bienvenido a esta simulacion de Cajas Express de un supermercado");
				System.out.print("Numero de Clientes: ");
				numClientes =  sc.nextInt();
    			superMercado.inicio(numClientes);		
    			System.out.println("****** Desea volver a simular? ******");
    			System.out.println("0.- SI    1.- NO");
    			System.out.print("Opcion (0,1): ");
    			opc = sc.nextInt();
    		} catch (java.util.InputMismatchException IME)
    		{
    			System.out.println("Error");
    			opc = 1;
    		}
		}
		superMercado.cls();
		superMercado.asciiArt("Adios");
  	}
}