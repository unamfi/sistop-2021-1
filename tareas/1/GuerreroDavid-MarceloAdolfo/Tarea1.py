import threading

#Se le solicita al usuario la cantidad de gatos
gatoInput = int(input("¿Cuántos gatos hay?: "))
#Se le solicita al usuario la cantidad de ratones
ratonInput = int(input("¿Cuántos ratones hay?: "))
#Se le solicita al usuario la cantidad de platos
platosInput = int(input("¿Cuántos platos hay?: "))

platos = [threading.Semaphore(1) for i in range(platosInput)]
animales = threading.Semaphore(platosInput)
entrada = threading.Semaphore(1)
mxGatosCuarto = threading.Semaphore(1) 
gatosCuarto = 0
ratonesCuarto = 0
mxRatonesCuarto = threading.Semaphore(1)
torniquete = threading.Semaphore(1)


ratonesMuertos = []
#Función del comportamiento del gato
def gatoEntrando(id):
	global platos,animales,entrada,mxGatosCuarto,gatosCuarto
	global ratonesCuarto,mxRatonesCuarto,torniquete
	torniquete.acquire()
	torniquete.release()
	entrada.acquire()
	mxGatosCuarto.acquire()
	gatosCuarto += 1
	mxGatosCuarto.release()
	platoDelGato(id)
	gatoAcabo(id)
	mxGatosCuarto.acquire()
	gatosCuarto -= 1
	mxGatosCuarto.release()
	entrada.release()
	print("Soy el gato " + str(id) + " y ya me fui")
#Función que le asigna plato al gato	
def platoDelGato(id):
	global platos,animales,entrada,mxGatosCuarto,gatosCuarto
	global ratonesCuarto,mxRatonesCuarto,torniquete
	animales.acquire()
	platos[(id)%platosInput].acquire()
	print("Soy el gato " + str(id) + "  y como en el plato: " + str((id)%platosInput))


#Función para que el gato suelte el plato
def gatoAcabo(id):
	global platos,animales,entrada,mxGatosCuarto,gatosCuarto
	global ratonesCuarto,mxRatonesCuarto,torniquete
	platos[(id)%platosInput].release()
	animales.release()

#Función del comportamiento del ratón	
def ratonEntrando(id):
	global platos,animales,entrada,mxGatosCuarto,gatosCuarto
	global ratonesCuarto,mxRatonesCuarto,torniquete
	torniquete.acquire()
	torniquete.release()
	mxGatosCuarto.acquire()
	if(gatosCuarto > 0):   
		print("Soy el ratón ",id,"y soy un confiando de la vida y comeré en el plato", (id)%platosInput, "\nSi me comieron, F en el chat")
		ratonesMuertos.append(id)
		mxGatosCuarto.release()
	else:
		mxGatosCuarto.release()
		mxRatonesCuarto.acquire()
		ratonesCuarto += 1
		if(ratonesCuarto == 1):
			entrada.acquire()
		mxRatonesCuarto.release()
		platoDelRaton(id)
		print("Soy el raton " + str(id) + "  y estoy comiendo en  el plato: " + str((id)%platosInput))
		ratonAcabo(id)
		mxRatonesCuarto.acquire()
		ratonesCuarto -= 1
		if(ratonesCuarto == 0):
			entrada.release()
		print("Soy el ratón ",id,"y ya me fui")
        

	
		mxRatonesCuarto.release()
#Función para agarrar el plato
def platoDelRaton(id):
	global platos,animales,entrada,mxGatosCuarto,gatosCuarto
	global ratonesCuarto,mxRatonesCuarto,torniquete
	animales.acquire()
	platos[(id)%platosInput].acquire()

#Función para que el raton suelte plato
def ratonAcabo(id):
	global platos,animales,entrada,mxGatosCuarto,gatosCuarto
	global ratonesCuarto,mxRatonesCuarto,torniquete
	platos[(id)%platosInput].release()
	animales.release()

#Función que imprime a los ratones muertos
def listaDeMuertos():
    ##Realizamos una contabilidad final de los pobres ratones caídos en batalla
    print("\nRatones Muertos: ")
    for y in ratonesMuertos:
        print("Ratón: ",y)  



#Asignacion de hilos para los gatos
for i in range(gatoInput):
    threading.Thread(target=gatoEntrando, args=[i+1]).start()

#Asignacion de hilos para los ratones
for i in range(ratonInput):
    threading.Thread(target=ratonEntrando, args=[i+1]).start()

#Conteo de los hilos
for thread in threading.enumerate():
    if thread.daemon:
        continue
    try:
        thread.join()
    except RuntimeError as err:
        if 'cannot join current thread' in err.args[0]:
            continue
        else:
            raise

listaDeMuertos()