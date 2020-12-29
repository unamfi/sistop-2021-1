class CConsumidorMuestras extends Thread{
	private Muestras m;
	private int aleatorio;

	public CConsumidorMuestras(String name, Muestras c){
		m = c;
		setName(name);
	}

	public void run(){
		while (true) {
			aleatorio = (int)(Math.random()*100);
			if (aleatorio >= 30) {
				break;
			} else {	
				m.DespachaMuestra(getName());//obtener el ultimo mensaje
				try{
					sleep((int)(Math.random()*300));
				} catch (InterruptedException e) {}
			}
		}
	}
}