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

def generate_visual_graphic_outputs(dic_ship, dic_berth, dic_stockpile, dic_pad, dic_load_point, dic_stacker_stream, dic_reclaimer):
    #função com entrada de dicionários com listas e saída de uma lista com vários dicionários
    #aplicando ao dic_berth primeiramente
    #ENTRADA - DIC_BERTH: {'instance_name': '00.txt', 'berths': [0, 1], 'ships_scheduled': [[1, 2], [0]],
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
            dic_aux = dict(berths = dic_berth['berths'][b],
                           ships_scheduled = dic_berth['ships_scheduled'][b][count],
                           arrival_time_berth = dic_berth['arrival_time_berth'][b][count],
                           time_departure = dic_berth['time_departure'][b][count],
                           ships_legend = (dic_berth['arrival_time_berth'][b][count] + dic_berth['time_departure'][b][count] ) / 2
                           )

            lista_dic_berth.append(dic_aux)

            count += 1

    #print(lista_dic_berth)

    df_b = pd.DataFrame(lista_dic_berth)
    #print(df_b)

    # GANTT DOS BERÇOS - ok
    # Berth to wichi ship v is assigned + time of arrival of ship v at berth bv
    # + time of departure of ship v from berth bv

    graph_berths = (
        ggplot(data = df_b)
        + geom_segment(aes(x='arrival_time_berth', y='berths', xend='time_departure', yend='berths', size = 50, color = "ships_scheduled"))
        + scale_colour_desaturate() #gradient, desaturate
        + geom_label(aes(label = "arrival_time_berth",  x = "arrival_time_berth", y = "berths", size = 50, color = "ships_scheduled"))
        + geom_label(aes(label="time_departure", x="time_departure", y="berths", size=50, color = "ships_scheduled"))
        + geom_label(aes(label="ships_scheduled", x="ships_legend", y="berths", size=50))
        + ggtitle(title = 'Berths Schedule - Ships moored')
        + labs(x = "Time", y = 'Berths')
        + theme_matplotlib() + theme(legend_position = 'none') #matplotlib, classic
        + scale_y_continuous(breaks = (0, 100, 1))
        #+ scale_x_continuous(breaks = (0, 500, 50))
    )

    # print(graph_berths)

    ###############################################   RECLAIMERES   ####################################################
    lista_dic_reclaimer = []
    for r in dic_reclaimer['reclaimers']:
        count = 0
        while count < len(dic_reclaimer['stockpiles_reclaimed'][r]):

            dic_aux = {}
            dic_aux = dict(reclaimers = dic_reclaimer['reclaimers'][r],
                           stockpiles_reclaimed = dic_reclaimer['stockpiles_reclaimed'][r][count],
                           reclaim_start = dic_reclaimer['reclaim_schedule'][r][count][0],
                           reclaim_finish = dic_reclaimer['reclaim_schedule'][r][count][1],
                           stockpiles_reclaimed_legend = (dic_reclaimer['reclaim_schedule'][r][count][0]
                                                +dic_reclaimer['reclaim_schedule'][r][count][1]) /2
                           )

            lista_dic_reclaimer.append(dic_aux)

            count += 1

    #print(lista_dic_reclaimer)

    df_r = pd.DataFrame(lista_dic_reclaimer)
    #print(df_r)

    # GANTT DOS RECLAIMERS
    # Reclaimer used in reclaiming stockpile s + time at wich reclaiming pf stockpile s starts
    # + time at which reclaiming of stockpile s finishes

    graph_reclaimers = (
        ggplot(data = df_r)
        + geom_segment(aes(x='reclaim_start', y='reclaimers', xend='reclaim_finish', yend='reclaimers', size = 50, color = "stockpiles_reclaimed"))
        + scale_colour_desaturate() #gradient, desaturate
        + geom_label(aes(label = "reclaim_start",  x = "reclaim_start", y = "reclaimers", size = 50, color = "stockpiles_reclaimed"))
        + geom_label(aes(label="reclaim_finish", x="reclaim_finish", y="reclaimers", size=50, color = "stockpiles_reclaimed"))
        + geom_label(aes(label="stockpiles_reclaimed", x = "stockpiles_reclaimed_legend", y="reclaimers", size=50 ))
        + labs(title = 'Reclaimers schedule - Stockpiles reclaimed', x = "Time", y = 'Reclaimers')
        + theme_matplotlib() + theme(legend_position='none')  # matplotlib, classic
        + scale_y_continuous(breaks=(0, 100, 1))
        #+ scale_x_continuous(breaks = (100, 500, 25))

    )
    # print(graph_reclaimers)

    ###############################################   STACKERS   #######################################################

    lista_dic_stacker = []
    for stk in dic_stacker_stream['stacker_streams']:
        count = 0
        while count < len(dic_stacker_stream['stockpiles_pad_serviced'][stk]):
            dic_aux = {}
            dic_aux = dict(stacker_streams=dic_stacker_stream['stacker_streams'][stk],
                           stockpiles_pad_serviced=dic_stacker_stream['stockpiles_pad_serviced'][stk][count],
                           res_cap_hours_stacker=dic_stacker_stream['res_cap_hours_stacker'][stk][count],
                           t_scheduled_stacking=dic_stacker_stream['t_scheduled_stacking'][stk][count])

            lista_dic_stacker.append(dic_aux)

            count += 1

    #print(lista_dic_stacker)

    df_stk = pd.DataFrame(lista_dic_stacker)
    #print(df_stk)

    graph_stackers = (
        ggplot(data = df_stk)
        + geom_bar(aes(x = 't_scheduled_stacking', y = 'res_cap_hours_stacker'), stat = 'identity', width = 5, position=position_dodge2(preserve = "single")) + scale_colour_desaturate() #gradient, desaturate
        + geom_label(aes(label = 'res_cap_hours_stacker', x = 't_scheduled_stacking', y = 'res_cap_hours_stacker', color = 'stacker_streams', size = 10))  + scale_colour_desaturate() #gradient, desaturate
        + facet_wrap('stacker_streams', ncol = 4)
        + geom_label(aes(label = 't_scheduled_stacking', x = 't_scheduled_stacking', y = 10.0, color = 'stacker_streams', size = 10))
        + geom_label(aes(label='stockpiles_pad_serviced', x='t_scheduled_stacking', y=9.5, color='stacker_streams', size=10))
        + labs(title='Residual capacity of Stackers - Stockpiles that consumed hours', x="Time", y='Residual capacity of Stackers')
        + theme_matplotlib() + theme(legend_position='none', axis_text_x= element_text(angle =90, vjust = 1), subplots_adjust = { 'wspace' : 0.25})  # matplotlib, classic
        + scale_y_continuous(limits=(0, 10))

    )

    # print(graph_stackers)

    ##############################################    STOCKPILES, PADS    ##############################################
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


    # print(lista_dic_stockpile_pad_0)
    # print(lista_dic_stockpile_pad_1)

    df_s_pad_0 = pd.DataFrame(lista_dic_stockpile_pad_0)
    #print(df_s_pad_0)

    df_s_pad_1 = pd.DataFrame(lista_dic_stockpile_pad_1)
    # print(df_s_pad_1)

    # GANTT DOS PADS x STOCKPILES
    # Pad on which stockpile s is assembled + position of stockpile s on its pad + number of coal movements carried out for stockpile s from load point l at time t
    # + time at which building of stockpile s starts + time at which reclaiming of stockpile s finishes

    graph_stockpiles_pad_0 = (
        ggplot(data = df_s_pad_0)

        + geom_rect(aes(xmin = "time_build_start", xmax = "time_rec_finish", ymin = "position_pad_start", ymax = "position_pad_finish", fill = "stockpiles"))  + scale_fill_desaturate() #gradient, desaturate
        + geom_label(aes(label = "stockpiles",  x = "stockpile_label_x", y = "stockpile_label_y", size = 15, color = "stockpiles" )) + scale_colour_desaturate() #gradient, desaturate
        + geom_label(aes(label="time_build_start", x="time_build_start", y="stockpile_label_y", size=15, color ="stockpiles")) + scale_colour_desaturate() #gradient, desaturate
        + geom_label(aes(label="time_build_finish", x="time_build_finish", y="stockpile_label_y", size=15, color="stockpiles")) + scale_colour_desaturate() #gradient, desaturate
        + geom_label(aes(label="time_rec_start", x="time_rec_start", y="stockpile_label_y", size=15, color="stockpiles")) + scale_colour_desaturate() #gradient, desaturate
        + geom_label(aes(label="time_rec_finish", x="time_rec_finish", y="stockpile_label_y", size=15, color="stockpiles")) + scale_colour_desaturate() #gradient, desaturate
        + geom_label(aes(label="position_pad_start", x="time_build_start", y="position_pad_start", size=15))

        + labs(title="PAD 0 - Stockpiles position, stacking and reclaiming", x="Time", y="Pad occupation")
        + theme_matplotlib() + theme(legend_position='none')


    )

    # print(graph_stockpiles_pad_0)

    graph_stockpiles_pad_1 = (
        ggplot(data = df_s_pad_1)

        + geom_rect(aes(xmin = "time_build_start", xmax = "time_rec_finish", ymin = "position_pad_start", ymax = "position_pad_finish", fill = "stockpiles")) + scale_fill_desaturate() #gradient, desaturate
        + geom_label(aes(label = "stockpiles",  x = "stockpile_label_x", y = "stockpile_label_y", size = 15, color = "stockpiles" )) + scale_colour_desaturate() #gradient, desaturate
        + geom_label(aes(label="time_build_start", x="time_build_start", y="stockpile_label_y", size=15, color ="stockpiles")) + scale_colour_desaturate() #gradient, desaturate
        + geom_label(aes(label="time_build_finish", x="time_build_finish", y="stockpile_label_y", size=15, color="stockpiles")) + scale_colour_desaturate() #gradient, desaturate
        + geom_label(aes(label="time_rec_start", x="time_rec_start", y="stockpile_label_y", size=15, color="stockpiles")) + scale_colour_desaturate() #gradient, desaturate
        + geom_label(aes(label="time_rec_finish", x="time_rec_finish", y="stockpile_label_y", size=15, color="stockpiles")) + scale_colour_desaturate() #gradient, desaturate
        + geom_label(aes(label="position_pad_start", x="time_build_start", y="position_pad_start", size=15))
        + labs(title="PAD 1 - Stockpiles position, stacking and reclaiming", x="Time", y="Pad occupation")
        + theme_matplotlib() + theme(legend_position='none')

    )
    # print(graph_stockpiles_pad_1)

    ##############################################    LOAD POINTS    #################################################
    list_dic_load_point_0 = []
    list_dic_load_point_1 = []
    list_dic_lp_general = []

    for l in dic_load_point['load_points']:
        count = 0
        while count < len(dic_load_point['n_coalmov_stockpile_time'][l]):
            dic_aux = {}
            dic_aux = dict(load_point=dic_load_point['load_points'][l],
                           n_coalmov=dic_load_point['n_coalmov_stockpile_time'][l][count][1],
                           stockpile_n_coalmov=dic_load_point['n_coalmov_stockpile_time'][l][count][0],
                           time_n_coalmov=dic_load_point['n_coalmov_stockpile_time'][l][count][4]
                           )

            if dic_load_point['load_points'][l] == 0:
                list_dic_load_point_0.append(dic_aux)
            else:
                list_dic_load_point_1.append(dic_aux)


            #list_dic_load_point.append(dic_aux)
            count += 1

    df_lp0 = pd.DataFrame(list_dic_load_point_0)
    #print(df_lp0)

    df_lp1 = pd.DataFrame(list_dic_load_point_1)
    #print(df_lp1)

    # (stockpile, nº mov, load point, k em serviço, tempo)
    # (0            1       2               3           4)



    graph_n_lp0_s = (
            ggplot(data = df_lp0)
            + geom_point(aes(x ="time_n_coalmov", y ="n_coalmov", color = 'stockpile_n_coalmov' )) + scale_colour_desaturate()  # gradient, desaturate
            + geom_label(aes(label = 'time_n_coalmov', x ="time_n_coalmov", y ="n_coalmov", color = 'stockpile_n_coalmov', size = 15)) + scale_colour_desaturate()
            + labs(title="Load Point 0 - Coal movements from LP1 / stockpile", x="Time", y="Number of coal movements")
            + facet_wrap('stockpile_n_coalmov')
            + theme_matplotlib() + theme(legend_position='none')

    )

    # print(graph_n_lp0_s)

    graph_n_lp1_s = (
        ggplot(data = df_lp1)
        +geom_point(aes(x ="time_n_coalmov", y ="n_coalmov", color = 'stockpile_n_coalmov' )) + scale_colour_desaturate()
        +geom_label(aes(label = 'time_n_coalmov', x ="time_n_coalmov", y ="n_coalmov", color = 'stockpile_n_coalmov', size = 15)) + scale_colour_desaturate()
        + labs(title="Load Point 1 - Coal movements from LP1 / stockpile", x="Time", y="Number of coal movements")
        + facet_wrap('stockpile_n_coalmov')
        + theme_matplotlib() + theme(legend_position='none')

    )

    # print(graph_n_lp1_s)




    os.chdir("OUTPUT")
    ggsave(plot=graph_berths, filename = dic_berth['instance_name'][:-4] + '_berths_schedule')
    ggsave(plot=graph_reclaimers, filename = dic_reclaimer['instance_name'][:-4] + '_reclaimers_schedule')
    ggsave(plot=graph_stockpiles_pad_0, filename = dic_pad['instance_name'][:-4] + '_pad_0_schedule')
    ggsave(plot=graph_stockpiles_pad_1, filename = dic_pad['instance_name'][:-4] + '_pad_1_schedule')
    ggsave(plot=graph_stackers, filename = dic_stacker_stream['instance_name'][:-4] + '_stackers_usage_and_remaining_capacity')
    ggsave(plot=graph_n_lp0_s, filename = dic_load_point['instance_name'][:-4] + '_movements_lp0_for_stockpiles')
    ggsave(plot=graph_n_lp1_s, filename = dic_load_point['instance_name'][:-4] + '_movements_lp1_for_stockpiles')





    return