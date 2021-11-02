import threading
import time
import random
import keyboard
import os

# Finaliza el programa forzosamente.
def finalizar_programa():
    print('\nPresionaste la tecla "Esc", terminando el programa...\n')
    os._exit(0)

class Filosofo(threading.Thread):

    # Semáforo para facilitar la adquisición y liberación de los palillos.
    sentados = threading.Semaphore(4)

    # Inicialización de los palillos.
    def __init__(self, palillo_izquierdo, palillo_derecho, nombre):
        super().__init__()
        self.palillo_izquierdo = palillo_izquierdo
        self.palillo_derecho = palillo_derecho
        self.nombre = nombre
        print(f'Filósofo {self.nombre} se sentó en la mesa')

    # Simula el comportamiento o estado de los filósofos
    def run(self):
        print(f'Filósofo {self.nombre} comenzó a Pensar')
        comida = 0
        while comida < 20: # Ciclo "cerrado" para evitar corridas eternas.
            pensar = random.randint(1,5)
            print(f'Filósofo {self.nombre} terminó de pensar tras', pensar, 'segundos.')
            self.sentados.acquire() # Inicialización del semáforo para permitir el paso de palillos.
            try:
                self.palillo_izquierdo.acquire()
                try:
                    print(f'Filósofo {self.nombre} obtuvo el palillo Izquierdo tras', pensar, 'segundos.')
                    self.palillo_derecho.acquire()
                    try:
                        print(f'Filósofo {self.nombre} los dos palillos y esta comiendo tras', pensar, 'segundos.')
                    finally:
                        self.palillo_derecho.release()
                        print(f'Filósofo {self.nombre} liberó el palillo Derecho tras', pensar, 'segundos.')
                finally:
                    self.palillo_izquierdo.release()
                    print(f'Filósofo {self.nombre} liberó el palillo Izquierdo tras', pensar, 'segundos.')
            finally:
                self.sentados.release()
            
        comida += 1

# Para finalizar el programa presionando la tecla Esc
keyboard.add_hotkey('escape', finalizar_programa)

def main():
    # filosofos = []
    threads = []
    tenedor = [threading.RLock() for i in range(5)]
    nombres = ["Socrates", "Platón", "Aristóteles", "Locke", "Descartes"]

    for i in range(5):
        time.sleep(random.randint(1,2))
        filosofo = Filosofo(tenedor[i], tenedor[(i+1) % 5], nombres[i])
        threads.append(filosofo)
        filosofo.start()

    for i in threads:
        i.join()

if __name__=='__main__':
    main()