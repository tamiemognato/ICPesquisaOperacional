import copy
import math


def most_to_least_total_tons_of_coal_from_l_to_s(current_stockpile):
    #vou criar uma lista de tuplas (indice do loadpoint, peso total que s requer de l) e organizar do maior para o menor de acorod com o peso total
    #tonnage_mov_stockpile_lp': [10, 0] * total_mov_stockpile_lp': [2, 0] - peso total que s requer de l

    total_de_toneladas = []
    index = 0
    while index < len(current_stockpile['tonnage_mov_stockpile_lp']):
        if not current_stockpile['tonnage_mov_stockpile_lp'][index] == 0:     #não faz sentido eu rodar esse loop para l se a stockpile s não precisa de carregamento do load point l
            tupla_aux = []
            tupla_aux.append(index)
            tupla_aux.append(current_stockpile['tonnage_mov_stockpile_lp'][index] * current_stockpile['total_mov_stockpile_lp'][index])
            tuple(tupla_aux)
            total_de_toneladas.append(tuple(tupla_aux))
        index += 1

    total_de_toneladas.sort(key=lambda x: x[1], reverse=1)

    return total_de_toneladas





########################################################################################################################


#no final revisar se precisa mesmo ter o current_stockpile ou só o indice de s

def SCHEDULE_COAL_MOVEMENTS(dic_load_point, current_stockpile, dic_stacker_stream, times_start_of_day,dic_pad):
    n_coalmov_lp_time_current_s = []

    most_to_least_total_tons_lp_to_s = most_to_least_total_tons_of_coal_from_l_to_s(current_stockpile)                  #lista com tuplas dos load_points que s precisa de carregamento
    lista_stacker_stream_que_pode_servir_s_no_pad = dic_pad['stacker_streams_pad'][current_stockpile['pad_assembled']]  #lista de stackers que servem ao pad em que s ta
    #print('LINE 38 most_to_least_total_tons_lp_to_s: ', most_to_least_total_tons_lp_to_s)
    #print('LINE 39 lista_stacker_stream_que_pode_servir_s_no_pad: ',lista_stacker_stream_que_pode_servir_s_no_pad)

    for i in most_to_least_total_tons_lp_to_s:                                                                          #para cada tupla de load point que s precisa de coal mov
        res_num = dic_load_point['total_mov_stockpile_lp'][current_stockpile['stockpiles']][i[0]]                       #informo o total de carregamento q s precisa
        #print('LINE 43 RES_NUM: ', res_num)

        for t in (t_starts for t_starts in times_start_of_day if t_starts >= current_stockpile['time_build_start']):    #para cada t de inicio de dia
            #print('LINE 46 T:', t)
            #LOAD POINT#
            #testanto se o load point já tem carragemento para t
            if t in dic_load_point['t_scheduled_coal_movement'][i[0]]:                                                  #se para esse tempo já tiver carragemento atribuido para l
                #print('LINE 50 já tem movimento para l nesse t')

                posicao_lp = dic_load_point['t_scheduled_coal_movement'][i[0]].index(t)                                 #guardo a posição desse tempo
                res_trj = dic_load_point['res_cap_coal_mov_lp'][i[0]][posicao_lp]                                       #pego a capacidade residual de movimentos em quesito deslocamento desse tempo
                res_ton = math.floor(dic_load_point['res_cap_tonnage_l'][i[0]][posicao_lp]/dic_load_point['tonnage_mov_stockpile_lp'][current_stockpile['stockpiles']][i[0]])       #pego a capacidade de movimentos em toneladas desse tempo
                                                                                                                        #a capacidade de movimentos baseada na tonelagem vai ser X toneladas disponiveis no dia / ton por movimento de l para s, arredondado para baixo
                #print('LINE 56 RES_TRJ: ', res_trj)
                #print('LINE 57 RES_TON: ', res_ton)
                #pensar em 1 única função ou função por linha(parâmetro)

            else:                                                                                                       #se não tem nada programado vamos pegar as capacidades máximas
                if t == 108:
                    break
                else:
                    #print('LINE 63 não tem movimento para l nesse t ainda')
                    res_trj = dic_load_point['daily_cap_coal_mov_lp'][i[0]]                                             #capacidade nominal de movimento de l
                    res_ton = math.floor(dic_load_point['daily_cap_tonnage_lp'][i[0]]/dic_load_point['tonnage_mov_stockpile_lp'][current_stockpile['stockpiles']][i[0]])
                                                                                                                        #a capacidade de movimentos baseada na tonelagem vai ser X toneladas disponiveis no dia / ton por movimento de l para s, arredondado para baixo
                    #print('LINE 67 RES_TRJ: ', res_trj)
                    #print('LINE 68 RES_TON: ', res_ton)


            #STACKER STREAM#
            #testanto se k já está atribuido para empilhar alguma pilha no pad - desconsiderando se os stackers vão bater a principio
            #vou usar a politica de atribuir o stacker que tem mais horas disponíveis, assim se k0 tem 0 horas usaremos k1 nem que sejam com 1 hora
            res_dur_list = []                                                                                           #lista de capacidades dos k's que servem ao pad
            for j in lista_stacker_stream_que_pode_servir_s_no_pad:
                if t in dic_stacker_stream['t_scheduled_stacking'][j]:                                                  #já tem algo programado para k aqui?
                    #print('LINE 77já tem movimento para k nesse t')
                    posicao_k = dic_stacker_stream['t_scheduled_stacking'][j].index(t)                                  #pego a posicao desse t
                    res_dur_list.append((dic_stacker_stream['res_cap_hours_stacker'][j][posicao_k]*dic_stacker_stream['productivity'][j])/dic_load_point['tonnage_mov_stockpile_lp'][current_stockpile['stockpiles']][i[0]])
                                                                                                                        #o n de carregamento baseado na disp de horas de k vai ser igual a horas residuais * a produtividade de k (ton/h) dividido pela tonelagem de 1 carregamento de l para s
                    #print('LINE 81 RES_DUR_LIST: ', res_dur_list)
                else:
                    if t == 108:
                        break
                    else:
                        #print('LINE 86 nao tem movimento para k nesse t ainda')
                        res_dur_list.append(math.floor((dic_stacker_stream['daily_cap_hours_stacker'][j]*dic_stacker_stream['productivity'][j])/dic_load_point['tonnage_mov_stockpile_lp'][current_stockpile['stockpiles']][i[0]]))
                                                                                                                        #o n de carregamento baseado na disp de horas de k vai ser igual a horas residuais * a produtividade de k (ton/h) dividido pela tonelagem de 1 carregamento de l para s
                        #print('LINE 89 RES_DUR_LIST: ', res_dur_list)

            res_dur = max(res_dur_list)                                                                                 #adicionei as capacidades de ambos os k's e agora vou ver qual deles tem mais capaciadade de atender a mais movimentos
            k_index = res_dur_list.index(max(res_dur_list))                                                             #guardando de que k será a capacidade maior, como sempre adiciono, então a posição 0 sempre é de k0 e 1 sempre de k1
            k = lista_stacker_stream_que_pode_servir_s_no_pad[k_index]
            #print('LINE 93 RES_DUR: ', res_dur, res_dur_list, k)

            res_min = min(res_num, res_trj, res_ton, res_dur)                                                           #então quantos carregamentos minimamente consigo programar nesse dia sem ultrapassar nenhuma capacidade?
            #print('LINE 97 RES_MIN: ', res_min)

            if res_min > 0:                                                                                             #aqui ele pergunta 'encontrei capacidade nesse dia? sim -> então vamos atribuir, não -> vamos para o proximo t e n vai ter carregamento
                t_res_min = t                                                                                           #atribuo uma variavel para legibilidade que corresponde ao t do carregamento minimo
                #print('LINE 101 T_RES_MIN: ', t_res_min)

                n_mov_slt = min(res_num, res_min)                                                                       #salvo o numero de carregamento que de fato vamos ter no dia de l para s no tempo t
                #print('LINE 104 N_MOV_SLT: ', n_mov_slt)

                res_num = res_num - n_mov_slt                                                                           #atualizo o numero de carregamentos que s precisa de l
                #print('LINE 107 RES_NUM: ', res_num)


                #updateing residual capacities of load point l and stacker stream k on day t - vamos atualizar as capaciadades residuais no t_res_min
                #LOAD POINT#
                if t_res_min not in dic_load_point['t_scheduled_coal_movement'][i[0]]:                                  #é a primeira atribuição para esse tempo t?
                    #print('LINE 113 é a primeira vez de t para l')
                    dic_load_point['t_scheduled_coal_movement'][i[0]].append(t)                                         #adiciono ele a lista, como o append adiciona no final da lista posso simplesmente só adicionar as capacidades res tb
                    cap_res_trj = res_trj - n_mov_slt                                                                   #atualizo o n de carregamento que ainda podem ser feitos por l em quesito deslocamento
                    cap_res_ton = dic_load_point['daily_cap_tonnage_lp'][i[0]] - (n_mov_slt * dic_load_point['tonnage_mov_stockpile_lp'][current_stockpile['stockpiles']][i[0]] )
                                                                                                                        #atualizo a capaciade em toneladas q l ainda pode fornecer no dia como a capaciade nominal - o peso de cada movimento para s * o numero de mov marcados

                    dic_load_point['res_cap_coal_mov_lp'][i[0]].append(cap_res_trj)                                     #adiciono o residual de mov
                    dic_load_point['res_cap_tonnage_l'][i[0]].append(cap_res_ton)                                       #adiciono o residual de toneladas
                    #pensar na inserção ordenada - for + é maior? insere antes
                    #(36 - 12 )/24 ...4.166 intervalos 99996 - inserção ordenada 0 a 4166
                    #print('LINE 122 CAP_RES_TRJ, CAP_RES_TON, dic_load_point[res_cap_coal_mov_lp][i[0]], dic_load_point[res_cap_tonnage_l][i[0]]: ',cap_res_trj,cap_res_ton, dic_load_point['res_cap_coal_mov_lp'][i[0]], dic_load_point['res_cap_tonnage_l'][i[0]])
                else:                                                                                                   #já tinha atribuição? vou atualizar as capacidades então
                    #print('LINE 124 já tem movimento em t para l')
                    posicao_lp = dic_load_point['t_scheduled_coal_movement'][i[0]].index(t_res_min)
                    cap_res_trj = dic_load_point['res_cap_coal_mov_lp'][i[0]][posicao_lp] - n_mov_slt
                    cap_res_ton = dic_load_point['res_cap_tonnage_l'][i[0]][posicao_lp] - (n_mov_slt * dic_load_point['tonnage_mov_stockpile_lp'][current_stockpile['stockpiles']][i[0]] )

                    dic_load_point['res_cap_coal_mov_lp'][i[0]][posicao_lp] = cap_res_trj                               #atualizo na lista a capacidade residual de mov
                    dic_load_point['res_cap_tonnage_l'][i[0]][posicao_lp] = cap_res_ton                                 #atualizo na lista a capacidade residual de toneladas

                    #print('LINE 132 CAP_RES_TRJ, CAP_RES_TON, dic_load_point[res_cap_coal_mov_lp][i[0]], dic_load_point[res_cap_tonnage_l][i[0]]: ',cap_res_trj, cap_res_ton, dic_load_point['res_cap_coal_mov_lp'][i[0]],dic_load_point['res_cap_tonnage_l'][i[0]])

                #STACKER STREAM#
                if t_res_min not in dic_stacker_stream['t_scheduled_stacking'][k]:                                #é a primeira atribuição para esse tempo t?
                    #print('LINE 136 é a primeira vez de t para k')
                    dic_stacker_stream['t_scheduled_stacking'][k].append(t)                                       #adiciono ele a lista, como o append adiciona no final da lista posso simplesmente só adicionar as capacidades res tb
                    cap_res_dur = dic_stacker_stream['daily_cap_hours_stacker'][k] - ((n_mov_slt * dic_load_point['tonnage_mov_stockpile_lp'][current_stockpile['stockpiles']][i[0]]) / dic_stacker_stream['productivity'][k] )
                                                                                                                        #a capaciade residual de acorod com horas restante de k vai ser a capaciade nominal - o numero de mov marcados * o peso de cada mov divido pela produtividade do stacker k

                    dic_stacker_stream['res_cap_hours_stacker'][k].append(cap_res_dur)                            #adiciono o residual de mov

                    dic_stacker_stream['stockpiles_pad_serviced'][k].append(current_stockpile['stockpiles'])

                    #print('LINE 143 CAP_RES_DUR, dic_stacker_stream[res_cap_hours_stacker][k]: ', cap_res_dur, dic_stacker_stream['res_cap_hours_stacker'][k])
                else:
                    posicao_k = dic_stacker_stream['t_scheduled_stacking'][k].index(t_res_min)                    #pego a posicao desse t
                    cap_res_dur = dic_stacker_stream['res_cap_hours_stacker'][k][posicao_k] - ((n_mov_slt * dic_load_point['tonnage_mov_stockpile_lp'][current_stockpile['stockpiles']][i[0]]) / dic_stacker_stream['productivity'][k])

                    dic_stacker_stream['res_cap_hours_stacker'][k][posicao_k] = cap_res_dur

                    #print('LINE 150 CAP_RES_DUR, dic_stacker_stream[res_cap_hours_stacker][k]: ', cap_res_dur, dic_stacker_stream['res_cap_hours_stacker'][k])

                #SALVANDO INFORMAÇÕES DE MOVIMENTO PARA S DE L COM USO DE K NO DIA T (stockpile, nº mov, load point, k em serviço, tempo)
                #transformar em função#
                aux_tuple_list = []
                aux_tuple_list.append(current_stockpile['stockpiles'])
                aux_tuple_list.append(n_mov_slt)
                aux_tuple_list.append(i[0])
                aux_tuple_list.append(k)
                aux_tuple_list.append(t_res_min)
                n_coalmov_lp_time_current_s.append(tuple(aux_tuple_list))
                #print('LINE 160 n_coalmov_lp_time_current_s: ', n_coalmov_lp_time_current_s)

                if res_num == 0:
                    break

        #print('LINE 159 DIC LOAD POINT: ', dic_load_point)
        #print('LINE 160 DIC STACKER STREAM: ', dic_stacker_stream)

        #atualizando a pilha corrente
        current_stockpile['n_coalmov_lp_time'] = n_coalmov_lp_time_current_s
        #função de checagem do early_time - #consertar LOCATE
        count = 0
        lista_tempos_mov = []
        while count < len(current_stockpile['n_coalmov_lp_time']):
            lista_tempos_mov.append(current_stockpile['n_coalmov_lp_time'][count][4])
            count += 1

        min_tempo_mov = min(lista_tempos_mov)
        if min_tempo_mov != current_stockpile['time_build_start']:
            current_stockpile['time_build_start'] = min_tempo_mov

        #print('LINE 171 CURRENT STOCKPILE: ', current_stockpile)

    #função para salvar info de carregamento para pilha no tempo t - load point
    for tupla in current_stockpile['n_coalmov_lp_time']:
        if tupla[2] == 0:
            dic_load_point['n_coalmov_stockpile_time'][0].append(tupla)
        if tupla[2] == 1:
            dic_load_point['n_coalmov_stockpile_time'][1].append(tupla)



    return
