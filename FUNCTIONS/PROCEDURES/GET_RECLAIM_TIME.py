
def set_of_stockpiles_that_finish_being_reclaimed_by_r_after_early_time(r, early_time, dic_reclaimer, dic_stockpile):
    list_of_s_finish_reclaim_by_r_after_early_time = []

    stockpiles_reclaimed_by_r = dic_reclaimer['stockpiles_reclaimed'][r]                                                #Seleciono as stockpiles que r atende
    print('LINE G6: ', stockpiles_reclaimed_by_r)
    if len(stockpiles_reclaimed_by_r) != 0:
        print('oi')
        for s in stockpiles_reclaimed_by_r:
            print('dic_stockpile[time_rec_finish][s]: ', dic_stockpile['time_rec_finish'][s])
            print('LINE 11 early time: ', early_time)
            if dic_stockpile['time_rec_finish'][s] >= early_time:                                                        #comparo se o tempo que elas terminam de serem recuperadas é maior (ou igual) que o early_time
                list_of_s_finish_reclaim_by_r_after_early_time.append(s)


    return list_of_s_finish_reclaim_by_r_after_early_time


def interval_ab(early_time, dic_instance):
    a = early_time
    b = dic_instance['infinite']
    interval_a_b = []
    interval_a_b.append(a)
    interval_a_b.append(b)

    return interval_a_b


def reclaim_s_using_r_during_ab_avoiding_clashes_respecting_nummxr(dic_reclaimer, dic_instance, a, b, r, R_s_s_p, s, dic_stockpile):
    we_can = True
    tuplas_ab_index_list = []

    #NÚMERO MÁXIMO DE RECLAIMERS
    aux_rec_list = []
    num_max_aux_list = []
    for rec in dic_reclaimer['reclaimers']: #crio uma lista com todos os r que já possuem intervalos programados e não são o r atual em teste (pois em ab ele já não está programado)
        if dic_reclaimer['tuplas_ab'][rec] != [-1] and dic_reclaimer['reclaimers'] != r:
            aux_rec_list.append(rec)

    for rec in aux_rec_list:  #para cada reclaimer nessa lista diferente do r atual em teste
        tuplas_ab_index_aux_list = []

        count = 0
        while count < len(dic_reclaimer['tuplas_ab'][rec]): #testo para cada intervalo
            if a in range(dic_reclaimer['tuplas_ab'][rec][count][0],dic_reclaimer['tuplas_ab'][rec][count][1]) == True or b in range(dic_reclaimer['tuplas_ab'][rec][count][0],dic_reclaimer['tuplas_ab'][rec][count][1]) == True:
                #se a está contido nele ou se b está contido nele
                num_max_aux_list.append(rec) #se está eu adiciono a esta lista e testo

                tuplas_ab_index_aux_list.append(rec)
                tuplas_ab_index_aux_list.append(count)
                tuplas_ab_index_list.append(tuple(tuplas_ab_index_aux_list)) #para o próximo passo, crio uma lista de tuplas (rec, index intervalo)

            count += 1



    if len(num_max_aux_list) >= dic_instance['maximum_reclaimers_use']: #se terá mais reclaimers em uso do que a capacidade permite neste intervalo
        we_can = False #caso tenha, não podemos programar r atual em teste para recuperar

    #COLISÕES COM RECLAIMERS DO MESMO PAD
    #A ideia é a mesma da de cima, vamos aproveir a lista num_max_aux_list que já tem os reclaimers em uso no mesmo período de tempo
    #Uma observação importante é que o algoritmo sempre testa tudo partindo do 0, então ele sempre está considerando um reclaimer
    #que está mais a esquerda antes do que está mais a direita, portanto se agendarmos esse mais a esquerda entendo que o mais a direita
    #pode fazer um deslocamento se necessário para o mais a esquerda trabalhar, eles apenas não podem colidir
    #Assim o que eu quero é perguntar: Essa pilha s em questão está numa posição que causará conflito dos reclaimers  no pad no intervalo ab testado?
    #Para recuperar s, r terá que bater em outro reclaimer? Isto é, s está após ou antes a posição da pilha que os demais reclaimers estão recuperando?
    #neste intervalo de tempo
    #como pergunto isso em python?

    aux_rec_same_p_aux_list = []
    for rec in R_s_s_p: #pego a lista de reclaimers do mesmo pad
        if rec in num_max_aux_list: #e aproveito a parte anterior do código só testando se eles já tem alguma programação que colida com o intervalo ab
            aux_rec_same_p_aux_list.append(rec) #crio uma lista só com recs do mesmo pad que estão trabalhando em algum momento de ab

    for rec in aux_rec_same_p_aux_list: #então para cada rec que trabalha no mesmo pad que r
        for tuplas_rec_ab in tuplas_ab_index_list:
                s_rec_ab = dic_reclaimer['stockpiles_reclaimed'][rec][tuplas_rec_ab[1]] #pego o index da pilha s' que o rec está recuperando em ab

                if dic_stockpile['position_pad'][s_rec_ab] < (dic_stockpile['position_pad'][s] + dic_stockpile['length_stockpile'][s]): #testo a condição e clashe
                    we_can = False #se verdade, então não podemos alocar r para s no intervalo ab


    return we_can





########################################################################################################################


def GET_RECLAIM_TIME(s, r, early_time, dic_stockpile, dic_reclaimer,dic_instance, R_s_s_p, dic_pad):
    print('LINE G93 r: ', r)
    S = set_of_stockpiles_that_finish_being_reclaimed_by_r_after_early_time(r, early_time, dic_reclaimer, dic_stockpile)   #SAÍDA OK
    #LINHA 2 - FAZER NO FINAL, N SERÁ ÚTIL PARA ESSA INSTÂNCIA TESTE
    print('LINE G96 S: ', S)

    #Daqui vou seguir 2 caminhos: 1 para a lista vazia em que fazemos a linha 7 e 19 e outro para lista não vazia que fazemos o procedimento inteiro

    #LISTA VAZIA
    if len(S) == 0:
        #reclaim_schedule = (early_time, early_time + dic_stockpile['time_reclaim_stockpile'][s])
        interval_a_b = (early_time, dic_instance['infinite'])    #linha 7 para lista n vazia
        print('LINE G103 Reclaim_schedule lista vazia: ', interval_a_b)

        #INSERIR TESTES DE COLISÃO, QNT R MAX - vou precisar de b definido, não 999




        return interval_a_b

    #LISTA NÃO VAZIA
    else:
        print('LINE G112 S != []')
        if dic_stockpile['time_rec_start'][S[0]]<= early_time:
            print('LINE G114 dic_stockpile[time_rec_start][S[0]]<= early_time: ', dic_stockpile['time_rec_start'][S[0]], ' <= ', early_time)
            early_time = dic_stockpile['time_rec_finish'][S[0]] + dic_instance['time_reclaimer_moves'][r]
            print('LINE G116 EARLY_TIME: ', early_time)
            S = S[1:]
            print('LINE G118 S: ', S)

        interval_a_b = interval_ab(early_time, dic_instance)  #linha 7
        print('LINE G121 INTERVAL_A_B: ', interval_a_b)

        if S != []:
            print('LINE G124 S != []')

            #NESSA INSTÂNCIA, NÃO DEVERIA SER PRECISO PASSAR POR ESSE IF
            # i = 0
            # tuples_list = []
            # aux_list = []
            # while i < len(S):
            #     if i > 1:
            #         a = dic_stockpile['time_rec_finish'][S[i-1]] + dic_instance['time_reclaimer_moves'][r]
            #         interval_a_b[0] = a
            #
            #     b = dic_stockpile['time_rec_start'][S[i]] - dic_reclaimer['time_reclaimer_moves'][r]
            #
            #     if dic_stockpile['time_reclaim_stockpile'][s] <= (b - a):
            #         we_can_reclaim_s_with_r_in_ab = reclaim_s_using_r_during_ab_avoiding_clashes_respecting_nummxr(dic_reclaimer, dic_instance, a, b, r, R_s_s_p, s, dic_stockpile)
            #         if we_can_reclaim_s_with_r_in_ab == True:
            #             aux_list.append(a)
            #             aux_list.append(b)
            #             tuples_list.append(tuple(a,b))
            #
            # tuples_list.sort(key=lambda x: x[0]) #organizo do menor a para o maior
            # reclaim_schedule = tuples_list[0] #menor intervalo possível

            #TESTES

        else:
            var = True

            #### TESTE DE COLISÃO #### linha 19

            #LIMITES DE TEMPO
            a = interval_a_b[0]
            b = interval_a_b[0] + dic_stockpile['time_reclaim_stockpile'][s]

            #LIMITES DE ESPAÇO
            c = dic_stockpile['position_pad'][s]
            d = dic_stockpile['position_pad'][s]+dic_stockpile['length_stockpile'][s]

            #CRIANDO A LISTA DE PILHAS RECUPERADAS PELOS RECLAIMEIRS QUE DIVIDEM O MESMO TRILHO

            #1º Precisamos da lista de pads a qual r atual serve
            lista_de_pads_a_qual_r_atual_serve = []
            for p in dic_pad['pads']:  #para cada pad p
                for rec in dic_pad['reclaimers_pad'][p]: #para recuperador na lista de recuperadores de p
                    if r == rec: #se r atual for igual a ele
                        lista_de_pads_a_qual_r_atual_serve.append(p) #então adicione o pad a lista de pads a qual r atual serve

            print('LINE 171 lista_de_pads_a_qual_r_atual_serve: ', lista_de_pads_a_qual_r_atual_serve)

            #2º Precisamos da lista de reclaimers que também servem a esse pad
            lista_de_rec_que_também_servem_a_esses_pads = []
            for p in lista_de_pads_a_qual_r_atual_serve: #para cada pad da lista_de_pads_a_qual_r_atual_serve
                for rec in dic_pad['reclaimers_pad'][p]: #para cada reclaimer que serve a cada um desses pads
                    if rec not in lista_de_rec_que_também_servem_a_esses_pads: #se ele já não estiver adicionado na lista
                        lista_de_rec_que_também_servem_a_esses_pads.append(rec)  #adiciono ele a lista de reclaimer que também servem aos padas que r atual serve
            print('LINE 179 lista_de_rec_que_também_servem_a_esses_pads: ', lista_de_rec_que_também_servem_a_esses_pads)

            #3º Agora podemos testar os gaps de tempos, a ou b está em [a', b']?
                # E o testar os gaps de espaços, c ou d está em [c', d']?
            for rec in lista_de_rec_que_também_servem_a_esses_pads:  #para cada rec
                count = 0
                while count < len(dic_reclaimer['reclaim_schedule'][rec]):  #com esse while vou passar por todos os gaps de tempo e espaço do respectivo rec
                    test_a = a in range(dic_reclaimer['reclaim_schedule'][rec][count][0], dic_reclaimer['reclaim_schedule'][rec][count][1])  #a está entre a' e b'?
                    test_b = b in range(dic_reclaimer['reclaim_schedule'][rec][count][0], dic_reclaimer['reclaim_schedule'][rec][count][1])  #b está entre a' e b'?
                    #print(dic_reclaimer['reclaim_schedule'][rec][count][0], dic_reclaimer['reclaim_schedule'][rec][count][1])
                    #print(test_a, test_b)
                    if test_a == True or test_b == True:  #se True para algum dos dois, então:
                        test_c = c in range(dic_reclaimer['space_of_reclaim_schedule'][rec][count][0], dic_reclaimer['space_of_reclaim_schedule'][rec][count][1])
                        test_d = d in range(dic_reclaimer['space_of_reclaim_schedule'][rec][count][0], dic_reclaimer['space_of_reclaim_schedule'][rec][count][1])
                        #print(dic_reclaimer['space_of_reclaim_schedule'][rec][count][0], dic_reclaimer['space_of_reclaim_schedule'][rec][count][1])
                        #print(test_c, test_d)
                        if test_c == True or test_d == True: #se true para algum dos dois, então colide no determinado tempo
                            var = False  #não é possível usar r atual, pois colide.
                    count += 1

            #### TESTE DE Nº DE RECS EM USO ####

            for rec in dic_reclaimer['reclaimers']: #agora para todos os recs nos pátios
                count = 0
                n_max = 0
                while count < len(dic_reclaimer['reclaim_schedule'][rec]):  # com esse while vou passar por todos os gaps de tempo e espaço do respectivo rec
                    test_a = a in range(dic_reclaimer['reclaim_schedule'][rec][count][0], dic_reclaimer['reclaim_schedule'][rec][count][1])  # a está entre a' e b'?
                    test_b = b in range(dic_reclaimer['reclaim_schedule'][rec][count][0], dic_reclaimer['reclaim_schedule'][rec][count][1])  # b está entre a' e b'?
                    # print(dic_reclaimer['reclaim_schedule'][rec][count][0], dic_reclaimer['reclaim_schedule'][rec][count][1])
                    # print(test_a, test_b)
                    if test_a == True or test_b == True:  #se true para algum, então terá +1 rec em uso no gap de tempo
                        n_max += 1  #somo mais um
                    count += 1

            #depois de testar todos os gaps de tempo de todos os recs, não só os que servem ao mesmo pad de r atual, checamos se n_max obedece o número máximo de recs em uso
            if n_max > dic_instance['maximum_reclaimers_use']: #se é maior
                var = False  #então, não podemos usar r nesse tempo, pois teremos mais recs em uso do que o permitido


            #### RETORNANDO ####

            if var == True:
                print('VAR TRUE, int a_b: ', interval_a_b)
                return interval_a_b
            else:
                interval_a_b[0] = dic_instance['infinite']  #se n for possivel usar o gap ab, então retorno a como infinito, pois não passará na linha 10 do proc 3
                print('VAR FALSE, int a_b: ', interval_a_b)
                return interval_a_b



            #reclaim_s_using_r_during_ab_avoiding_clashes_respecting_nummxr(dic_reclaimer, dic_instance, a, b, r, R_s_s_p, s, dic_stockpile)
            print('TESTES')


        #SE OS TESTES INDICAREM QUE NÃO PODEMOS USAR R, RETORNAR EARLY_TIME = DIC_INSTANCE['INFINITE'] PORQUE ELE NAO VAI PASSAR NO TESTE DO PROC 3

    # # else:
    # #     reclaim_schedule = (early_time, early_time + dic_stockpile['time_reclaim_stockpile'][s] )
    #

    return
