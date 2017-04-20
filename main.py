from funciones import *
from GSP import *

init_state, final_state = read_file("inicio.txt", "final.txt")

#Obtengo cada uno de los estados, final e inical
print "Estado inicial"
print init_state
print "Estado Final"
print final_state

#defino una lista de predicados
PREDICATES = ['ON', 'ONTABLE', 'HOLDING', 'CLEAR', 'ARMEMPTY']

plan, actual_state = GSP(init_state, final_state, PREDICATES)
print "DEBE SEGUIR EL SIGUIENTE PLAN PARA RESOLVER \n"
print plan

if(actual_state != final_state):
    print "Cuidado con el plan porque existe una anomalia"