import csv
import pandas as pd
import openpyxl
import xlsxwriter



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
    print(df_sp)

    #DIC_STOCKPILE










    #df_b.to_csv('csv_test_modelo_3.csv')


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

    return

