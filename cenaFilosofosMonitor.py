import threading
import keyboard
import os
from time import sleep

# Finaliza el programa forzosamente.
def finalizar_programa():
    print('\nPresionaste la tecla "Esc", terminando el programa...\n')
    os._exit(0)

# Monitor para facilitar la adquisición de palillos entre los filósofos.
class Mesero():
    def __init__(self):
        self.condiciones = list()
    
    def registra_filosofos(self, filosofos):
        self.filosofos = filosofos 
        self.numero_filosofos = len(filosofos)
        for _ in range(self.numero_filosofos):
            self.condiciones.append(threading.Condition())

    def empieza_cena(self):
        for i in range(self.numero_filosofos):
            self.filosofos[i].start()

    def comienza_comer(self, id):
        with self.condiciones[id]:
            permite_comer = self.__permite_comer(id)
            if not permite_comer:
                self.condiciones[id].wait()

    def __permite_comer(self, id):
        return self.filosofos[id].estado == "HAMBRIENTO" \
                and self.get_vecino_izquierdo(id).estado != "COMIENDO" \
                    and self.get_vecino_derecho(id).estado != "COMIENDO"
    
    def termina_comer(self, id):
        id_vecino_izquierdo = self.get_id_vecino_izquierdo(id)
        with self.condiciones[id_vecino_izquierdo]:
            self.condiciones[id_vecino_izquierdo].notify()
        id_vecino_derecho = self.get_id_vecino_derecho(id)
        with self.condiciones[id_vecino_derecho]:
            self.condiciones[id_vecino_derecho].notify()

    def get_vecino_izquierdo(self, id):
        return self.filosofos[self.get_id_vecino_izquierdo(id)]
    
    def get_vecino_derecho(self, id):
        return self.filosofos[self.get_id_vecino_derecho(id)]

    def get_id_vecino_izquierdo(self, id):
        return (id + self.numero_filosofos - 1) % self.numero_filosofos
    
    def get_id_vecino_derecho(self, id):
        return (id + 1) % self.numero_filosofos

mesero = Mesero() # Llamado al monitor previo.

# Estados:  PENSANDO -> HAMBRIENTO -> COMIENDO
class Filosofo(threading.Thread):
    def __init__(self, id, mesero, num_tiempo_come, tiempo_come, tiempo_piensa):
        threading.Thread.__init__(self)
        self.tiempo_come = tiempo_come
        self.tiempo_piensa = tiempo_piensa
        self.id = id
        self.num_tiempo_come = num_tiempo_come
        self.mesero = mesero # monitor 
        self.estado = None

    def run(self):
        num_tiempo_come = 0
        while num_tiempo_come != self.num_tiempo_come:
            self.piensa()
            self.tiene_hambre()
            self.come()
            num_tiempo_come += 1
            print("Filosofo %i comió %i veces."% (self.id, num_tiempo_come))
        self.estado = "FIN"

    def piensa(self):
        self.estado = "PENSANDO"
        print("Filosofo %i está pensando."%self.id)
        sleep(self.tiempo_piensa)

    def tiene_hambre(self):
        print("Filosofo %i tiene hambre."%self.id)
        self.estado = "HAMBRIENTO"

    def come(self):
        self.mesero.comienza_comer(self.id)
        self.estado = "COMIENDO"
        print("Filosofo %i está comiendo."%self.id)
        sleep(self.tiempo_come)
        self.mesero.termina_comer(self.id)

p0 = Filosofo(id = 0, mesero = mesero, num_tiempo_come = 10, tiempo_come = 1, tiempo_piensa = 1)
p1 = Filosofo(id = 1, mesero = mesero, num_tiempo_come = 2, tiempo_come = 2, tiempo_piensa = 2)
p2 = Filosofo(id = 2, mesero = mesero, num_tiempo_come = 3, tiempo_come = 3, tiempo_piensa = 5)
p3 = Filosofo(id = 3, mesero = mesero, num_tiempo_come = 1, tiempo_come = 1, tiempo_piensa = 2)
p4 = Filosofo(id = 4, mesero = mesero, num_tiempo_come = 2, tiempo_come = 5, tiempo_piensa = 2)

filosofos = [p0, p1, p2, p3, p4]
mesero.registra_filosofos(filosofos)
mesero.empieza_cena()

# Para finalizar el programa presionando la tecla Esc
keyboard.add_hotkey('escape', finalizar_programa)