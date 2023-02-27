#Andre marroquin, Gabriel paz, Andy fuentes.
#HDT 5
import simpy
import random
import statistics

RANDOM_SEED = 25
RAM_SIZE = 100 # tamanio de la memoria RAM en MB
CPU_SPEED = 3 # velocidad del CPU en unidades de tiempo por instruc
N_PROCESSES = 200 # cantidad de procesos a simular
SIM_TIME = 1000000 # tiempo total de simulación
INTERVAL = 10 # intervalo de tiempo para la llegada de nuevos procesos
N_CPUS = 1 # cantidad de procesadores en el sistema

# variables para almacenar estadisticas
wait_times = []
turnaround_times = []
response_times = []

# función que simula el proceso
def process(env, name, cpu, ram, instr):
    global wait_times, turnaround_times, response_times
    mem = random.randint(1, 10) 
    print(f"{name} solicita {mem} MB de memoria RAM en t={env.now}")
    yield ram.get(mem) 
    print(f"{name} obtiene {mem} MB de memoria RAM en t={env.now}")
    ready_time = env.now
    print(f"{name} pasa al estado 'ready' en t={env.now}")
    while instr > 0:
        with cpu.request() as req:
            yield req
            print(f"{name} comienza a ejecutarse en t={env.now}")
            for i in range(min(CPU_SPEED, instr)):
                yield env.timeout(1) 
            instr -= CPU_SPEED
            print(f"{name} lleva {max(0, instr)} instrucciones pendientes")
            if instr > 0:
                print(f"{name} vuelve al estado 'ready' en t={env.now}")
                ready_time = env.now

    ram.put(mem) 
    print(f"{name} finaliza en t={env.now}")
    wait_times.append(ready_time)
    turnaround_times.append(env.now - ready_time)
    response_times.append(ready_time - env.now + CPU_SPEED)



