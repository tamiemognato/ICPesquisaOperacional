import os
import re

# fill_in_dic_ship
# fill_in_dic_stockpile
# fill_in_dic_berth
# fill_in_dic_pad
# fill_in_dic_stacker_stream
# fill_in_dic_load_point
# fill_in_dic_reclaimer
# fill_in_dic_time
# print_dic_ship
# print_dic_stockpile
# print_dic_berth
# print_dic_pad
# print_dic_stacker_stream
# print_dic_load_point
# print_dic_reclaimer
# import print_dic_time




########### FILL IN FUNCTIONS FOR SECONDARY DICTIONARIES ###########
# The functions run the dic_instance, key by key, and fills the respective keys in the respective dictionaries with the data.

def fill_in_dic_ship(parameter):
    'texto texto texto'

    dic_ship = {
        'instance_name'             : [],   # input         # instance .txt file name
        'ships'                     : [],   # 'V'           # set of ships (lista de str)
        'eta_ship'                  : [],   # 'EtaV'        # estimated time of arrival of ship v (lista de int)
        'total_stockpiles_ship'     : [],   # 'nv'          # the number of stockpiles of v (int)
        'order_stockpiles_ship'     : [],   # 'Sv'          # set of stockpiles of ship v, given in the order in which they must be reclaimed (lista de listas de str)
        'nomination_ship'           : [],   # 'NomV'        # nomination time of ship v (lista de int)
        'berth_assigned'            : [],   # -             # berth to which ship v is assigned (output)
        'arrival_time_berth'        : [],   # -             # time of arrival of ship v at the berth in berth_assigned (output)
        'time_departure'            : [],   # -             # time of departure of ship v from the berth in berth_assigned (output)
        'time_rec_last_stockpile'   : [],   # -             # time at which reclaiming of the last stockpile of ship v finishes (output)
                }

    for k,v in dic_ship.items():
        if k in parameter:
            dic_ship[k] = parameter[k]
        else:
            for i in parameter['ships']:
                dic_ship[k].append(-1)

    return dic_ship

#########

def fill_in_dic_stockpile(parameter):

    dic_stockpile = {
        'instance_name'                 : [], # input         # instance .txt file name
        'stockpiles'                    : [], # 'S'           # set of stockpiles (lista de str)
        'least_lp_stockpile'            : [], # 'Ls'          # set of load points from which stockpile s requires at least one coal movement
        'length_stockpile'              : [], # 'LenS'        # length of stockpile s on a pad (lista de int)
        'time_reclaim_stockpile'        : [], # 'DurRecS'     # amount of time it takes to reclaim stockpile s (lista de int)
        'total_mov_stockpile_lp'        : [], # 'NumMovSL'    # total number of coal movements that must be carried out for stockpile s from load point l (lista de listas de int)
        'tonnage_mov_stockpile_lp'      : [], # 'LodTonSL'    # load (tonnage) of a coal movement for stockpile s from load point l (lista de listas de int)
        'pad_assembled'                 : [], # -             # pad on which stockpile s is assembled (output)
        'position_pad'                  : [], # -             # position of stockpile s on its pad (position of the easternmost edge of s) (output)
        'reclaimer'                     : [], # -             # reclaimer used in reclaiming stockpile s (output)
        'n_coalmov_lp_time'             : [], # -             # number of coal movements carried out for stockpile s from load point l at time t in TD (output)
        'time_rec_start'                : [], # -             # time at which reclaiming of stockpile s starts (output)
        'time_build_start'              : [], # -             # time at which building of stockpile s starts (the day the first coal movement for s takes place (output)
        'time_build_finish'             : [], # -             # time at which building of stockpile s finishes (one day after the last coal movement for s takes place (output)
        'time_rec_finish'               : [], # -             # rime at which reclaiming of stockpile s finishes (output)
                    }

    for k,v in dic_stockpile.items():
        if k in parameter:
            dic_stockpile[k] = parameter[k]
        else:
            for i in parameter['stockpiles']:
                dic_stockpile[k].append(-1)

    return dic_stockpile

#########

def fill_in_dic_berth(parameter):

    dic_berth = {
        'instance_name'                 : [], # input         # instance .txt file name
        'berths'                        : [], # 'B'           # set of berths (lista de str)
        'ships_scheduled'               : [], # -             # set of ships scheduled to arrive at berth b (input/output)
        'arrival_time_berth'            : [],
        'time_departure'                : [],
                }

    for k, v in dic_berth.items():
        if k in parameter:
            dic_berth[k] = parameter[k]
        else:
            for i in parameter['berths']:
                dic_berth[k].append([])

    return dic_berth

#########

def fill_in_dic_pad(parameter):

    dic_pad = {
        'instance_name'                 : [], # input         # instance .txt file name
        'pads'                          : [], # 'P'           # set of pads (lista de str)
        'lenght_pad'                    : [], # 'LenP'        # length of pad p (lista de int)
        'stacker_streams_pad'           : [], # 'Kp'          # set of stacker streams that service pad p (lista de listas de str)
        'reclaimers_pad'                : [], # 'Rp'          # set of reclaimers that service pad p (lista de listas de str)
        'distance_between_stockpiles'   : [], # 'BufDisP'     # buffer distance that must be maintained between adjacent stockpiles on pad p (lista de int)
        'stockpiles_on_time'            : [], # -             # set of stockpiles on pad p at time t (input/output)
        'length_stockpile'              : [], # 'LenS'        # length of stockpile s on a pad (lista de int)
        'time_build_start'              : [], # -             # time at which building of stockpile s starts (the day the first coal movement for s takes place (output)
        'time_rec_finish'               : [], # -             # rime at which reclaiming of stockpile s finishes (output)
        'position_pad'                  : [], # -             # position of stockpile s on its pad (position of the easternmost edge of s) (output)
        'stockpiles'                    : [],  # 'S'           # set of stockpiles (lista de str)

              }

    for k, v in dic_pad.items():
        if k in parameter and k != 'length_stockpile' and k != 'stockpiles':
            dic_pad[k] = parameter[k]
        else:
            for i in parameter['pads']:
                dic_pad[k].append([])

    return dic_pad

#########

def fill_in_dic_stacker_stream(parameter):

    dic_stacker_stream = {
        'instance_name'                 : [], # input         # instance .txt file name
        'stacker_streams'               : [], # 'K'           # set of stacker streams (lista de str)
        'daily_cap_hours_stacker'       : [], # 'CapDurK'     # daily capacity, in terms of working hours, of stacker stream k (lista de int)
        'stockpiles_pad_serviced'       : [], # -             # set of stockpiles located on a pad serviced by stacker stream k (input/output)
        'res_cap_hours_stacker'         : [],
        't_scheduled_stacking'     : [],
        'productivity' : []
                         }

    for k, v in dic_stacker_stream.items():
        if k in parameter:
            dic_stacker_stream[k] = parameter[k]
        else:
            for i in parameter['stacker_streams']:
                dic_stacker_stream[k].append([])

    return dic_stacker_stream

#########

def fill_in_dic_load_point(parameter):

    dic_load_point = {
        'instance_name'                 : [], # input         # instance .txt file name
        'load_points'                   : [], # 'L'           # set of load points (lista de str)
        'least_stockpiles_lp'           : [], # 'Sl'          # set of stockpiles that require at least one coal movement from load point l
        'total_mov_stockpile_lp'        : [], # 'NumMovSL'    # total number of coal movements that must be carried out for stockpile s from load point l (lista de listas de int)
        'tonnage_mov_stockpile_lp'      : [], # 'LodTonSL'    # load (tonnage) of a coal movement for stockpile s from load point l (lista de listas de int)
        'daily_cap_coal_mov_lp'         : [], # 'CapMovL'     # number of coal movements that can be accommodated at load point l in one day (lista de int)
        'daily_cap_tonnage_lp'          : [], # 'CapTonL'     # daily capacity, in terms of tonnage, of load point l (lista de int)
        'n_coalmov_stockpile_time'      : [], # -             # number of coal movements carried out for stockpile s from load point l at time t in TD (output)
        'res_cap_tonnage_l'             : [],
        't_scheduled_coal_movement'     : [],
        'res_cap_coal_mov_lp'           :[]
                     }

    for k, v in dic_load_point.items():
        if k in parameter:
            dic_load_point[k] = parameter[k]
        else:
            for i in parameter['load_points']:
                dic_load_point[k].append([])

    return dic_load_point

#########

def fill_in_dic_reclaimer(parameter):

    dic_reclaimer = {
        'instance_name'                 : [], # input         # instance .txt file name
        'reclaimers'                    : [], # 'R'           # set of reclaimers (lista de str)
        'stockpiles_reclaimed'          : [], # -             # set of stockpiles reclaimed by reclaimer r (input/output)
        'inital_position_reclaimers': [],
        'velocity_reclaimeirs' : [],
        'reclaim_schedule'                      : [],
        'space_of_reclaim_schedule'  : [],
        'final_position_reclaimers': []

    }

    for k, v in dic_reclaimer.items():
        if k in parameter:
            dic_reclaimer[k] = parameter[k]
        else:
            for i in parameter['reclaimers']:
                dic_reclaimer[k].append([])

    return dic_reclaimer

#########

def fill_in_dic_time(parameter):

    dic_time = {
        'instance_name'                 : [], # input         # instance .txt file name
        'times_start_of_day'            : [], # 'TD'          # set of times representing the start of a day (int) - The parameter will be generated in Python
        'n_coalmov_stockpile_lp'        : [], # -             # number of coal movements carried out for stockpile s from load point l at time t in TD (output)
        'stockpiles_on_pad'             : [], # -             # set of stockpiles on pad p at time t (input/output)
        'reclaimers_in_use'             : [], # -             # set of reclaimers in use at time t (input/output-auxiliar-temporario-utilitario)
               }

    for k, v in dic_time.items():
        if k in parameter:
            dic_time[k] = parameter[k]

    return dic_time

########### OUTPUT FUNCTIONS OF SECONDARY DICTIONARIES ###########
# The functions return a file with the data printed linked to keys of the respective dictionary.

def print_dic_ship(parameter):

    os.chdir("..")
    os.chdir("OUTPUT")


    with open(parameter['instance_name'][:-4] + "_DIC_SHIP.out", 'w') as arquivo:
        print("Dic_ship\n", file=arquivo)
        for k,v in parameter.items():
            print(f"{k:<23} {' : '} {v}", file=arquivo)

    return

##########

def print_dic_stockpile(parameter):

    os.chdir("..")
    os.chdir("OUTPUT")

    with open(parameter['instance_name'][:-4] + "_DIC_STOCKPILE.out" , 'w') as arquivo:
        print("Dic_stockpile\n", file=arquivo)
        for k,v in parameter.items():
            print(f"{k:<24} {' : '} {v}", file=arquivo)

    return

##########

def print_dic_berth(parameter):

    os.chdir("..")
    os.chdir("OUTPUT")

    with open(parameter['instance_name'][:-4] + "_DIC_BERTH.out"  , 'w') as arquivo:
        print("Dic_berth\n", file=arquivo)
        for k,v in parameter.items():
            print(f"{k:<15} {' : '} {v}", file=arquivo)

    return

##########

def print_dic_pad(parameter):

    os.chdir("..")
    os.chdir("OUTPUT")

    with open(parameter['instance_name'][:-4] + "_DIC_PAD.out" , 'w') as arquivo:
        print("Dic_pad\n", file=arquivo)
        for k,v in parameter.items():
            print(f"{k:<27} {' : '} {v}", file=arquivo)

    return

##########

def print_dic_stacker_stream(parameter):

    os.chdir("..")
    os.chdir("OUTPUT")

    with open(parameter['instance_name'][:-4] + "_DIC_STACKERS.out", 'w') as arquivo:
        print("Dic_stacker_stream\n", file=arquivo)
        for k,v in parameter.items():
            print(f"{k:<23} {' : '} {v}", file=arquivo)

    return

##########

def print_dic_load_point(parameter):

    os.chdir("..")
    os.chdir("OUTPUT")

    with open(parameter['instance_name'][:-4] + "_DIC_LOADP.out", 'w') as arquivo:
        print("Dic_load_point\n", file=arquivo)
        for k,v in parameter.items():
            print(f"{k:<24} {' : '} {v}", file=arquivo)

    return

##########

def print_dic_reclaimer(parameter):

    os.chdir("..")
    os.chdir("OUTPUT")

    with open(parameter['instance_name'][:-4] + "_DIC_RECLAIMER.out", 'w') as arquivo:
        print("Dic_reclaimer\n", file=arquivo)
        for k,v in parameter.items():
            print(f"{k:<20} {' : '} {v}", file=arquivo)

    return

##########

def print_dic_time(parameter):

    os.chdir("..")
    os.chdir("OUTPUT")

    with open(parameter['instance_name'][:-4] + "_DIC_TIME.out", 'w') as arquivo:
        print("Dic_time\n", file=arquivo)
        for k,v in parameter.items():
            print(f"{k:<22} {' : '} {v}", file=arquivo)

    return

##########

########### PRINT ALL THE INFORMATION OF A SINGLE ENTITY OF A DIC ###########

def print_infos_entity_by_label(dictionary,label):
    list_of_values = list(dictionary.values())
    list_of_keys = list(dictionary.keys())
    list_of_main_labels = list_of_values[1]
    position = 0
    while position < len(list_of_main_labels):
        if label == list_of_main_labels[position]:
            break
        else:
            position += 1

    auxcounting = 0
    while auxcounting < len(list_of_values):
        if not auxcounting == 0:
            if len(list_of_values[auxcounting]) == len(list_of_main_labels):
                print(list_of_keys[auxcounting], " : ", list_of_values[auxcounting][position])
        auxcounting += 1



