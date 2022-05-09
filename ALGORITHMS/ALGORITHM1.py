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

from FUNCTIONS.Visual_Outputs import generate_visual_graphic_outputs

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
    #dic_ship['time_departure'] = [374,303,404]                                                                      ##simulando tempos de partidas dos navios

    for v in V:
        #print(v[0])
        current_ship = select_current_entity(dic_ship,v[0])                                                             #Copying to a new dictionary the informations only of the current ship
        #print('\nLINE 27 current_ship: ', current_ship)

        best_berth = -1
        min_time_arr = dic_instance['infinite']
        #print(dic_berth)
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
        #best_current_berth['time_departure'].append(current_ship['time_departure'])                                     ##essa linha deixará de existir quando chegar na  linha 28 - ou manter ela aqui, adicionar um numero do tipo -1 e lá no final só acessar a posicao e substituir
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

        dic_berth['time_departure'][dic_ship['berth_assigned'][v[0]]].append(dic_ship['time_departure'][v[0]])






    # print('-------DICIONARIOS ATUALIZADOS--------\n')
    #
    # print('DIC_BERTH: ', dic_berth)
    # print('DIC_SHIP:', dic_ship)
    # print('DIC_STOCKPILE:', dic_stockpile)
    # print('DIC_PAD: ', dic_pad)
    # print('DIC_LOAD_POINT:', dic_load_point)
    # print('DIC_STACKER_STREAM: ', dic_stacker_stream)
    # print('DIC_RECLAIMER: ', dic_reclaimer)
    #
    #
    # print('\n----------------end-----------------')

    #generate_visual_graphic_outputs(dic_ship, dic_berth, dic_stockpile, dic_pad, dic_load_point, dic_stacker_stream, dic_reclaimer)


    return dic_ship, dic_berth, dic_stockpile, dic_pad, dic_load_point, dic_stacker_stream, dic_reclaimer

