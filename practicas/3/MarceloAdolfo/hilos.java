import java.util.*;
public class hilos extends Thread{
 Scanner dato = new Scanner(System.in);
 String n, d;
 double h;
  public hilos(String nombre, String dia, double hora){
    n=nombre;
    d=dia;
    h=hora;
 System.out.println("Ingrese el nombre del empleado :");
        n = dato.next();
        System.out.println("Ingrese el dia :");
        d = dato.next();
        System.out.println("Ingrese la hora :");
        h = dato.nextDouble();
 
 }
public void run(){
 if(h>8.00){
 System.out.println(n + " llego tarde el día " + d);
 }else{
 System.out.println(n + " llego temprano el día " + d);
 }
 }
 public static void main(String []args){
  Thread usuario1 = new hilos(" "," ",0);
    usuario1.start();
  Thread usuario2 = new hilos(" "," ",0);
    usuario2.start();
 }
}