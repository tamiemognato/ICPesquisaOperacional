from FUNCTIONS.ALGORITHM1functions import saving_value_in_principal_entity_dictionary
from FUNCTIONS.PROCEDURES.GET_RECLAIM_TIME import GET_RECLAIM_TIME


def returning_time_build_last_s_finish(current_ship, dic_stockpile):
    last_s_of_v_index = current_ship['order_stockpiles_ship'][-1]                                                       #Salvar o index da última pilha de v
    time_build_finish_of_last_s_of_v = dic_stockpile['time_build_finish'][last_s_of_v_index]                            #Seleciono o tempo calculado na função returning_time_build_s_finish no ALGORITMO 1

    return time_build_finish_of_last_s_of_v

def returning_time_rec_last_s_finish(current_ship, dic_stockpile):
    last_s_of_v_index = current_ship['order_stockpiles_ship'][-1]                                                       #Salvar o index da última pilha de v
    time_build_finish_of_last_s_of_v = dic_stockpile['time_rec_finish'][last_s_of_v_index]                            #Seleciono o tempo calculado salvo em dic_stockpile calculado no procedimento 2 e 3

    return time_build_finish_of_last_s_of_v



def generating_i_loop_list(current_ship_nv):                                                                                #se count = 1 , +1
    count = 0                                                                                                           #PONTO DE ATENÇÃO, TESTANDO COMEÇANDO DO 0
    list_i = []
    while count < (current_ship_nv):
        list_i.append(count)
        count += 1


    #print(list_i)
    return list_i

def reclaimers_serving_the_ships_stockpile_pad(current_ship, i, dic_stockpile, dic_pad):
    s = current_ship['order_stockpiles_ship'][i]
    #print(s)
    p = dic_stockpile['pad_assembled'][s]
    #print(p)
    R_s_s_p = dic_pad['reclaimers_pad'][p]
    #print(R_pad_s_v)

    return R_s_s_p




########################################################################################################################
#VÁRIAVEIS
#'time_elapse_arrive_load': {},  # 'BufAtlV'     # amount of time that must elapse after ship v arrives at a berth before loading can begin (lista de int)
#'arrival_time_berth': {},  # 'TArrV'       # !!!! time of arrival of ship v at the berth in berth_assigned (output)
#'time_build_finish': [],  # -             # time at which building of stockpile s finishes (one day after the last coal movement for s takes place (output)
#'total_stockpiles_ship'         : {}, # 'nv'          # the number of stockpiles of v (int)
#'time_reclaimer_moves'          : {}, # 'DurRhh'      # amount of time that elapses when reclaimer r moves from position h to position h' (lista de int)






def SET_RECLAIM_SCHEDULE(current_ship, dic_stockpile, dic_instance, dic_pad, dic_reclaimer, dic_ship):
    time_build_finish_of_last_s_of_v = returning_time_build_last_s_finish(current_ship, dic_stockpile)
    #print('LINE 58 time_build_finish_of_last_s_of_v:' , time_build_finish_of_last_s_of_v)
    time_v_is_ready_to_reclaim = current_ship['arrival_time_berth'] + dic_instance['time_elapse_arrive_load'][current_ship['ships']]       #!!!!! COLOCAR ISTO NO DIC SHIP
    early_time = max(time_build_finish_of_last_s_of_v,time_v_is_ready_to_reclaim)          #TODOS OK, EXCETO: ETA DO NAVIO 2 ESTÁ ERRADO, PASSEI ERRADO NA ENTRADA, VOU FINALIZAR COM ESSE VALOR.                                                  #PROCEDIMENTO 3 LINHA 1
    #print('LINE 61 EARLY_TIME: ', early_time)

    list_i = generating_i_loop_list(current_ship['total_stockpiles_ship'])
    #print('LINE 64 LIST_I: ', list_i)
    for i in list_i:                                                                                                                       #Atenção: o i não é o indice das pilhas em geral, mas sim o indice das pilhas da lista de pilhas ordenadas de v
        s = current_ship['order_stockpiles_ship'][i]
        #print('LINE 67 S: ', s)
        if i > 0:
            previous_s_index = current_ship['order_stockpiles_ship'][i-1]
            #print('LINE 70 previous_s_index: ', previous_s_index)
            previous_s_reclaimer_used = dic_stockpile['reclaimer'][previous_s_index]
            #print('LINE 70 previous_s_reclaimer_used: ', previous_s_reclaimer_used)

            early_time = dic_stockpile['time_rec_finish'][previous_s_index] + dic_instance['time_reclaimer_moves'][previous_s_reclaimer_used] #PROCEDIMENTO 3 LINHA 4
            #print('LINE 73: dic_stockpile[time_rec_finish][previous_s_index] + dic_instance[time_reclaimer_moves][previous_s_reclaimer_used]')
            #print(dic_stockpile['time_rec_finish'][previous_s_index],'+' ,dic_instance['time_reclaimer_moves'][previous_s_reclaimer_used])
            #print('LINE 75 EARLY_TIME: ', early_time)

        best_rcl_time = dic_instance['infinite']
        best_rcl_time_finish = -1
        best_rcl = -1

        R_s_s_p = reclaimers_serving_the_ships_stockpile_pad(current_ship, i, dic_stockpile, dic_pad)                                      #lista de reclaimers que serve ao pad que s de v está
        #print('LINE 82 R_s_s_p: ', R_s_s_p)

        for r in R_s_s_p:
            #print('\n %%%%%%%%%%%%% GET_RECLAIM_TIME %%%%%%%%%%%%% \n')
            proc4_em_test = GET_RECLAIM_TIME(s, r, early_time, dic_stockpile, dic_reclaimer, dic_instance, R_s_s_p, dic_pad)
            #print('LINE 87 GET_RECLAIM_TIME RESULTADO: ', proc4_em_test)

            if proc4_em_test[0] < best_rcl_time:
                #print('LINE 91 proc4_em_test[0] < best_rcl_time: ', proc4_em_test[0], ' < ', best_rcl_time )
                best_rcl_time = proc4_em_test[0]
                best_rcl = r


        reclaimer_of_s_from_v = best_rcl
        time_rec_start = best_rcl_time
        time_rec_finish = time_rec_start + dic_stockpile['time_reclaim_stockpile'][s]
        #print('LINE 100 reclaimer_of_s_from_v, time_rec_start, time_rec_finish: ', reclaimer_of_s_from_v,time_rec_start,time_rec_finish)

        #Gravando o gap de tempo em que r estará em uso para s
        gap_r_in_use = [] #limpando a lista
        gap_r_in_use.append(time_rec_start)
        gap_r_in_use.append(time_rec_finish)
        #print('LINE 106 GAP_R_IN_USE: ', gap_r_in_use)

        #Gravando o gap de espaço em que r estará em uso para s
        space_gap_r_in_use = []
        space_gap_r_in_use.append(dic_stockpile['position_pad'][s])
        space_gap_r_in_use.append(dic_stockpile['position_pad'][s]+dic_stockpile['length_stockpile'][s])
        #print('LINE 112 SPACE_GAP_R_IN_USE: ', space_gap_r_in_use)


        #ATUALIZANDO DIC_RECLAIMER
        dic_reclaimer['stockpiles_reclaimed'][best_rcl].append(s)
        dic_reclaimer['reclaim_schedule'][best_rcl].append(tuple(gap_r_in_use))
        dic_reclaimer['space_of_reclaim_schedule'][best_rcl].append(tuple(space_gap_r_in_use))
        #print('LINE 119 DIC_RECLAIMER ATUALIZADO: ', dic_reclaimer)

        #ATUALIZANDO DIC_STOCKPILE
        dic_stockpile['reclaimer'][s] = best_rcl
        dic_stockpile['time_rec_start'][s] = time_rec_start
        dic_stockpile['time_rec_finish'][s] = time_rec_finish
        #print('LINE 125 DIC_STOCKPILE ATUALIZADO: ',dic_stockpile)

        #ATUALIZANDO DIC_SHIP - **************
        dic_ship['time_rec_last_stockpile'][current_ship['ships']] = returning_time_rec_last_s_finish(current_ship, dic_stockpile)
        #print('LINE 129 DIC_SHIP ATUALIZADO: ',dic_ship)

    return
