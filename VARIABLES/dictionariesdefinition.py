import os

# #LISTS OF LABELS PARAMETERS - METHOD 1
# V = []
# S = []
# B = []
# P = []
# K = []
# L = []
# R = []
# #LIST OF LISTS OF LABELS PARAMETERS - METHOD 2
# Kp = []
# Rp = []
# Sv = []
# Sl = []
# Ls = []
# #LIST OF LISTS OF INTS PARAMETERS - METHOD 3
# NumMovSL = []
# LodTonSL = []
# #LIST OF INTS PARAMETERS - METHOD 4
# nv = []
# NomV = []
# EtaV = []
# BufAtlV = []
# BufDtaV = []
# BufLtdV = []
# LenS = []
# DurRecS = []
# LenP = []
# CapDurK = []
# CapMovL = []
# CapTonL = []
# BufDisP = []
# DurRhh = []
# #UNIQUE INTS PARAMETERS - METHOD 5
# NumMxR = []
# Inf = []
# #EMPTY PARAMETERS
# VL = []
# TD = []
# TL = []

######## Armazenar a instancia como um dicionario ##########
dic_instance = {
    'instance_name'                 : {}, # input         # instance .txt file name
    'ships'                         : {}, # 'V'           # set of ships (lista de str)
    'stockpiles'                    : {}, # 'S'           # set of stockpiles (lista de str)
    'berths'                        : {}, # 'B'           # set of berths (lista de str)
    'pads'                          : {}, # 'P'           # set of pads (lista de str)
    'stacker_streams'               : {}, # 'K'           # set of stacker streams (lista de str)
    'load_points'                   : {}, # 'L'           # set of load points (lista de str)
    'reclaimers'                    : {}, # 'R'           # set of reclaimers (lista de str)

    'stacker_streams_pad'           : {}, # 'Kp'          # set of stacker streams that service pad p (lista de listas de str)
    'reclaimers_pad'                : {}, # 'Rp'          # set of reclaimers that service pad p (lista de listas de str)
    'order_stockpiles_ship'         : {}, # 'Sv'          # set of stockpiles of ship v, given in the order in which they must be reclaimed (lista de listas de str)
    'least_stockpiles_lp'           : {}, # 'Sl'          # set of stockpiles that require at least one coal movement from load point l
    'least_lp_stockpile'            : {}, # 'Ls'          # set of load points from which stockpile s requires at least one coal movement

    'total_mov_stockpile_lp'        : {}, # 'NumMovSL'    # total number of coal movements that must be carried out for stockpile s from load point l (lista de listas de int)
    'tonnage_mov_stockpile_lp'      : {}, # 'LodTonSL'    # load (tonnage) of a coal movement for stockpile s from load point l (lista de listas de int)

    'total_stockpiles_ship'         : {}, # 'nv'          # the number of stockpiles of v (int)
    'nomination_ship'               : {}, # 'NomV'        # nomination time of ship v (lista de int)
    'eta_ship'                      : {}, # 'EtaV'        # estimated time of arrival of ship v (lista de int)
    'time_elapse_arrive_load'       : {}, # 'BufAtlV'     # amount of time that must elapse after ship v arrives at a berth before loading can begin (lista de int)
    'time_elapse_depart_arrive'     : {}, # 'BufDtaV'     # amount of time that must elapse after ship v departs a berth before the next ship can arrive (lista de int)
    'time_elapse_load_depart'       : {}, # 'BufLtdV'     # amount of time that must elapse after ship v has been loaded, before it can depart (lista de int)
    'length_stockpile'              : {}, # 'LenS'        # length of stockpile s on a pad (lista de int)
    'time_reclaim_stockpile'        : {}, # 'DurRecS'     # amount of time it takes to reclaim stockpile s (lista de int)
    'lenght_pad'                    : {}, # 'LenP'        # length of pad p (lista de int)
    'daily_cap_hours_stacker'       : {}, # 'CapDurK'     # daily capacity, in terms of working hours, of stacker stream k (lista de int)
    'daily_cap_coal_mov_lp'         : {}, # 'CapMovL'     # number of coal movements that can be accommodated at load point l in one day (lista de int)
    'daily_cap_tonnage_lp'          : {}, # 'CapTonL'     # daily capacity, in terms of tonnage, of load point l (lista de int)
    'distance_between_stockpiles'   : {}, # 'BufDisP'     # buffer distance that must be maintained between adjacent stockpiles on pad p (lista de int)
    'time_reclaimer_moves'          : {}, # 'DurRhh'      # amount of time that elapses when reclaimer r moves from position h to position h' (lista de int)

    'maximum_reclaimers_use'        : {}, # 'NumMxR'      # maximum number of reclaimers that can be in use at one time (number of ship loaders) (int)
    'infinite'                      : {}, # 'Inf'         # parameter that represents a very large number, which in this problem can be read as infinite. It will be an auxiliary parameter to generate TD and TL (int) (int)

    'large_ships'                   : {}, # 'VL'          # set of large ships (lista de str)
    'times_start_of_day'            : {}, # 'TD'          # set of times representing the start of a day (int) - The parameter will be generated in Python
    'times_large_ship_depart'       : {}, # 'TL'          # set of times at which a large ship can depart (float) - The parameter will be generated in Python
                }



######## Armazenar entradas e saídas referentes aos navios como um dicionário ##########
dic_ship = {
    'instance_name'                 : {}, # input         # instance .txt file name
    'ships'                         : {}, # 'V'           # set of ships (lista de str)
    'eta_ship'                      : {}, # 'EtaV'        # estimated time of arrival of ship v (lista de int)
    'total_stockpiles_ship'         : {}, # 'nv'          # the number of stockpiles of v (int)
    'order_stockpiles_ship'         : {}, # 'Sv'          # set of stockpiles of ship v, given in the order in which they must be reclaimed (lista de listas de str)
    'nomination_ship'               : {}, # 'NomV'        # nomination time of ship v (lista de int)
    'berth_assigned'                : {}, # 'Bv'          # !!!! berth to which ship v is assigned (output)
    'arrival_time_berth'            : {}, # 'TArrV'       # !!!! time of arrival of ship v at the berth in berth_assigned (output)
    'time_departure'                : {}, # -             # time of departure of ship v from the berth in berth_assigned (output)
    'time_rec_last_stockpile'       : {}, # -             # time at which reclaiming of the last stockpile of ship v finishes (output)
            }

######## Armazenar entradas e saídas referentes as pilhas como um dicionário ##########
dic_stockpile = {
    'instance_name'                 : {}, # input         # instance .txt file name
    'stockpiles'                    : {}, # 'S'           # set of stockpiles (lista de str)
    'least_lp_stockpile'            : {}, # 'Ls'          # set of load points from which stockpile s requires at least one coal movement
    'length_stockpile'              : {}, # 'LenS'        # length of stockpile s on a pad (lista de int)
    'time_reclaim_stockpile'        : {}, # 'DurRecS'     # amount of time it takes to reclaim stockpile s (lista de int)
    'total_mov_stockpile_lp'        : {}, # 'NumMovSL'    # total number of coal movements that must be carried out for stockpile s from load point l (lista de listas de int)
    'tonnage_mov_stockpile_lp'      : {}, # 'LodTonSL'    # load (tonnage) of a coal movement for stockpile s from load point l (lista de listas de int)
    'pad_assembled'                 : {}, # -             # pad on which stockpile s is assembled (output)
    'position_pad'                  : {}, # -             # position of stockpile s on its pad (position of the easternmost edge of s) (output)
    'reclaimer'                     : {}, # -             # reclaimer used in reclaiming stockpile s (output)
    'n_coalmov_lp_time'             : {}, # -             # number of coal movements carried out for stockpile s from load point l at time t in TD (output)
    'time_rec_start'                : {}, # -             # time at which reclaiming of stockpile s starts (output)
    'time_build_start'              : {}, # -             # time at which building of stockpile s starts (the day the first coal movement for s takes place (output)
    'time_build_finish'             : {}, # -             # time at which building of stockpile s finishes (one day after the last coal movement for s takes place (output)
    'time_rec_finish'               : {}, # -             # rime at which reclaiming of stockpile s finishes (output)
    'v_stockpiles'                  : {}, # -             # navio da stocpikle s
                }

######## Armazenar entradas e saídas referentes aos berços como um dicionário ##########
dic_berth = {
    'instance_name'                 : {},  # input         # instance .txt file name
    'berths'                        : {}, # 'B'            # set of berths (lista de str)
    'ships_scheduled'               : {}, # 'Vb'           # !!!! set of ships scheduled to arrive at berth b (input/output)
            }

######## Armazenar entradas e saídas referentes aos pátios como um dicionário ##########
dic_pad = {
    'instance_name'                 : {}, # input         # instance .txt file name
    'pads'                          : {}, # 'P'           # set of pads (lista de str)
    'lenght_pad'                    : {},  # 'LenP'        # length of pad p (lista de int)
    'stacker_streams_pad'           : {}, # 'Kp'          # set of stacker streams that service pad p (lista de listas de str)
    'reclaimers_pad'                : {}, # 'Rp'          # set of reclaimers that service pad p (lista de listas de str)
    'stockpiles_on_time'            : {}, # -             # set of stockpiles on pad p at time t (input/output)
    'length_stockpile'              : {}, # 'LenS'        # length of stockpile s on a pad (lista de int)
    'time_build_start'              : {},# -             # time at which building of stockpile s starts (the day the first coal movement for s takes place (output)
    'time_rec_finish'               : {},  # -             # time at which reclaiming of stockpile s finishes (output)
    'position_pad'                  : {},# -             # position of stockpile s on its pad (position of the easternmost edge of s) (output)
    'distance_between_stockpiles'   : {}, # 'BufDisP'     # buffer distance that must be maintained between adjacent stockpiles on pad p (lista de int)

}

######## Armazenar entradas e saídas referentes aos stacker streams como um dicionário ##########
dic_stacker_stream = {
    'instance_name'                 : {}, # input         # instance .txt file name
    'stacker_streams'               : {}, # 'K'           # set of stacker streams (lista de str)
    'daily_cap_hours_stacker'       : {}, # 'CapDurK'     # daily capacity, in terms of working hours, of stacker stream k (lista de int)
    'stockpiles_pad_serviced'       : {}, # -             # set of stockpiles located on a pad serviced by stacker stream k (input/output)
    'res_cap_hours_stacker'         : {}, # -             # residual capacity of stacker s on day t - algo como (t, stacker, capacity)
                     }

######## Armazenar entradas e saídas referentes aos load points como um dicionário ##########
dic_load_point = {
    'instance_name'                 : {}, # input         # instance .txt file name
    'load_points'                   : {}, # 'L'           # set of load points (lista de str)
    'least_stockpiles_lp'           : {}, # 'Sl'          # set of stockpiles that require at least one coal movement from load point l
    'total_mov_stockpile_lp'        : {}, # 'NumMovSL'    # total number of coal movements that must be carried out for stockpile s from load point l (lista de listas de int)
    'tonnage_mov_stockpile_lp'      : {}, # 'LodTonSL'    # load (tonnage) of a coal movement for stockpile s from load point l (lista de listas de int)
    'daily_cap_coal_mov_lp'         : {}, # 'CapMovL'     # number of coal movements that can be accommodated at load point l in one day (lista de int)
    'daily_cap_tonnage_lp'          : {}, # 'CapTonL'     # daily capacity, in terms of tonnage, of load point l (lista de int)
    'n_coalmov_stockpile_time'      : {}, # -             # number of coal movements carried out for stockpile s from load point l at time t in TD (output)
    'res_cap_tonnage_l'             : {}, # -             # residual capacity of load point l on day t (t, load point, capacity)
     't_scheduled_coal_movement'    : {} ,               #tempo em que há pelo menos 1 movimentação de carvão de l, não há tempos repetidos
'res_cap_coal_mov_lp' : {}
                 }


######## Armazenar entradas e saídas referentes aos reclaimers como um dicionário ##########
dic_reclaimer = {
    'instance_name'                 : {}, # input         # instance .txt file name
    'reclaimers'                    : {}, # 'R'           # set of reclaimers (lista de str)
    'stockpiles_reclaimed'          : {}, # -             # set of stockpiles reclaimed by reclaimer r (input/output)
                }

######## Armazenar entradas e saídas referentes ao tempo como um dicionário ##########
dic_time = {
    'instance_name'                 : {}, # input         # instance .txt file name
    'times_start_of_day'            : {}, # 'TD'          # set of times representing the start of a day (int) - The parameter will be generated in Python
    'n_coalmov_stockpile_lp'        : {}, # -             # number of coal movements carried out for stockpile s from load point l at time t in TD (output)
    'stockpiles_on_pad'             : {}, # -             # set of stockpiles on pad p at time t (input/output)
    'reclaimers_in_use'             : {}, # -             # set of reclaimers in use at time t (input/output-auxiliar-temporario-utilitario)
           }
