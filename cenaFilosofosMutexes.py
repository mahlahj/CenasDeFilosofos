import threading
import random
import time
import keyboard
import os

# El Deadlock se evita al nunca tener que esperar por un palillo mientras tenga uno en mano (locked)
# El procedimiento es bloquear (block) mientras espera a tener el primer palillo, y tener una adquisición no bloqueante
# (nonblocking) adquisición del segundo palillo.
# Si falla al obtener el segundo palillo, libera el primero, cambia al primero por el segundo y reintenta hasta obtener ambos.

# Finaliza el programa forzosamente.
def finalizar_programa():
    print('\nPresionaste la tecla "Esc", terminando el programa...\n')
    os._exit(0)

class Filosofo(threading.Thread):
 
    funcionando = True
 
    def __init__(self, nombre, palillo_izquierdo, palillo_derecho):
        threading.Thread.__init__(self)
        self.name = nombre
        self.palillo_izquierdo = palillo_izquierdo
        self.palillo_derecho = palillo_derecho
 
    def run(self):
        while(self.funcionando):
            #  Filosofo está pensando (aunque en realidad está "apagado").
            time.sleep( random.uniform(3,13))
            print (('%s está hambriento.') % self.name)
            self.cena()

    # Mutex arriba mencionado (cambio de palillo y búsqueda de adquisición.)
    def cena(self):
        palillo1, palillo2 = self.palillo_izquierdo, self.palillo_derecho
 
        while self.funcionando:
            palillo1.acquire(True)
            locked = palillo2.acquire(False)
            if locked: break
            palillo1.release()
            print (('%s cambia palillos') % self.name)
            palillo1, palillo2 = palillo2, palillo1
        else:
            return
 
        self.cenando()
        palillo2.release()
        palillo1.release()
 
    def cenando(self):			
        print (('%s comienza a comer ')% self.name)
        time.sleep(random.uniform(1,10))
        print (('%s termina de comer y empieza a filosofar.')% self.name)
 
def cenaFilosofos():
    palillos = [threading.Lock() for n in range(5)]
    nombres = ('Aristóteles','Sócrates','Platón','Nietzche', 'Kant')
 
    filosofos= [Filosofo(nombres[i], palillos[i%5], palillos[(i+1)%5]) \
            for i in range(5)]
 
    random.seed(507129)
    Filosofo.funcionando = True
    for f in filosofos: f.start()
    time.sleep(100)
    Filosofo.funcionando = False
    print ("Ya terminamos.")

# Para finalizar el programa presionando la tecla Esc
keyboard.add_hotkey('escape', finalizar_programa)

cenaFilosofos()