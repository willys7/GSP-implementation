import re
from claw import claw
from Block import Block


def read_file(init, final):
    file = open(init, 'r')
    init_state = []
    final_state = []
    for line in file:
        temp = re.split(r'\W+', line)
        if '' in temp:
            temp.remove("")
        init_state.append(temp)
    file.close()

    file = open(final, 'r')
    for line in file:
        temp = re.split(r'\W+', line)
        if '' in temp:
            temp.remove("")
        final_state.append(temp)
    file.close()

    return init_state, final_state



def verify_predicate(to_check, claw, current_state=[]):
    """
    verifica si se cumple el predicado a evaluar
    """
    tst = to_check[to_check.index('(')+1:to_check.index(')')]
    block_names = re.split(',', tst)
    iterar = True
    cont = 1
    if to_check.startswith('ONTABLE'):
        pass
    elif to_check.startswith('ON'):
        cont = 2
    elif to_check.startswith('CLEAR'):
        cont = 3
    elif to_check.startswith('HOLDING'):
        iterar = False
        cont = 4
    elif to_check.startswith('ARMEMPTY'):
        iterar = False
        cont = 5

    if iterar:
        #check onTable
        if cont == 1:
            for torre in current_state:
                if torre[0] == block_names[0]:
                    return True

        #check ON
        elif cont == 2:
            for torre in current_state:
                if block_names[0] in torre:
                    ind = torre.index(block_names[0])
                    if ind > 0:
                        under = torre[ind-1]
                        if block_names[1] == under:
                            return True

        #check clear
        elif cont == 3:
            for torre in current_state:
                if block_names[0] in torre:
                    ind = torre.index(block_names[0])
                    if ind == (len(torre)-1):
                        return True
        return False
    else:
        if cont == 4:
            if claw.is_empty() == False:
                if claw.holding == block_names[0]:
                    return True
        elif cont == 5:
            return claw.is_empty()
        return False


def get_relevant_actions(to_check, current_state, claw):
    """
    este metodo regresa las acciones relevantes para que se cumpla el predicado
    que se esta evaluando asi como sus precondiciones
    """
    tst = to_check[to_check.index('(')+1:to_check.index(')')]
    block_names = re.split(',', tst)
    to_execute = []
    b1_name = block_names[0]
    if to_check.startswith('ONTABLE'):
        to_execute.append('PUTDOWN({})'.format(b1_name))
        to_execute.append('HOLDING({})'.format(b1_name))
        for torre in current_state:
            if b1_name in torre:
                ind = torre.index(b1_name)
                to_execute.append('UNSTACK({},{})'.format(b1_name, torre[ind-1]))
                to_execute.append('ARMEMPTY(@)')
                to_execute.append('CLEAR({})'.format(b1_name))
                to_execute.append('ON({},{})'.format(b1_name, torre[ind-1]))

    elif to_check.startswith('ON'):
        to_execute.append('STACK({},{})'.format(b1_name, block_names[1]))
        to_execute.append('HOLDING({})'.format(b1_name))
        to_execute.append('CLEAR({})'.format(block_names[1]))

    elif to_check.startswith('CLEAR'):
        for torre in current_state:
            if b1_name in torre:
                ind = torre.index(b1_name)
                to_execute.append('UNSTACK({},{})'.format(torre[ind+1], b1_name))
                to_execute.append('ARMEMPTY(@)')
                to_execute.append('CLEAR({})'.format(torre[ind+1]))
                to_execute.append('ON({},{})'.format(torre[ind+1], b1_name))

    elif to_check.startswith('HOLDING'):
        to_execute.append('PICKUP({})'.format(b1_name))
        to_execute.append('ARMEMPTY(@)')
        to_execute.append('ONTABLE({})'.format(b1_name))
        to_execute.append('CLEAR({})'.format(b1_name))

    elif to_check.startswith('ARMEMPTY'):
        to_execute.append('PUTDOWN({})'.format(claw.holding))
        to_execute.append('HOLDING({})'.format(claw.holding))
    return to_execute

def apply_action(to_apply, current_state, claw):
    """
    hace cambios al estado actual en base a la accion
    recibida como param
    """
    tst = to_apply[to_apply.index('(')+1:to_apply.index(')')]
    block_names = re.split(',', tst)
    b1_name = block_names[0]
    if to_apply.startswith('STACK'):
        for torre in current_state:
            if b1_name in torre:
                torre.remove(b1_name)
            if block_names[1] in torre:
                torre.append(b1_name)
        claw.put_down(claw.holding)

    elif to_apply.startswith('UNSTACK'):
        for torre in current_state:
            if b1_name in torre:
                torre.remove(b1_name)
        #nt = [b1_name]
        claw.pickup(b1_name)
        #current_state.append(nt)

    elif to_apply.startswith('PICKUP'):
        claw.pickup(b1_name)
        for torre in current_state:
            if b1_name in torre:
                torre.remove(b1_name)


    elif to_apply.startswith('PUTDOWN'):
        claw.put_down(b1_name)
        nt = [b1_name]
        current_state.append(nt)

    return current_state

