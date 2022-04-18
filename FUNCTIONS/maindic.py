import os
import re

def insert_inst_dic(parameter):
    # This function reads the instance input file in
    # "INPUTRUN" and fills, variable by variable,
    # the dic_instance defined in "dictionariesdefinition".

    # # LISTS OF LABELS PARAMETERS - METHOD 1
    # V = []
    # S = []
    # B = []
    # P = []
    # K = []
    # L = []
    # R = []
    #
    # # LIST OF LISTS OF LABELS PARAMETERS - METHOD 2
    # Kp = []
    # Rp = []
    # Sv = []
    # Sl = []
    # Ls = []

    # LIST OF LISTS OF INTS PARAMETERS - METHOD 3
    Kp = []
    Rp = []
    Sv = []
    Sl = []
    Ls = []
    NumMovSL = []
    LodTonSL = []

    # LIST OF INTS PARAMETERS - METHOD 4
    V = []
    S = []
    B = []
    P = []
    K = []
    L = []
    R = []
    nv = []
    NomV = []
    EtaV = []
    BufAtlV = []
    BufDtaV = []
    BufLtdV = []
    LenS = []
    DurRecS = []
    LenP = []
    CapDurK = []
    CapMovL = []
    CapTonL = []
    BufDisP = []
    DurRhh = []
    Prod_Stacker = []

    # UNIQUE INTS PARAMETERS - METHOD 5
    NumMxR = []
    Inf = []

    # EMPTY PARAMETERS
    VL = []
    TD = []
    TL = []

    os.chdir("..")                                            # FUNCTIONS > GRANELTM
    os.chdir("INPUTRUN")                                      # GRANELTM > INPUTRUN

    filekeep = open(parameter, "r")
    contentkeep = filekeep.readlines()
    input = parameter
    filekeep.close()
    maincount = 0
    while maincount < len(contentkeep):
        if contentkeep[maincount].startswith("#"):           # Removing comments from the list
            del (contentkeep[maincount])

        # ######### METHOD 1 ######## V, S, B, P, K, L, R
        #
        # if contentkeep[maincount].startswith("V "):          # Select 'V = 00, 01, 02, 03\n'
        #     mainaux = contentkeep[maincount]                 # Keep 'V = 00, 01, 02, 03\n'
        #     listmainaux = mainaux.split(" = ")               # Split 'V = 00, 01, 02, 03' in a list ['V', '00, 01, 02, 03\n']
        #     Aaux = listmainaux[1]                            # Select '00, 01, 02, 03\n'
        #     Aaux = Aaux[:-1]                                 # Remove \n
        #     V = Aaux.split(", ")                             # Generate a list ['00', '01', '02', '03'] from '00, 01, 02, 03'
        #
        # if contentkeep[maincount].startswith("S "):
        #     mainaux = contentkeep[maincount]
        #     listmainaux = mainaux.split(" = ")
        #     Aaux = listmainaux[1]
        #     Aaux = Aaux[:-1]
        #     S = Aaux.split(", ")
        #
        # if contentkeep[maincount].startswith("B "):
        #     mainaux = contentkeep[maincount]
        #     listmainaux = mainaux.split(" = ")
        #     Aaux = listmainaux[1]
        #     Aaux = Aaux[:-1]
        #     B = Aaux.split(", ")
        #
        # if contentkeep[maincount].startswith("P "):
        #     mainaux = contentkeep[maincount]
        #     listmainaux = mainaux.split(" = ")
        #     Aaux = listmainaux[1]
        #     Aaux = Aaux[:-1]
        #     P = Aaux.split(", ")
        #
        # if contentkeep[maincount].startswith("K "):
        #     mainaux = contentkeep[maincount]
        #     listmainaux = mainaux.split(" = ")
        #     Aaux = listmainaux[1]
        #     Aaux = Aaux[:-1]
        #     K = Aaux.split(", ")
        #
        # if contentkeep[maincount].startswith("L "):
        #     mainaux = contentkeep[maincount]
        #     listmainaux = mainaux.split(" = ")
        #     Aaux = listmainaux[1]
        #     Aaux = Aaux[:-1]
        #     L = Aaux.split(", ")
        #
        # if contentkeep[maincount].startswith("R "):
        #     mainaux = contentkeep[maincount]
        #     listmainaux = mainaux.split(" = ")
        #     Aaux = listmainaux[1]
        #     Aaux = Aaux[:-1]
        #     R = Aaux.split(", ")
        #
        # ######### METHOD 2 ######## Kp, Rp, Sv, Sl, Ls
        #
        # if contentkeep[maincount].startswith("Kp "):
        #     mainaux = contentkeep[maincount]
        #     listmainaux = mainaux.split(" = ")
        #     Aaux = listmainaux[1]
        #     Aaux = Aaux[:-1]
        #     Baux = Aaux.split("; ")
        #     Acount = 0
        #     while Acount < len(Baux):
        #         Caux = (Baux[Acount])
        #         Daux = Caux.split(", ")
        #         Baux[Acount] = Daux
        #         Acount += 1
        #     Kp = Baux
        #
        # if contentkeep[maincount].startswith("Rp "):
        #     mainaux = contentkeep[maincount]
        #     listmainaux = mainaux.split(" = ")
        #     Aaux = listmainaux[1]
        #     Aaux = Aaux[:-1]
        #     Baux = Aaux.split("; ")
        #     Acount = 0
        #     while Acount < len(Baux):
        #         Caux = (Baux[Acount])
        #         Daux = Caux.split(", ")
        #         Baux[Acount] = Daux
        #         Acount += 1
        #     Rp = Baux
        #
        # if contentkeep[maincount].startswith("Sv "):
        #     mainaux = contentkeep[maincount]
        #     listmainaux = mainaux.split(" = ")
        #     Aaux = listmainaux[1]
        #     Aaux = Aaux[:-1]
        #     Baux = Aaux.split("; ")
        #     Acount = 0
        #     while Acount < len(Baux):
        #         Caux = (Baux[Acount])
        #         Daux = Caux.split(", ")
        #         Baux[Acount] = Daux
        #         Acount += 1
        #     Sv = Baux
        #
        # if contentkeep[maincount].startswith("Sl "):
        #     mainaux = contentkeep[maincount]
        #     listmainaux = mainaux.split(" = ")
        #     Aaux = listmainaux[1]
        #     Aaux = Aaux[:-1]
        #     Baux = Aaux.split("; ")
        #     Acount = 0
        #     while Acount < len(Baux):
        #         Caux = (Baux[Acount])
        #         Daux = Caux.split(", ")
        #         Baux[Acount] = Daux
        #         Acount += 1
        #     Sl = Baux
        #
        # if contentkeep[maincount].startswith("Ls "):
        #     mainaux = contentkeep[maincount]
        #     listmainaux = mainaux.split(" = ")
        #     Aaux = listmainaux[1]
        #     Aaux = Aaux[:-1]
        #     Baux = Aaux.split("; ")
        #     Acount = 0
        #     while Acount < len(Baux):
        #         Caux = (Baux[Acount])
        #         Daux = Caux.split(", ")
        #         Baux[Acount] = Daux
        #         Acount += 1
        #     Ls = Baux

        ######### METHOD 3 ######## NumMovSL, LodTonSL

        if contentkeep[maincount].startswith("Kp = "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            Aaux = mainlistaux[1]
            Baux = Aaux.split("; ")
            Acount = 0
            while Acount < len(Baux):
                Caux = (Baux[Acount])
                Daux = Caux.split(", ")
                Baux[Acount] = Daux
                Acount += 1
            for i in range(len(Baux)):
                Kp.append([])
                for j in range(len(Baux[i])):
                    Kp[i].append(0)
                    Kp[i][j] = int(Baux[i][j])

        if contentkeep[maincount].startswith("Rp = "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            Aaux = mainlistaux[1]
            Baux = Aaux.split("; ")
            Acount = 0
            while Acount < len(Baux):
                Caux = (Baux[Acount])
                Daux = Caux.split(", ")
                Baux[Acount] = Daux
                Acount += 1
            for i in range(len(Baux)):
                Rp.append([])
                for j in range(len(Baux[i])):
                    Rp[i].append(0)
                    Rp[i][j] = int(Baux[i][j])

        if contentkeep[maincount].startswith("Sv = "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            Aaux = mainlistaux[1]
            Baux = Aaux.split("; ")
            Acount = 0
            while Acount < len(Baux):
                Caux = (Baux[Acount])
                Daux = Caux.split(", ")
                Baux[Acount] = Daux
                Acount += 1
            for i in range(len(Baux)):
                Sv.append([])
                for j in range(len(Baux[i])):
                    Sv[i].append(0)
                    Sv[i][j] = int(Baux[i][j])

        if contentkeep[maincount].startswith("Sl = "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            Aaux = mainlistaux[1]
            Baux = Aaux.split("; ")
            Acount = 0
            while Acount < len(Baux):
                Caux = (Baux[Acount])
                Daux = Caux.split(", ")
                Baux[Acount] = Daux
                Acount += 1
            for i in range(len(Baux)):
                Sl.append([])
                for j in range(len(Baux[i])):
                    Sl[i].append(0)
                    Sl[i][j] = int(Baux[i][j])

        if contentkeep[maincount].startswith("Ls = "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            Aaux = mainlistaux[1]
            Baux = Aaux.split("; ")
            Acount = 0
            while Acount < len(Baux):
                Caux = (Baux[Acount])
                Daux = Caux.split(", ")
                Baux[Acount] = Daux
                Acount += 1
            for i in range(len(Baux)):
                Ls.append([])
                for j in range(len(Baux[i])):
                    Ls[i].append(0)
                    Ls[i][j] = int(Baux[i][j])

        if contentkeep[maincount].startswith("NumMovSL = "):  # Select 'NumMovSL = 1, 5; 5, 0; 0, 3; 2, 0; 1, 0'
            mainaux = contentkeep[maincount]                  # Keep 'nv = 1, 1, 2, 1\n'
            mainlistaux = mainaux.split(" = ")                # Split 'nv = 1, 1, 2, 1\n' in a list ['nv', '1, 1, 2, 1\n']
            Aaux = mainlistaux[1]                             # Select '1, 1, 2, 1\n'
            Baux = Aaux.split("; ")                           # Split '1, 1, 2, 1\n' in a list ['1', '1', '2', '1\n']
            Acount = 0
            while Acount < len(Baux):
                Caux = (Baux[Acount])
                Daux = Caux.split(", ")
                Baux[Acount] = Daux
                Acount += 1
            for i in range(len(Baux)):
                NumMovSL.append([])
                for j in range(len(Baux[i])):
                    NumMovSL[i].append(0)                    # Fill nv = [] with a quantity of elements "0" representing the quantity of elements in listaux ['1', '1', '2', '1\n']
                    NumMovSL[i][j] = int(Baux[i][j])         # Replace each element of nv for each element of listaux transformed to int

        if contentkeep[maincount].startswith("LodTonSL = "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            Aaux = mainlistaux[1]
            Baux = Aaux.split("; ")
            Acount = 0
            while Acount < len(Baux):
                Caux = (Baux[Acount])
                Daux = Caux.split(", ")
                Baux[Acount] = Daux
                Acount += 1
            for i in range(len(Baux)):
                LodTonSL.append([])
                for j in range(len(Baux[i])):
                    LodTonSL[i].append(0)
                    LodTonSL[i][j] = int(Baux[i][j])

        ######### METHOD 4 ######## nv, NomV, EtaV, BufAtlV, BufDtaV, BufLtdV, LenS, DurRecS, LenP, CapDurK, CapMovL, CapTonL, BufDisP, DurRhh, Prod_Stacker

        if contentkeep[maincount].startswith("V "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                V.append(0)
                V[i] = int(listaux[i])

        if contentkeep[maincount].startswith("S "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                S.append(0)
                S[i] = int(listaux[i])

        if contentkeep[maincount].startswith("B "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                B.append(0)
                B[i] = int(listaux[i])

        if contentkeep[maincount].startswith("P "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                P.append(0)
                P[i] = int(listaux[i])

        if contentkeep[maincount].startswith("K "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                K.append(0)
                K[i] = int(listaux[i])

        if contentkeep[maincount].startswith("L "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                L.append(0)
                L[i] = int(listaux[i])

        if contentkeep[maincount].startswith("R "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                R.append(0)
                R[i] = int(listaux[i])

        if contentkeep[maincount].startswith("nv "):        # Select 'nv = 1, 1, 2, 1\n'
            mainaux = contentkeep[maincount]                # Keep 'nv = 1, 1, 2, 1\n'
            mainlistaux = mainaux.split(" = ")              # Split 'nv = 1, 1, 2, 1\n' in a list ['nv', '1, 1, 2, 1\n']
            aux = mainlistaux[1]                            # Select '1, 1, 2, 1\n'
            listaux = aux.split(", ")                       # Split '1, 1, 2, 1\n' in a list ['1', '1', '2', '1\n']
            for i in range(len(listaux)):
                nv.append(0)                                # Fill nv = [] with a quantity of elements "0" representing the quantity of elements in listaux ['1', '1', '2', '1\n']
                nv[i] = int(listaux[i])                     # Replace each element of nv for each element of listaux transformed to int

        if contentkeep[maincount].startswith("NomV "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                NomV.append(0)
                NomV[i] = int(listaux[i])

        if contentkeep[maincount].startswith("EtaV "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                EtaV.append(0)
                EtaV[i] = int(listaux[i])

        if contentkeep[maincount].startswith("BufAtlV "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                BufAtlV.append(0)
                BufAtlV[i] = int(listaux[i])

        if contentkeep[maincount].startswith("BufDtaV "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                BufDtaV.append(0)
                BufDtaV[i] = int(listaux[i])

        if contentkeep[maincount].startswith("BufLtdV "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                BufLtdV.append(0)
                BufLtdV[i] = int(listaux[i])

        if contentkeep[maincount].startswith("LenS "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                LenS.append(0)
                LenS[i] = int(listaux[i])

        if contentkeep[maincount].startswith("DurRecS "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                DurRecS.append(0)
                DurRecS[i] = int(listaux[i])

        if contentkeep[maincount].startswith("LenP "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                LenP.append(0)
                LenP[i] = int(listaux[i])

        if contentkeep[maincount].startswith("CapDurK "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                CapDurK.append(0)
                CapDurK[i] = int(listaux[i])

        if contentkeep[maincount].startswith("CapMovL "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                CapMovL.append(0)
                CapMovL[i] = int(listaux[i])

        if contentkeep[maincount].startswith("CapTonL "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                CapTonL.append(0)
                CapTonL[i] = int(listaux[i])

        if contentkeep[maincount].startswith("BufDisP "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                BufDisP.append(0)
                BufDisP[i] = int(listaux[i])

        if contentkeep[maincount].startswith("DurRhh "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                DurRhh.append(0)
                DurRhh[i] = int(listaux[i])

        if contentkeep[maincount].startswith("Prod_Stacker "):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" = ")
            aux = mainlistaux[1]
            listaux = aux.split(", ")
            for i in range(len(listaux)):
                Prod_Stacker.append(0)
                Prod_Stacker[i] = int(listaux[i])




        ######### METHOD 5 ######## NumMxR, Inf

        if contentkeep[maincount].startswith("NumMxR "):
            aux = contentkeep[maincount]
            listaux = aux.split(" = ")
            NumMxR = int(listaux[1])

        if contentkeep[maincount].startswith("Inf "):
            aux = contentkeep[maincount]
            listaux = aux.split(" = ")
            Inf = int(listaux[1])

        maincount += 1


    dic_instance = {
        'instance_name'               : input,              # instance .txt file name
        'ships'                       : V,                  # set of ships (lista de str)
        'stockpiles'                  : S,                  # set of stockpiles (lista de str)
        'berths'                      : B,                  # set of berths (lista de str)
        'pads'                        : P,                  # set of pads (lista de str)
        'stacker_streams'             : K,                  # set of stacker streams (lista de str)
        'load_points'                 : L,                  # set of load points (lista de str)
        'reclaimers'                  : R,                  # set of reclaimers (lista de str)

        'stacker_streams_pad'         : Kp,                 # set of stacker streams that service pad p (lista de listas de str)
        'reclaimers_pad'              : Rp,                 # set of reclaimers that service pad p (lista de listas de str)
        'order_stockpiles_ship'       : Sv,                 # set of stockpiles of ship v, given in the order in which they must be reclaimed (lista de listas de str)
        'least_stockpiles_lp'         : Sl,                 # set of stockpiles that require at least one coal movement from load point l
        'least_lp_stockpile'          : Ls,                 # set of load points from which stockpile s requires at least one coal movement


        'total_mov_stockpile_lp'      : NumMovSL,           # total number of coal movements that must be carried out for stockpile s from load point l (lista de listas de int)
        'tonnage_mov_stockpile_lp'    : LodTonSL,           # load (tonnage) of a coal movement for stockpile s from load point l (lista de listas de int)

        'total_stockpiles_ship'       : nv,                 # the number of stockpiles of v (int)
        'nomination_ship'             : NomV,               # nomination time of ship v (lista de int)
        'eta_ship'                    : EtaV,               # estimated time of arrival of ship v (lista de int)
        'time_elapse_arrive_load'     : BufAtlV,            # amount of time that must elapse after ship v arrives at a berth before loading can begin (lista de int)
        'time_elapse_depart_arrive'   : BufDtaV,            # amount of time that must elapse after ship v departs a berth before the next ship can arrive (lista de int)
        'time_elapse_load_depart'     : BufLtdV,            # amount of time that must elapse after ship v has been loaded, before it can depart (lista de int)
        'length_stockpile'            : LenS,               # length of stockpile s on a pad (lista de int)
        'time_reclaim_stockpile'      : DurRecS,            # amount of time it takes to reclaim stockpile s (lista de int)
        'lenght_pad'                  : LenP,               # length of pad p (lista de int)
        'daily_cap_hours_stacker'     : CapDurK,            # daily capacity, in terms of working hours, of stacker stream k (lista de int)
        'productivity' : Prod_Stacker,
        'daily_cap_coal_mov_lp'       : CapMovL,            # number of coal movements that can be accommodated at load point l in one day (lista de int)
        'daily_cap_tonnage_lp'        : CapTonL,            # daily capacity, in terms of tonnage, of load point l (lista de int)
        'distance_between_stockpiles' : BufDisP,            # buffer distance that must be maintained between adjacent stockpiles on pad p (lista de int)
        'time_reclaimer_moves'        : DurRhh,             # amount of time that elapses when reclaimer r moves from position h to position h' (lista de int)

        'maximum_reclaimers_use'      : NumMxR,             # maximum number of reclaimers that can be in use at one time (number of ship loaders) (int)
        'infinite'                    : Inf,                # parameter that represents a very large number, which in this problem can be read as infinite. It will be an auxiliary parameter to generate TD and TL (int) (int)

        'large_ships'                 : VL,                 # set of large ships (lista de str)
        'times_start_of_day'          : TD,                 # set of times representing the start of a day (int) - The parameter will be generated in Python
        'times_large_ship_depart'     : TL,                 # set of times at which a large ship can depart (float) - The parameter will be generated in Python
                    }

    return dic_instance



def print_inst_from_dic(parameter):
    # This function generates an instance output file from the dictionary
    # filled with the data from the respective instance's input file.
    # You can use it to check if the data of the original file.txt is being read correctly.

    os.chdir("..")
    os.chdir("OUTPUT")
    Alist = ['V', 'S', 'B', 'P', 'K', 'L', 'R', 'Kp', 'Rp', 'Sv', 'Sl', 'Ls', 'NumMovSL', 'LodTonSL', 'nv', 'NomV', 'EtaV', 'BufAtlV', 'BufDtaV', 'BufLtdV', 'LenS', 'DurRecS', 'LenP', 'CapDurK', 'CapMovL', 'CapTonL', 'BufDisP', 'DurRhh', 'Prod_Stacker', 'NumMxR', 'Inf', 'VL', 'TD', 'TL']
    Blist = ['ships', 'stockpiles', 'berths', 'pads', 'stacker_streams', 'load_points', 'reclaimers', 'stacker_streams_pad', 'reclaimers_pad', 'order_stockpiles_ship', 'least_stockpiles_lp', 'least_lp_stockpile', 'total_mov_stockpile_lp', 'tonnage_mov_stockpile_lp', 'total_stockpiles_ship', 'nomination_ship', 'eta_ship', 'time_elapse_arrive_load', 'time_elapse_depart_arrive', 'time_elapse_load_depart', 'length_stockpile', 'time_reclaim_stockpile', 'lenght_pad', 'daily_cap_hours_stacker', 'productivity','daily_cap_coal_mov_lp', 'daily_cap_tonnage_lp', 'distance_between_stockpiles', 'time_reclaimer_moves', 'maximum_reclaimers_use', 'infinite', 'large_ships', 'times_start_of_day', 'times_large_ship_depart']
    Clist = []
    Dlist = []
    Elist = []
    with open(parameter['instance_name'][:-4] + ".out", 'w') as arquivo:
        for i in range(len(Alist)):
            Clist.append(0)
            Clist[i] = (parameter[Blist[i]])
            Dlist.append(str(Clist[i]))

            if Dlist[i].startswith('['):
                if Dlist[i] == "[]":
                    Dlist[i] = Dlist[i]
                else:
                    Dlist[i] = Dlist[i][1:-1]
                    if Dlist[i].startswith('['):
                        if Dlist[i] == "[]":
                            Dlist[i] = Dlist[i]
                        else:
                            Dlist[i] = Dlist[i][1:-1]
                            Dlist[i] = re.sub("], \[", "; ", Dlist[i])

            Dlist[i] = re.sub("'","",Dlist[i])
            Elist.append(0)
            Elist[i] = Alist[i] + " = " + Dlist[i] + "\n"

            print(Elist[i], file=arquivo)

    return

def print_dic_instance(parameter):
    # The function return a file with the data printed linked to keys of "dic_instance".

    os.chdir("..")
    os.chdir("OUTPUT")

    with open(parameter['instance_name'][:-4] + "_MAIN_DIC.out", 'w') as arquivo:
        print("Dic_instance\n", file=arquivo)
        for k,v in parameter.items():
            print(f"{k:<27} {' : '} {v}", file=arquivo)

    return

##########