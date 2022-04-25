import copy
import os
import sys
import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.express as px
import plotnine
import pandas as pd
from plotnine import *

sys.path.append('FUNCTIONS')

from FUNCTIONS.ALGORITHM1functions import sort_entity_by_related_parameter_order_lesstomore, \
    returning_time_build_s_finish

from FUNCTIONS.ALGORITHM1functions import select_current_entity
from FUNCTIONS.ALGORITHM1functions import saving_value_in_principal_entity_dictionary
from FUNCTIONS.ALGORITHM1functions import saving_value_in_dic_berth
from FUNCTIONS.ALGORITHM1functions import min_time_arr_at_berth
from FUNCTIONS.ALGORITHM1functions import sort_stockpiles_in_order_stockpiles_ship_by_rec_sequence

from FUNCTIONS.PROCEDURES.LOCATE import LOCATE
from FUNCTIONS.PROCEDURES.SCHEDULE_COAL_MOVEMENTS import SCHEDULE_COAL_MOVEMENTS
from FUNCTIONS.PROCEDURES.SET_RECLAIM_SCHEDULE import SET_RECLAIM_SCHEDULE


def ALGORITHM1(dic_ship, dic_instance, dic_berth, dic_stockpile, dic_pad, dic_load_point, dic_stacker_stream, dic_reclaimer):
    # #GERANDO TEMPOS - Tempos com granularidade 1
    # times_start_of_day = [12]
    # count = 1
    # while count <= dic_instance['infinite']:  #gerar ele apenas dentro da função para não ocupar memória
    #     times_start_of_day.append(0 + count)
    #     count += 1
    # #print(times_start_of_day)

    #PARA A MUDANÇA DOS TEMPOS !!!!
    #Constante de passo. Passo = 0 tempo 0..1..2...3..4..5.6
    #Passo = 12 tempo 12, 24,36,....
    #Fazer função para gerar o tempo em função do passo para tornar o código inteiro  adaptavel
    #granularidade X passo
    #priorizar a multiplicação ou somar, pois divisão por zero bloqueia
    #Por em termos humanos apenas no print solução de acordo com o passo e granularidade

    #criar uma vez só, como global ou parametro, fora da função / criar lista de load point no tempo
    times_start_of_day = [12]
    count = 24
    while count < dic_instance['infinite']:  # gerar ele apenas dentro da função para não ocupar memória
        times_start_of_day.append(12 + count)
        count += 24
    #print('LINE 73 times_start_of_day:', times_start_of_day)




    V = sort_entity_by_related_parameter_order_lesstomore(dic_ship,'ships','eta_ship')                                  #Sorting the ships by ETA, in a crescent order
    S_sorted = sort_stockpiles_in_order_stockpiles_ship_by_rec_sequence(dic_ship['order_stockpiles_ship'],V)            ##ver se vai precisar mesmo na linha 15 - line 14 - as listas dentro da lista já é organizada por ordem de recuperação
    #print(V)
    #print(dic_ship['order_stockpiles_ship'])
    #print(S_sorted)
    #dic_ship['time_departure'] = [374,303,404,397]                                                                      ##simulando tempos de partidas dos navios
    dic_ship['time_departure'] = [374,303,404]                                                                      ##simulando tempos de partidas dos navios

    for v in V:
        #print(v[0])
        current_ship = select_current_entity(dic_ship,v[0])                                                             #Copying to a new dictionary the informations only of the current ship
        #print('\nLINE 27 current_ship: ', current_ship)

        best_berth = -1
        min_time_arr = dic_instance['infinite']

        for b in dic_berth['berths']:
            current_berth = select_current_entity(dic_berth,b)                                                          #Copying to a new dictionary the informations only of the current berth
            #print('\nLINE 34 current_berth: ', current_berth)
                                                                                                                        #In the next lines it will be defined the time arrival of the current ship in the chosen berth
            if current_berth['ships_scheduled'] == []:                                                                  #If the list of berths allocated in the current berth is empty, then this means the berth has no ships schedule to it yet, then we can allocated the current ship to it at the precisely time it arrives at the port (ETA)
                time_arr = current_ship['eta_ship']
                #print('\nLINE 38 time_arr: ', time_arr, ' .ship: ', current_ship['ships'], ' berth: ', current_berth['berths'])
            else:                                                                                                       #If the list of berths allocated in the current berth isn't empty, then it means the berth already have at least one ship booked on it. This ship, or ships, will arrive at the berth necessarily before our current ship. So we must ask: at which time the current ship can arrive at this berth? Or what is the earliest time at witch the current ship can arrive at the current berth after all ships alreay booked leave it? The function 'min_time_arr_at_berth' responses this question

                time_arr = min_time_arr_at_berth(current_berth['time_departure'], current_ship['eta_ship'])
                #print('\nLINE 42 time_arr: ', time_arr, ' .ship: ', current_ship['ships'], ' berth: ', current_berth['berths'])

            #print('\nLINE 44 min_time_arr: ', min_time_arr, ' .ship: ', current_ship['ships'], ' berth: ', current_berth['berths'])
            if time_arr < min_time_arr:                                                                                 #In the case of the first berth this line asks: "Is the time_arr lower than infinite?". In the case of the following berths this line will ask: "Does the ship can arrive earlier at this current berth or in the previous?"
                best_berth = b
                min_time_arr = time_arr
                #print('\nLINE 48 min_time_arr: ', min_time_arr, ' .ship: ', current_ship['ships'], ' berth: ', current_berth['berths'])


        #print('\nLINE 51 best_berth: ', best_berth, ' min_time_arr: ', min_time_arr)
        best_current_berth = select_current_entity(dic_berth, best_berth)                                               #We only want to save the informations of 'best_berth' and 'min_time_arr' when we finish testing all the possibilities with the previous loop, but we don't want to loose information with the redefinition of variables in the loop. For acomplish it, we will use a copy dictionary of the best berth with it information and than append the necessary update information after we leave the loop, as follows below
        #print('\nLINE 53 best_current_berth: ', best_current_berth)
        best_current_berth['ships_scheduled'].append(v[0])
        best_current_berth['arrival_time_berth'].append(min_time_arr)
        best_current_berth['time_departure'].append(current_ship['time_departure'])                                     ##essa linha deixará de existir quando chegar na  linha 28 - ou manter ela aqui, adicionar um numero do tipo -1 e lá no final só acessar a posicao e substituir
        #print('\nLINE 57 best_current_berth: ', best_current_berth)

        #print('\nLINE 59 dic_berth: ', dic_berth)
        dic_berth = saving_value_in_dic_berth(dic_berth, best_current_berth)                                            #Updating our main dictionary of berths with the new attributions
        #print('\nLINE 61 dic_berth: ', dic_berth)

        current_ship['berth_assigned'] = best_berth                                                                     #Updating the current ship dictionary with the best berth and the best arrival time
        current_ship['arrival_time_berth'] = min_time_arr

        dic_ship = saving_value_in_principal_entity_dictionary(dic_ship,current_ship)                                   #Updating our main dictionary of ships with the new attributions
        #print('\nLINE 67 dic_ship: ', dic_ship)

########################################################################################################################################################

        for s in dic_ship['order_stockpiles_ship'][v[0]]:                                                               ##order stockpiles in S(v) by reclaiming sequence - feito no input de dados, avaliar se é necessário, pois resolvivel com a linha a seguir e as pilhas de cada navio já devem ser organizar no input
            dummy_dic_pad = copy.deepcopy(dic_pad)
            #print('\nLINE 103 DUMMY DIC PAD: ', dummy_dic_pad)

            #print('LINE 105 stockpiles of v: ', s, ' e v: ', v[0])
            current_stockpile = select_current_entity(dic_stockpile, s)
            #print('LINE 107 current_stockpile: ', current_stockpile)

            # if current_stockpile['stockpiles'] == 3:
            #     dic_load_point['t_scheduled_coal_movement'][0].append(12)
            #     dic_load_point['res_cap_coal_mov_lp'][0].append(0)
            #     dic_load_point['res_cap_tonnage_l'][0].append(0)
            #
            #     dic_load_point['t_scheduled_coal_movement'][1].append(12)
            #     dic_load_point['res_cap_coal_mov_lp'][1].append(0)
            #     dic_load_point['res_cap_tonnage_l'][1].append(0)
            #     print('TESTE DIC LOAD POINT: ', dic_load_point)

            updated_dummy_dic_pad = LOCATE(dic_instance,dummy_dic_pad,current_stockpile,times_start_of_day,dic_load_point,dic_ship,v[0])
            #print('LINE 110 UPDATE_DUMMY_DIC_PAD:',updated_dummy_dic_pad)

            dic_pad = copy.deepcopy(updated_dummy_dic_pad)
            #print('LINE 113 DIC_PAD:', dic_pad)
            #print('LINE 114 current_stockpile: ', current_stockpile)

            #print('LINE 116 DIC_STOCKPILE ANTES: ', dic_stockpile)
            dic_stockpile = saving_value_in_principal_entity_dictionary(dic_stockpile,current_stockpile)                                   #Updating our main dictionary of ships with the new attributions
            #print('LINE 118 DIC_STOCKPILE DEPOIS: ', dic_stockpile) #pilha 3 do navio 2, correto 36 aqui, vai mudar no próximo procedimento quando começar a atualizar a cap residual dos load points


            #print('\n ##################### SCHEDULE_COAL_MOVEMENTS EM TESTE ##################\n')

            #print('LINE 117 DIC LOAD POINT ANTES: ', dic_load_point)
            #print('LINE 118 DIC STACKER STREAM ANTES: ', dic_stacker_stream)
            #print('LINE 119 DIC STOCKPILE ANTES:', dic_stockpile)

            proc2_em_teste = SCHEDULE_COAL_MOVEMENTS(dic_load_point, current_stockpile, dic_stacker_stream, times_start_of_day,dic_pad)

            #print('LINE 133 DIC LOAD POINT DEPOIS: ', dic_load_point)
            #print('LINE 134 DIC STACKER STREAM DEPOIS: ', dic_stacker_stream)
            dic_stockpile = saving_value_in_principal_entity_dictionary(dic_stockpile,current_stockpile)                                   #Updating our main dictionary of ships with the new attributions
            #print('LINE 135 DIC STOCKPILE DEPOIS:', dic_stockpile)

            #ATÉ AQUI AS PILHAS ESTÃO NOS RESPECTIVOS BERÇOS CORRETOS, NOS RESPECTIVOS PÁTIOS CORRETOS EM SUAS RESPECTIVAS POSIÇÕES CORRETAS E
            #COM AS MOVIMENTAÇÕES DOS RESPECITVOS LOAD POINTS E ATENDIMENTO DOS RESPECITVOS STACKERS CORRETOS, TUDO NO TEMPO CORRETO

            #ESTOU SEGUINDO COM A PROGRAMAÇÃO PARA VOLTAR NA QUESTÃO DO TEMPO APENAS NA HORA DE FAZER O DESLOCAMENTO PARA NÃO FICAR PRESA

        # print("\n\n\nout of for s\n\n\n") #SAINDO DO FOR S
        #
        # print('DIC_SHIP_ATUALIZADO:', dic_ship)
        # print('DIC_STOCKPILE_ATUALIZADO:', dic_stockpile)
        # print('DIC_LOAD_POINT_ATUALIZADO:', dic_load_point)
        # print('DIC_RECLAIMER: ', dic_reclaimer)
        # print('DIC_PAD: ', dic_pad)
        # print('CURRENT_SHIP: ', current_ship)

        #print('########################################################################################################')

        returning_time_build_s_finish(current_ship, dic_stockpile)      #SAÍDAS TODAS OK                                                 #Gerando T(lst)s - time at whic building of stockpile s finishes

        # print('DIC_STOCKPILE_ATUALIZADO:', dic_stockpile)
        #
        # print('\n **************** SET_RECLAIM_SCHEDULE **************** \n')
        proc3_em_teste = SET_RECLAIM_SCHEDULE(current_ship, dic_stockpile, dic_instance, dic_pad, dic_reclaimer, dic_ship)

        #LINHAS NAVIOS GRANDES

        # print('\n dic_ship: ', dic_ship)
        # print('CURRENT_SHIP: ', current_ship)
        # print('CURRENT_SHIP DEPARTURE TIME: ', current_ship['time_departure'])
        dic_ship['time_departure'][v[0]] = dic_ship['time_rec_last_stockpile'][v[0]] + dic_instance['time_elapse_load_depart'][v[0]]
        # print(dic_ship['time_rec_last_stockpile'][v[0]])
        # print(dic_instance['time_elapse_load_depart'][v[0]])
        # print('dic_ship: ', dic_ship)






    print('-------DICIONARIOS ATUALIZADOS--------\n')

    #print('DIC_BERTH: ', dic_berth)
    # print('DIC_SHIP:', dic_ship)
    print('DIC_STOCKPILE:', dic_stockpile)
    # print('DIC_PAD: ', dic_pad)
    # print('DIC_LOAD_POINT:', dic_load_point)
    # print('DIC_STACKER_STREAM: ', dic_stacker_stream)
    #print('DIC_RECLAIMER: ', dic_reclaimer)

    print('\n----------------end-----------------')

    #função com entrada de dicionários com listas e saída de uma lista com vários dicionários
    #aplicando ao dic_berth primeiramente
    #ENTRADA - DIC_BERTH: {'instance_name': '01_GCA_ETA_LOCATE_TEST.txt', 'berths': [0, 1], 'ships_scheduled': [[1, 2], [0]],
                #'arrival_time_berth': [[282, 374], [300]], 'time_departure': [[303, 404], [374]]}
    #SAÍDA - lista_dic_berth = [{'berths' : 0 , 'ships_scheduled' : 1 ...},
                            #   {'berths' : 0 , 'ships_scheduled' : 2 ...},
                            #   {'berths' : 1 , 'ships_scheduled' : 0 ...}]

    lista_dic_berth = []
    lista_chaves_dic_berth = ['berths', 'ships_scheduled', 'arrival_time_berth', 'time_departure']
    for b in dic_berth['berths']: #para cada berço
        count = 0
        while count < len(dic_berth['ships_scheduled'][b]): #dar o laço para o número de dados nas listas dos respectivos berços

            dic_aux = {}
            dic_aux = dict(berths = dic_berth['berths'][b], ships_scheduled = dic_berth['ships_scheduled'][b][count], arrival_time_berth = dic_berth['arrival_time_berth'][b][count], time_departure = dic_berth['time_departure'][b][count])

            lista_dic_berth.append(dic_aux)

            count += 1

    #print(lista_dic_berth)

    df_b = pd.DataFrame(lista_dic_berth)
    #df = df.transpose()
    #print(df_b)

    # GANTT DOS BERÇOS - ok
    # Berth to wichi ship v is assigned + time of arrival of ship v at berth bv
    # + time of departure of ship v from berth bv

    graph_berths = (
        ggplot(data = df_b)
        + geom_segment(aes(x='arrival_time_berth', y='berths', xend='time_departure', yend='berths'))
        + aes(size = 10, color = "ships_scheduled")
        + geom_label(aes(label = "arrival_time_berth",  x = "arrival_time_berth", y = "berths", size = 10))
        + geom_label(aes(label="time_departure", x="time_departure", y="berths", size=10))
        + labs(title = 'Berths schedule', x = "Time", y = 'Berths')

        )

    print(graph_berths)

    ###############################################   RECLAIMERES   ####################################################
    lista_dic_reclaimer = []
    for r in dic_reclaimer['reclaimers']:
        count = 0
        while count < len(dic_reclaimer['stockpiles_reclaimed'][r]):

            dic_aux = {}
            dic_aux = dict(reclaimers = dic_reclaimer['reclaimers'][r], stockpiles_reclaimed = dic_reclaimer['stockpiles_reclaimed'][r][count], reclaim_start = dic_reclaimer['reclaim_schedule'][r][count][0], reclaim_finish = dic_reclaimer['reclaim_schedule'][r][count][1])

            lista_dic_reclaimer.append(dic_aux)

            count += 1

    #print(lista_dic_reclaimer)

    df_r = pd.DataFrame(lista_dic_reclaimer)
    #df = df.transpose()
    #print(df_r)

    # GANTT DOS RECLAIMERS
    # Reclaimer used in reclaiming stockpile s + time at wich reclaiming pf stockpile s starts
    # + time at which reclaiming of stockpile s finishes

    graph_reclaimers = (
        ggplot(data = df_r)
        + geom_segment(aes(x='reclaim_start', y='reclaimers', xend='reclaim_finish', yend='reclaimers'))
        + aes(size = 10, color = "stockpiles_reclaimed")
        + geom_label(aes(label = "reclaim_start",  x = "reclaim_start", y = "reclaimers", size = 10))
        + geom_label(aes(label="reclaim_finish", x="reclaim_finish", y="reclaimers", size=10))
        + labs(title = 'Reclaimers schedule', x = "Time", y = 'Reclaimers')
        )
    print(graph_reclaimers)

    ##############################################    STOCKPILES    ####################################################
    lista_dic_stockpile_pad_0 = []
    lista_dic_stockpile_pad_1 = []

    for s in dic_stockpile['stockpiles']:
            dic_aux = {}
            dic_aux = dict(stockpiles = dic_stockpile['stockpiles'][s],
                           pad_assembled = dic_stockpile['pad_assembled'][s],
                           position_pad_start = dic_stockpile['position_pad'][s],
                           position_pad_finish = dic_stockpile['position_pad'][s] + dic_stockpile['length_stockpile'][s],
                           time_build_start = dic_stockpile['time_build_start'][s],
                           time_build_finish = dic_stockpile['time_build_finish'][s],
                           time_rec_start = dic_stockpile['time_rec_start'][s],
                           time_rec_finish = dic_stockpile['time_rec_finish'][s],
                           stockpile_label_x = (dic_stockpile['time_build_start'][s] + dic_stockpile['time_rec_finish'][s])/2,
                           stockpile_label_y = (dic_stockpile['position_pad'][s] + dic_stockpile['position_pad'][s] + dic_stockpile['length_stockpile'][s])/2
                           )

            if dic_stockpile['pad_assembled'][s] == 0:
                lista_dic_stockpile_pad_0.append(dic_aux)
            else:
                lista_dic_stockpile_pad_1.append(dic_aux)

    print(lista_dic_stockpile_pad_0)
    print(lista_dic_stockpile_pad_1)


    df_s_pad_0 = pd.DataFrame(lista_dic_stockpile_pad_0)
    #df = df.transpose()
    print(df_s_pad_0)

    df_s_pad_1 = pd.DataFrame(lista_dic_stockpile_pad_1)
    #df = df.transpose()
    print(df_s_pad_1)

    # GANTT DOS PADS x STOCKPILES
    # Pad on which stockpile s is assembled + position of stockpile s on its pad + number of coal movements carried out for stockpile s from load point l at time t
    # + time at which building of stockpile s starts + time at which reclaiming of stockpile s finishes

    graph_stockpiles_pad_0 = (
        ggplot(data = df_s_pad_0)

        + geom_rect(aes(xmin = "time_build_start", xmax = "time_rec_finish", ymin = "position_pad_start", ymax = "position_pad_finish", fill = "stockpiles"))
        + labs(title = "PAD 0", x = "Time", y = "Pad occupation")
        + scale_fill_continuous(guide = guide_legend())
        + geom_label(aes(label="stockpiles", x="stockpile_label_x", y="stockpile_label_y", size=10, color="stockpiles"))
        + geom_label(aes(label="time_build_start", x="time_build_start", y="position_pad_start", size=10, color="stockpiles"))
        + geom_label(aes(label="time_build_finish", x="time_build_finish", y="position_pad_start", size=10, color="stockpiles"))
        + geom_label(aes(label="time_rec_start", x="time_rec_start", y="position_pad_start", size=10, color="stockpiles"))
        + geom_label(aes(label="time_rec_finish", x="time_rec_finish", y="position_pad_start", size=10, color="stockpiles"))
    )
    print(graph_stockpiles_pad_0)

    graph_stockpiles_pad_1 = (
        ggplot(data = df_s_pad_1)

        + geom_rect(aes(xmin = "time_build_start", xmax = "time_rec_finish", ymin = "position_pad_start", ymax = "position_pad_finish", fill = "stockpiles"))
        + labs(title = "PAD 1", x = "Time", y = "Pad occupation")
        + scale_fill_continuous(guide = guide_legend())
        + geom_label(aes(label = "stockpiles",  x = "stockpile_label_x", y = "stockpile_label_y", size = 10, color = "stockpiles" ))
        + geom_label(aes(label="time_build_start", x="time_build_start", y="position_pad_start", size=10, color ="stockpiles"))
        + geom_label(aes(label="time_build_finish", x="time_build_finish", y="position_pad_start", size=10, color="stockpiles"))
        + geom_label(aes(label="time_rec_start", x="time_rec_start", y="position_pad_start", size=10, color="stockpiles"))
        + geom_label(aes(label="time_rec_finish", x="time_rec_finish", y="position_pad_start", size=10, color="stockpiles"))

    )
    print(graph_stockpiles_pad_1)

    os.chdir("OUTPUT")
    ggsave(plot=graph_berths, filename='berths_schedule')
    ggsave(plot=graph_reclaimers, filename='reclaimers_schedule')
    ggsave(plot=graph_stockpiles_pad_0, filename='pad_0_schedule')
    ggsave(plot=graph_stockpiles_pad_1, filename='pad_1_schedule')
