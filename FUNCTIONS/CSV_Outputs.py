import csv


def generate_csv_outputs(parameter,dic_instance, dic_ship, dic_berth, dic_stockpile, dic_pad, dic_load_point, dic_stacker_stream, dic_reclaimer):

    with open(parameter['instance_name'][:-4] + "_CSV.out", 'w') as file:
        writer = csv.writer(file)


    return