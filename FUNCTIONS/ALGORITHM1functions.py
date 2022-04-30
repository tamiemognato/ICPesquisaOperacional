import copy


def sort_entity_by_related_parameter_order_lesstomore(dictionary,entity,parameter):

    count_while_1 = 0
    list_of_list_ship_eta = []

    while count_while_1 < len(dictionary[entity]):                                           #Criando n listas para cada navio com [rótulo navio, eta navio] e adicionando a uma lista única
        list_by_list_ship_eta = []
        list_by_list_ship_eta.append(dictionary[entity][count_while_1])
        list_by_list_ship_eta.append(dictionary[parameter][count_while_1])
        list_of_list_ship_eta.append(tuple(list_by_list_ship_eta))
        count_while_1 += 1

    list_of_list_ship_eta.sort(key=lambda x: x[1])                                           #ordenando a lista de tuplas por meio do eta que ocupa a segunda posição, do menor para o maior

    return list_of_list_ship_eta


def select_current_entity(dictionary,position):
    aux_dic_current_entity = copy.deepcopy(dictionary)                                                    #cópia por valor
    list_of_keys = list(dictionary.keys())
    count = 1

    while count < len(dictionary):
        aux_dic_current_entity[list_of_keys[count]] = dictionary[list_of_keys[count]][position]
        count += 1

    dic_current_entity = copy.deepcopy(aux_dic_current_entity)

    return dic_current_entity



def saving_value_in_principal_entity_dictionary(principal_entity_dictionary,current_entity_dictionary):
    aux_actualized_principal_entity_dictionary = copy.deepcopy(principal_entity_dictionary)                                          #cópia por valor
    aux_current_entity_dictionary = copy.deepcopy(current_entity_dictionary)
    list_of_keys = list(aux_actualized_principal_entity_dictionary.keys())
    list_of_keys = list_of_keys[1:]

    for key in list_of_keys:
        aux_actualized_principal_entity_dictionary[key][aux_current_entity_dictionary[list_of_keys[0]]] = aux_current_entity_dictionary[key]

    actualized_principal_entity_dictionary = copy.deepcopy(aux_actualized_principal_entity_dictionary)

    return actualized_principal_entity_dictionary

def saving_value_in_dic_berth(dic_berth,current_berth):
    aux_actualized_dic_berth = copy.deepcopy(dic_berth)                                                                                    #cópia por valor
    aux_current_berth = copy.deepcopy(current_berth)

    contador = len(aux_current_berth['ships_scheduled'])

    if aux_current_berth['berths'] == 0:
        aux_actualized_dic_berth['ships_scheduled'][0].append(aux_current_berth['ships_scheduled'][contador-1])
        aux_actualized_dic_berth['arrival_time_berth'][0].append(aux_current_berth['arrival_time_berth'][contador - 1])
        #aux_actualized_dic_berth['time_departure'][0].append(aux_current_berth['time_departure'][contador - 1])
    else:
        aux_actualized_dic_berth['ships_scheduled'][1].append(aux_current_berth['ships_scheduled'][contador-1])
        aux_actualized_dic_berth['arrival_time_berth'][1].append(aux_current_berth['arrival_time_berth'][contador - 1])
        #aux_actualized_dic_berth['time_departure'][1].append(aux_current_berth['time_departure'][contador - 1])

    actualized_dic_berth = copy.deepcopy(aux_actualized_dic_berth)

    return actualized_dic_berth


def min_time_arr_at_berth(list_time_departure_of_current_berth, int_eta_ship_of_current_ship):    #(current_berth['time_departure'],current_ship['eta_ship'])
    aux_list_departure_of_current_berth = copy.deepcopy(list_time_departure_of_current_berth)
    aux_int_eta_ship_of_current_ship = int_eta_ship_of_current_ship

    count = 0
    while count < len(aux_list_departure_of_current_berth):
        if (aux_list_departure_of_current_berth[count] + 1) < aux_int_eta_ship_of_current_ship:
            del(aux_list_departure_of_current_berth[count])
        count += 1

    if aux_list_departure_of_current_berth == []:
        min_time_arr = int_eta_ship_of_current_ship
    else:
        min_time_arr = max(aux_list_departure_of_current_berth) + 1

    return min_time_arr

def sort_stockpiles_in_order_stockpiles_ship_by_rec_sequence(order_stockpiles_ship_list,V):
    aux_order_stockpiles_ship_list = copy.deepcopy(order_stockpiles_ship_list)
    sorted_order_stockpiles_ship = []
    for v in V:
        sorted_order_stockpiles_ship.append(aux_order_stockpiles_ship_list[v[0]])

    return sorted_order_stockpiles_ship


#################################################### QUASE APROVADAS ##################################################


def list_of_real_and_dummy_stockpiles_already_located_in_the_stockyard(dummy_dic_pad):
    #time rec finishes > southernmost pad > lowest position
    #(time_rec_finish, pad, position_pad, stokpiles_on_time)

    list_of_tuples_stockpile_pad_timefinrec_dr = []

    for p in dummy_dic_pad['pads']: #para cada pad
        count = 0
        if len(dummy_dic_pad['stockpiles'][p]) > 0: #se o pad n estiver vazio

            while count < len(dummy_dic_pad['stockpiles'][p]): #para cada pilha no pad
                list_by_list_stockpile_pad_timefinrec_dr = [] #crie uma lista
                list_by_list_stockpile_pad_timefinrec_dr.append(dummy_dic_pad['time_rec_finish'][p][count]) #adicione a ela a o tempo que a pilha termina de ser recuperada
                list_by_list_stockpile_pad_timefinrec_dr.append(p) #adicione a ela o pad que a pilha está
                list_by_list_stockpile_pad_timefinrec_dr.append(dummy_dic_pad['position_pad'][p][count])  #adicione a ela a posição em que essa pilha está no pad
                list_by_list_stockpile_pad_timefinrec_dr.append(dummy_dic_pad['stockpiles'][p][count]) #adicione a ela o código dessa pilha
                list_by_list_stockpile_pad_timefinrec_dr.append(dummy_dic_pad['length_stockpile'][p][count])  #adicione a ela o comprimento dessa pilha
                list_of_tuples_stockpile_pad_timefinrec_dr.append(tuple(list_by_list_stockpile_pad_timefinrec_dr)) #transforme isso tudo numa tupla dessa pilha
                count += 1

    list_of_tuples_stockpile_pad_timefinrec_dr.sort(key=lambda x: x[0])  #ordene pelo tempo de fim de recuperação !!!!!!!!!!! ponto para checar

    return list_of_tuples_stockpile_pad_timefinrec_dr


def list_of_real_and_dummy_stockpiles_located_on_pad_p_ordered_by_position(S_LINHA, p):
    count = 0
    S_DUASLINHAS = []

    while count < len(S_LINHA): #para cada s_linha em S_LINHA
        if S_LINHA[count][1] == p:   #se o pad de s_linha for igual a ao pad p em questão
            S_DUASLINHAS.append(S_LINHA[count])   #então adicione ela a lista S_DUASLINHAS
        count += 1

    S_DUASLINHAS.sort(key=lambda  x: x[2]) #ordene a lista de pilhas no pad p pela posição h !!!!!!!!!!! ponto para checar

    return S_DUASLINHAS


def returning_time_build_s_finish(current_ship, dic_stockpile):
    last_s_of_v_index = current_ship['order_stockpiles_ship'][-1]  #Salvar o index da última pilha de v
    for s in current_ship['order_stockpiles_ship']:
        list_of_movements_for_s = copy.deepcopy(dic_stockpile['n_coalmov_lp_time'][s])  # Copio a lista de carregamentos para s
        list_of_movements_for_s.sort(key=lambda x: x[4])  # Organizo do menor para o maior tempo de movimento
        #print(list_of_movements_for_s)
        last_coal_movement_time = list_of_movements_for_s[-1][4]  # Seleciono o último tempo de carregamento
        #print(last_coal_movement_time)
        time_build_finish_s = last_coal_movement_time + 24  # Adiciono 1 dia a ele !!!!!!!!!GRANULARIDADE
        #print(time_build_finish_s)

        dic_stockpile['time_build_finish'][s] = time_build_finish_s


    return




########################################## EM TESTE ###################################################################


def does_s_not_conflict_with_any_other_stockpile_on_p(p,h,t,dummy_dic_pad,infinite):
    #position - lower_limit = h and upper_limit = h + dummy_dic_pad['length_stockpile'][p][-1] + dummy_dic_pad['distance_between_stockpiles'][p]
    # [0,510]
    #time - lower limit = t and upper_limit = dic_instance['infinite']
    #imprimir figura, exemplo fig 4 do alg 1
    returnable = False
    #[0,3] h
    count = 0
    #print('TESTE DE POSIÇÃO 148:', h, '<=', dummy_dic_pad['position_pad'][p][count], '<=', h + dummy_dic_pad['length_stockpile'][p][-1] + dummy_dic_pad['distance_between_stockpiles'][p])
    while count < len(dummy_dic_pad['stockpiles'][p][:-1]):
        if (h <= dummy_dic_pad['position_pad'][p][count] <= h + dummy_dic_pad['length_stockpile'][p][-1] + dummy_dic_pad['distance_between_stockpiles'][p]):
            #print('TESTE DE POSIÇÃO 151:',h,'<=',dummy_dic_pad['position_pad'][p][count],'<=', h + dummy_dic_pad['length_stockpile'][p][-1] + dummy_dic_pad['distance_between_stockpiles'][p])
            #if (t < dummy_dic_pad['time_rec_finish'][p][count] < infinite):
            #print('TESTE DE POSIÇÃO 153:',t, '<', dummy_dic_pad['time_rec_finish'][p][count], '<', infinite)
            returnable = True
            break
        count += 1

    return returnable


def at_least_one_coal_movement_can_be_carried_out_for_s_on_day_t(t_starts,dic_load_point,s):  #talvez seja bom dividir em duas funções
    tem_capacidade = True #for t in dic_load_point['t_scheduled_coal_movement'][tupla[0]] se tiver vazio n roda o q significa q n tem nada marcado então tem capaciadade
    count = 0
    list_of_tuples_with_lp_and_tonnage_s_needs = []
    while count < len(dic_load_point['tonnage_mov_stockpile_lp'][s]):   #estou pegando cada elemento da lista de toneladas que s precisa de l0 e l1, exemplo para s=1 temos [10, 0]
        #print('estou dentro do while', count)
        if dic_load_point['tonnage_mov_stockpile_lp'][s][count] > 0:  #se o elemento for maior que 0 significa que s precisa do carragamento do l respectivo, se for 0 nem precisamos testar
            #print('estou dentro do dic_load_point[tonnage_mov_stockpile_lp][s][count] > 0', dic_load_point['tonnage_mov_stockpile_lp'][s][count])
            tupla_aux = []
            tupla_aux.append(count)  #adiciono a posição que representa l ex 0
            tupla_aux.append(dic_load_point['tonnage_mov_stockpile_lp'][s][count])  #adiciono o peso em toneladas q s precisa de l ex 10
            list_of_tuples_with_lp_and_tonnage_s_needs.append(tuple(tupla_aux))  #aqui eu tenho uma lista de tuplas somente dos load points e suas respectivas toneladas que s precisa, ex [(0,10)] (load point, tonelada)
        count +=1

    for tupla in list_of_tuples_with_lp_and_tonnage_s_needs: #para toda tupla que contém os load points de q s precisa de movimento
        #print('estou dentro do for tupla', tupla)
        ########### !!!!!!!!!!!! conferir essa parte após atualização do procedimento 3
        for t in dic_load_point['t_scheduled_coal_movement'][tupla[0]]: #para td tempo dentro na lista de tempos com movimentos marcados para, exemplo, o load point tupla[0] = 0
            #print('estou dentro do for t', t , dic_load_point['t_scheduled_coal_movement'][tupla[0]])
            if t == t_starts:  #exemplo se 12 == 12, então significa q no dia representado por 12 q estamos testando já tem alguma carregamento marcado para o load point l = 0
                #print('estou dentro do t == t_starts')
                posicao = dic_load_point['t_scheduled_coal_movement'][tupla[0]].index(t)  #eu guardo a posição desse tempo, e aqui usar index dá certo pq eu n vou ter uma lista de tempos repetidos, no procedimento 3 vou usar esse msm raciocnio para atualizar
                res_cap = dic_load_point['res_cap_tonnage_l'][tupla[0]][posicao] #e faço a diferença entre a capacidade residual de l no tempo t - a tonelagem que s precisa de l
                diferenca = res_cap - tupla[1]
                #print(diferenca)
                if diferenca >= 0: #se essa diferença for maior ou igual a 0 siginifica que l tem capaciade de pelo menos 1 movimento
                    #print('diferenca >= 0')
                    tem_capacidade = True

                else:   #se for < 0 então não tem capacidade. Exemplo: 40 de 50 - 40 = 0, pode pelo menos 1 / 40 de 50 - 30 = 10, pode pelo menos 1 / 40 de 50 - 60 = -20, nao pode
                    tem_capacidade = False

            else: #se n tiver nenhum t == t_starts signica q n tem nenhum movimento no dia t / acredito que essa linha n é necessaria mas estou deixando para ajudar no raciocinio inicial
                tem_capacidade = True

    return tem_capacidade


def clear_and_update_dummy_dic_pad(early_time,best_pad,best_pos,dummy_dic_pad):
    aux_dummy_dic_pad = copy.deepcopy(dummy_dic_pad)

    for p in aux_dummy_dic_pad['pads']:
        if p == best_pad:
            aux_dummy_dic_pad['time_build_start'][p].pop()
            aux_dummy_dic_pad['time_build_start'][p].append(early_time)

            aux_dummy_dic_pad['position_pad'][p].pop()
            aux_dummy_dic_pad['position_pad'][p].append(best_pos)

            #print('LINE 287 DUMMY DIC_PAD:', aux_dummy_dic_pad)

        else:
            aux_dummy_dic_pad['stockpiles'][p].pop()
            aux_dummy_dic_pad['time_build_start'][p].pop()
            aux_dummy_dic_pad['time_rec_finish'][p].pop()
            aux_dummy_dic_pad['position_pad'][p].pop()
            aux_dummy_dic_pad['length_stockpile'][p].pop()

            #print('LINE 295 DUMMY DIC_PAD:', aux_dummy_dic_pad)


    return aux_dummy_dic_pad