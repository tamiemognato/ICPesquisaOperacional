import csv
import pandas as pd


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

    lista_dic_berth = []
    for b in dic_berth['berths']:
        count = 0
        while count < len(dic_berth['ships_scheduled'][b]):

            dic_aux = {}
            dic_aux = dict(Berth = dic_berth['berths'][b],
                           Scheduled_Ships = dic_berth['ships_scheduled'][b][count],
                           Time_arrivel_at_the_berth = dic_berth['arrival_time_berth'][b][count],
                           Departure_time_from_the_berth = dic_berth['time_departure'][b][count],
                           )

            lista_dic_berth.append(dic_aux)

            count += 1

    df_b = pd.DataFrame(lista_dic_berth)
    print(df_b)



    #df_b.to_csv('csv_test_modelo_3.csv')

    return

