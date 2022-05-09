import csv
import os

import pandas as pd
import openpyxl
import xlsxwriter

# def retorna_chave_com_maior_len(dic):
#     aux = -1
#
#     for key in dic.keys():
#         print('key',key)
#
#         if dic[key] == 'instance_name':
#             aux = -1
#             print('key == instance_name')
#         else:
#             len_key = len(dic[key])
#             print('len,key', len_key)
#             if len_key > aux:
#                 aux = len_key
#                 max_len_key = key
#                 print('max_len_key',max_len_key)
#     return max_len_key


def generate_csv_outputs(dic_ship, dic_berth, dic_stockpile, dic_pad, dic_load_point, dic_stacker_stream, dic_reclaimer):

    #MODELO 1
    # with open("csv_test_modelo_1.csv", 'w') as file:
    #     writer = csv.writer(file)
    #     for k, v in dic_ship.items():
    #         writer.writerow([k, v])


    #MODELO 2
    # dct_arr = [dic_ship]
    # labels = ['instance_name','ships','eta_ship','total_stockpiles_ship','order_stockpiles_ship',
    #            'nomination_ship', 'berth_assigned', 'arrival_time_berth',
    #            'time_departure', 'time_rec_last_stockpile']
    # try:
    #     with open('csv_test_modelo_2.csv', 'w') as file:
    #         writer = csv.DictWriter(file, fieldnames=labels)
    #         writer.writeheader()
    #         for elem in dct_arr:
    #             writer.writerow(elem)
    # except IOError:
    #     print('I/0 error')
    #

    #df_b.to_csv('csv_test_modelo_3.csv')


    #MODELO 3

    #TRATANDO AS SAÍDAS

    #DIC_BERTH
    lista_dic_berth = []
    for b in dic_berth['berths']:
        count = 0
        while count < len(dic_berth['ships_scheduled'][b]):

            dic_aux = {}
            dic_aux = dict(Berth = dic_berth['berths'][b],
                           Scheduled_Ships = dic_berth['ships_scheduled'][b][count],
                           Time_arrival_at_the_berth = dic_berth['arrival_time_berth'][b][count],
                           Departure_time_from_the_berth = dic_berth['time_departure'][b][count],
                           )

            lista_dic_berth.append(dic_aux)

            count += 1

    df_b = pd.DataFrame(lista_dic_berth)
    #print(df_b)

    #DIC_SHIP
    lista_dic_ship = []
    for s in dic_ship['ships']:
        count = 0
        while count < len(dic_ship['order_stockpiles_ship'][s]):

            dic_aux = dict(Ship = dic_ship['ships'][s],
                           Ships_ETA = dic_ship['eta_ship'][s],
                           Total_Stockipiles_per_ship = dic_ship['total_stockpiles_ship'][s],
                           Orderned_Stockpiles_per_ship = dic_ship['order_stockpiles_ship'][s][count],   #O QUE É MAIS INTERESSANTE, DEIXAR A LISTA EM UMA ÚNICA CÉLULA OU DIVIDIR EM MAIS DE UMA REPETINDO OS DEMAIS DADOS?
                           Ship_nomination = dic_ship['nomination_ship'][s],                             #A INFORMAÇÃO QUE O USUÁRIO QUER É UMA LISTA ORDENADA, DE FATO.
                           Berth_assigned = dic_ship['berth_assigned'][s],
                           Time_arrival_at_the_berth = dic_ship['arrival_time_berth'][s],
                           Departure_time_from_the_berth = dic_ship['time_departure'][s],
                           Time_of_reclaimaing_of_the_last_stockpile = dic_ship['time_rec_last_stockpile'][s]
                           )

            lista_dic_ship.append(dic_aux)

            count += 1


    df_sp = pd.DataFrame(lista_dic_ship)
    #print(df_sp)

    #DIC_STOCKPILE
    lista_dic_stockpile = []
    for s in dic_stockpile['stockpiles']:
        count = 0
        while count < len(dic_stockpile['n_coalmov_lp_time'][s]):
            dic_aux = dict(Stockpile = dic_stockpile['stockpiles'][s],
                           Lps_that_stockpile_needs_mov = dic_stockpile['least_lp_stockpile'][s],
                           Stockpiles_length = dic_stockpile['length_stockpile'][s],
                           Stockpiles_duration_of_reclaiming = dic_stockpile['time_reclaim_stockpile'][s],
                           Total_mov_of_lp_to_stockpile = dic_stockpile['total_mov_stockpile_lp'][s],
                           Tonnage_mov_of_lp_to_stockpile = dic_stockpile['tonnage_mov_stockpile_lp'][s],
                           Stockpiles_pad = dic_stockpile['pad_assembled'][s],
                           Stockpiles_position = dic_stockpile['position_pad'][s],
                           Stockpiles_reclaimer = dic_stockpile['reclaimer'][s],
                           Number_of_mov_from_lp_to_Stockpile_at_time = dic_stockpile['n_coalmov_lp_time'][s],
                           Stockpile_time_build_starts = dic_stockpile['time_build_start'][s],
                           Stockpile_time_build_finishes = dic_stockpile['time_build_finish'][s],
                           Stockpile_time_reclaim_starts = dic_stockpile['time_rec_start'][s],
                           Stockpile_time_reclaim_finishes=dic_stockpile['time_rec_finish'][s]
                           )

            lista_dic_stockpile.append(dic_aux)

            count += 1

    df_s = pd.DataFrame(lista_dic_stockpile)
    #print(df_s)


    #DIC_PAD
    lista_dic_pad = []
    for p in dic_pad['pads']:
        count = 0
        while count < len(dic_pad['stockpiles'][p]):
            dic_aux = dict(Pad = dic_pad['pads'][p],
                           Pad_lenght = dic_pad['lenght_pad'][p],
                           Stackers_that_serve_the_pad = dic_pad['stacker_streams_pad'][p],
                           Reclaimers_that_serve_the_pad = dic_pad['reclaimers_pad'][p],
                           Standard_distance_between_stockpiles_on_pad = dic_pad['distance_between_stockpiles'][p],
                           Stockpiles_at_the_pad = dic_pad['stockpiles'][p],
                           Stockpiles_on_time_at_the_pad = dic_pad['stockpiles_on_time'][p],
                           Length_of_stockpile_on_the_pad = dic_pad['length_stockpile'][p],
                           Stockpiles_position_at_the_pad=dic_pad['position_pad'][p],
                           Time_build_start_of_stockpile_on_the_pad = dic_pad['time_build_start'][p],
                           Time_reclaiming_finishes_of_stockpile_on_the_pad = dic_pad['time_rec_finish'][p]
                           )

            lista_dic_pad.append(dic_aux)

            count += 1

    df_p = pd.DataFrame(lista_dic_pad)
    #print(df_p)

    #DIC_LOAD_POINT
    list_dic_load_point = []

    for l in dic_load_point['load_points']:
        count = 0
        while count < len(dic_load_point['n_coalmov_stockpile_time'][l]):
            dic_aux = dict(Load_point = dic_load_point['load_points'][l],
                           Stockpiles_that_need_mov_from_lp = dic_load_point['least_stockpiles_lp'][l],
                           Total_number_of_movements_from_lp_to_s = dic_load_point['total_mov_stockpile_lp'][l],
                           Tonnage_of_the_mov_to_stockpile_from_lp = dic_load_point['tonnage_mov_stockpile_lp'][l],
                           Daily_capacity_of_mov_from_lp = dic_load_point['daily_cap_coal_mov_lp'][l],
                           Daily_capacity_of_mov_tonnage_from_lp = dic_load_point['daily_cap_tonnage_lp'][l],
                           n_coalmov_stockpile_time = dic_load_point['n_coalmov_stockpile_time'][l],
                           Residual_capacity_tonnage_of_the_load_point_on_the_day =dic_load_point['res_cap_tonnage_l'][l],
                           Residual_capacity_mov_of_the_load_point_on_the_day=dic_load_point['res_cap_coal_mov_lp'][l],
                           Day_of_residual_capacity_of_the_load_point = dic_load_point['t_scheduled_coal_movement'][l]
                           )

            list_dic_load_point.append(dic_aux)
            count += 1

    df_lp = pd.DataFrame(list_dic_load_point)
    #print(df_lp)



    #DIA_STACKER_STREAM
    list_dic_stacker_stream = []

    for k in dic_stacker_stream['stacker_streams']:
        count = 0
        while count < len(dic_stacker_stream['stockpiles_pad_serviced'][k]):
            dic_aux = dict(Stacker_streams = dic_stacker_stream['stacker_streams'][k],
                           Daily_cap_hours_stacker = dic_stacker_stream['daily_cap_hours_stacker'][k],
                           Stockpiles_pad_serviced = dic_stacker_stream['stockpiles_pad_serviced'][k],
                           res_cap_hours_stacker = dic_stacker_stream['res_cap_hours_stacker'][k],
                           t_scheduled_stacking = dic_stacker_stream['t_scheduled_stacking'][k],
                           productivity = dic_stacker_stream['productivity'][k]
                           )

            list_dic_stacker_stream.append(dic_aux)
            count += 1

    df_ss = pd.DataFrame(list_dic_stacker_stream)
    #print(df_ss)




    #DIA_RECLAIMER
    list_dic_reclaimer = []

    for r in dic_reclaimer['reclaimers']:
        count = 0
        while count < len(dic_reclaimer['stockpiles_reclaimed'][r]):
            dic_aux = dict(Reclaimers = dic_reclaimer['reclaimers'][r],
                           stockpiles_reclaimed = dic_reclaimer['stockpiles_reclaimed'][r],
                           inital_position_reclaimers = dic_reclaimer['inital_position_reclaimers'][r],
                           velocity_reclaimeirs = dic_reclaimer['velocity_reclaimeirs'][r],
                           reclaim_schedule = dic_reclaimer['reclaim_schedule'][r],
                           space_of_reclaim_schedule = dic_reclaimer['space_of_reclaim_schedule'][r]
                           )

            list_dic_reclaimer.append(dic_aux)
            count += 1

    df_r = pd.DataFrame(list_dic_reclaimer)
    #print(df_r)



    # # Criando os dataframes Pandas para armazenar os dados
    # df1 = pd.DataFrame({'Data': [2, 4, 6, 8]})
    # df2 = pd.DataFrame({'Data': [100, 150, 200, 250]})
    # df3 = pd.DataFrame({'Data': [3, 6, 9, 12]})
    #
    # # Usando o ExcelWriter, cria um doc .xlsx, usando engine='xlsxwriter'
    # writer = pd.ExcelWriter('tabelas_exemplo.xlsx', engine='xlsxwriter')
    #
    # # Armazena cada df em uma planilha diferente do mesmo arquivo
    # df1.to_excel(writer, sheet_name='Tabela 1')
    # df2.to_excel(writer, sheet_name='Tabela 2')
    # df3.to_excel(writer, sheet_name='Tabela 3')
    #
    # # Fecha o ExcelWriter e gera o arquivo .xlsx
    # writer.save()

    #os.chdir("OUTPUT")

    writer = pd.ExcelWriter(dic_ship['instance_name'][:-4] + '.xlsx', engine='xlsxwriter')

    df_b.to_excel(writer, sheet_name='DIC_BERTH')
    df_sp.to_excel(writer, sheet_name='DIC_SHIP')
    df_s.to_excel(writer, sheet_name='DIC_STOCKPILE')
    df_p.to_excel(writer, sheet_name='DIC_PAD')
    df_lp.to_excel(writer, sheet_name='DIC_LOAD_POINT')
    df_ss.to_excel(writer, sheet_name='DIC_STACKER_STREAM')
    df_r.to_excel(writer, sheet_name='DIC_RECLAIMER')

    writer.save()
    return

