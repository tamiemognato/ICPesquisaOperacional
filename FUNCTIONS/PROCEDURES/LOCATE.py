
from FUNCTIONS.ALGORITHM1functions import list_of_real_and_dummy_stockpiles_already_located_in_the_stockyard
from FUNCTIONS.ALGORITHM1functions import list_of_real_and_dummy_stockpiles_located_on_pad_p_ordered_by_position
from FUNCTIONS.ALGORITHM1functions import does_s_not_conflict_with_any_other_stockpile_on_p
from FUNCTIONS.ALGORITHM1functions import at_least_one_coal_movement_can_be_carried_out_for_s_on_day_t
from FUNCTIONS.ALGORITHM1functions import clear_and_update_dummy_dic_pad


def LOCATE(dic_instance,dummy_dic_pad,current_stockpile,times_start_of_day,dic_load_point,dic_ship,ship_of_stockpile_s):
    best_pad = -1
    best_pos = -1
    early_time = dic_instance['infinite']

    for p in dummy_dic_pad['pads']:  #Neste for o código adiciona stockpiles -1 falsas a ambos os pads com tempo de fim da recuperação igual a 0 e posição igual a largura da pilha + distância de segurança no pad.
        dummy_dic_pad['stockpiles'][p].append(-1)
        dummy_dic_pad['time_build_start'][p].append(-1)
        dummy_dic_pad['time_rec_finish'][p].append(0)
        dummy_dic_pad['position_pad'][p].append((-1 * (current_stockpile['length_stockpile'] + dummy_dic_pad['distance_between_stockpiles'][p])))
        dummy_dic_pad['length_stockpile'][p].append(current_stockpile['length_stockpile'])
        #print('LINE 20 DUMMY DIC PAD: ', dummy_dic_pad)

    # LINE 7 S' - função para gerar a lista que recebe o dummy_dic_pad com as pilhas reais e  as pilhas temporarias falsas, retorna (tempo final de rec, pad, dummy h, stockpile, comprimento)
    S_LINHA = list_of_real_and_dummy_stockpiles_already_located_in_the_stockyard(dummy_dic_pad)  ## !!!!!!!!!!!! CONFERIR SE ORDENA CERTO DPS Q COMEÇAR A SALVAR NO DIC PAD
    #print('LINE 24 S_LINHA: ', S_LINHA)

    for s_linha in S_LINHA:
        t = s_linha[0]  # vamos considerar t igual ao tempo de fim de recuperação da pilha s_linha em questão
        #print('LINE 28 t: ', t)
        if t > early_time:
            break
        p = s_linha[1]  # vamos considerar p igual ao pad da pilha s_linha em questão
        #print('LINE 32 p: ', p)
        # LINE 14 S" - função para gerar a lista de pilhas que estão no pátio e mais especificamente no pad p
        S_DUAS_LINHAS = list_of_real_and_dummy_stockpiles_located_on_pad_p_ordered_by_position(S_LINHA,p)  ## !!!!!!!!!!!! CONFERIR SE ORDENA CERTO DPS Q COMEÇAR A SALVAR NO DIC PAD
        #print('LINE 35 S_DUAS_LINHAS: ', S_DUAS_LINHAS)

        ################################################################################################################

        for s_duas_linhas in S_DUAS_LINHAS:
            h = s_duas_linhas[2] + s_duas_linhas[4] + dummy_dic_pad['distance_between_stockpiles'][p]  # posição de s_duas_linhas + o comprimento de s_duas_linhas + a distancia de segurança do pad
            #print('LINE 41 h:', h, ' sendo a stockpile corrente:', current_stockpile['stockpiles'])

            if (h + current_stockpile['length_stockpile']) <= dummy_dic_pad['lenght_pad'][p]:
                #print('LINE 44:', h, '+', current_stockpile['length_stockpile'], '<=', dummy_dic_pad['lenght_pad'][p])

                dummy_dic_pad['stockpiles'][p][-1] = current_stockpile['stockpiles']
                dummy_dic_pad['position_pad'][p][-1] = h
                dummy_dic_pad['time_rec_finish'][p][-1] = dic_instance['infinite']
                dummy_dic_pad['time_build_start'][p][-1] = t
                #print('LINE 50 DUMMY DIC PAD: ', dummy_dic_pad)

                testing_conflict = does_s_not_conflict_with_any_other_stockpile_on_p(p, h, t, dummy_dic_pad,dic_instance['infinite'])  ## !!!!!!!!! CONFERIR SE RETORNA CERTO DPS Q COMEÇAR A SALVAR NO DIC PAD
                #print('LINE 53 testing_conflict:', testing_conflict)
                if testing_conflict == False:
                    aux_times_start_of_day = [t_starts for t_starts in times_start_of_day if t_starts >= t]
                    #print('LINE 56 aux_times_start_of_day:', aux_times_start_of_day)

                    for t_starts in aux_times_start_of_day:
                        #print('LINE 59:', t_starts)
                        if t_starts >= early_time:  # aqui testa se já foi atribuido o menor tempo possível
                            #print('LINE 60', t_starts)
                            #print('LINE 61 MAIOR!')
                            break
                        else:
                            #if t >= dic_ship['nomination_ship'][ship_of_stockpile_s]: #deu errado, mas deve ser algum erro lógico
                            if at_least_one_coal_movement_can_be_carried_out_for_s_on_day_t(t_starts, dic_load_point,current_stockpile['stockpiles']) == True:
                                #print("LINE 65 ENTROU")
                                #print(t_starts)
                                early_time = t_starts
                                #print('LINE 68 ATUALIZOU')
                                #print('LINE 174 pad p', p, ' e posicao h', h)
                                best_pad = p
                                best_pos = h


    if early_time < dic_ship['nomination_ship'][ship_of_stockpile_s]:
        early_time = min([t_starts for t_starts in aux_times_start_of_day if t_starts >= dic_ship['nomination_ship'][ship_of_stockpile_s]])
    # essa linha não ficou 100% clara para mim, porque o algoritmo faz td trabalho de testar os tempos acima e ai simplesmente se o early_time for maior que a nomeação do
    # navio ele decide atribuir o tempo min logo depois da nomeação, mas não existe nenhum tipo de teste para esse tempo, não deveria ter?
    # quando rodei o código no excel eu acabei entendendo que isso seria corrigido no procedimento 3, mas ainda assim, n seria mais funcional testar desde já?
        #de fato o que acontece é que na pilha 3 por exemplo o early_time fica como 36, mas o primeiro mov pode ser feito somente em 60

        # for t_teste in ([t_starts for t_starts in aux_times_start_of_day if t_starts >= dic_ship['nomination_ship'][ship_of_stockpile_s]]):
        #     if at_least_one_coal_movement_can_be_carried_out_for_s_on_day_t(t_teste, dic_load_point, current_stockpile['stockpiles']) == True:
        #         early_time = t_teste
        #acredito que isso pode ficar como ideia de melhoria no algoritmo, por enquanto está rodando conforme o pseudocódigo
        #coloquei uma reparação no schedule_coal_movement

        #print('LINE 79 early_time:', early_time, 'dic_ship[nomination_ship][ship_of_stockpile_s]:', dic_ship['nomination_ship'][ship_of_stockpile_s])


    #print('LINE 82 DUMMY DIC PAD: ', dummy_dic_pad)

    aux_dummy_dic_pad = clear_and_update_dummy_dic_pad(early_time,best_pad,best_pos,dummy_dic_pad)

    #print('LINE 86 DUMMY DIC PAD: ', aux_dummy_dic_pad)

    current_stockpile['time_build_start'] = early_time
    current_stockpile['pad_assembled'] = best_pad
    current_stockpile['position_pad'] = best_pos

    return aux_dummy_dic_pad





