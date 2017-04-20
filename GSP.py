from funciones import *

def GSP(init_state, final_state, PREDICATES):
    """
    Implementacion de Gold Stack Planning
    """
    stack = []
    plan = []
    actual_state = init_state
    blocks = []
    #le llamo tower a cada una de las torreo o elemento unicos que tengo en mi estado inicial
    for tower in init_state:
        #veo de que tmanio es la torre que tengo en cada una de las posiciones
        cont_block = len(tower)
        for block in range(cont_block):
            on_table = False
            clear = True
            current_block = tower[block]
            if block+1 < cont_block:
                clear = False

            if block < 1:
                on_table = True
            else:
                pass
            prop = {'name': current_block, 'onTable': on_table, 'clear':clear}
            btmp = Block(current_block, prop)
            blocks.append(btmp)

    #Ya que conozco el estado inicar
    #Ahora veo el estado final y lo paso a preposiciones
    #para saber a lo que debo llegar

    complex_goal = ''

    for tower in final_state:
        #veo de que tmanio es la torre que tengo en cada una de las posiciones
        cont_block = len(tower)
        state = ''
        for block in range(cont_block):
            current_block = tower[block]

            if block-1 >= 0:
                state += 'ON({},{})^'.format(current_block, tower[block-1])
            if block < 1:
                state += 'ONTABLE({})^'.format(current_block)
        complex_goal += state

    complex_goal = complex_goal[:-1]
    sub_goals = re.split(r'\^', complex_goal)
    stack.append(complex_goal)

    #agregar las subgoals al stack
    for goal in sub_goals:
        stack.append(goal)

    #Ya con los goals y los subgoals
    #tambien con las proposicones procedemos a resolver
    the_claw = claw()
    while stack:
        for tower in actual_state:
            if len(tower) < 1:
                actual_state.remove(tower)
        accion_actual = stack.pop()
        ind = accion_actual.index('(')
        pred = '@'
        if ind > 0:
            pred = accion_actual[:ind]
        print accion_actual
        if pred in PREDICATES:
            if '^' in accion_actual:
                tmp_gls = re.split(r'\^', accion_actual)
                cumplido = True
                for meta in tmp_gls:
                    cumplido = cumplido and verify_predicate(meta, the_claw, actual_state)

            else:
                cumplido = verify_predicate(accion_actual, the_claw, actual_state)
                if cumplido == False:
                    rest = get_relevant_actions(accion_actual, actual_state, the_claw)
                    stack.extend(rest)

        #Si no es una precondicion entonces implica que 
        #estamos tratando con una accion.
        else:
            actual_state = apply_action(accion_actual, actual_state, the_claw)
            print "Nuevo estado"
            print actual_state
            plan.append(accion_actual)
    return plan, actual_state
