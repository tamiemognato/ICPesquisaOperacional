# import plotnine
# import pandas as pd
# from plotnine import *
#
#
# #data = {'ships': [0, 1, 2, 3], 'berth_assigned': [1, 0, 1, 0], 'arrival_time_berth': [100, 150, 300, 400], 'time_departure': [180, 250, 400, 500]}
# data = {'stockpiles': [0, 1, 2, 3, 4, 5], 'h': [0, 510, 300, 310, 0, 160], 'h+length': [500, 810, 490, 600, 150, 700], 'start': [36, 45, 90, 120, 80, 210], 'finish': [70, 112, 100, 200, 300, 420]}
# #data = {'stockpiles': [0, 1], 'h': [0, 510], 'h+length': [500, 810], 'start': [36, 45], 'finish': [70, 112], 'n_mov':[1,4], 'n_mov_time': [40, 80]}
#
# print(data['stockpiles'])
# print(type(data['stockpiles']))
#
#
# df = pd.DataFrame.from_dict(data, orient= 'index')
# df = df.transpose()
#
# print(df)
#
# graph = (
#     ggplot(data = df)
#
#     #gantt sem cor e rótulo - grafico dos berços
#     #+geom_segment(aes(x = "time_departure", xend = "arrival_time_berth", y = "berth_assigned" , yend = "berth_assigned"), size = 10, show_legend = True)
#     #+geom_label(aes(x ="arrival_time_berth", y = "berth_assigned", label = "ships", size = 5, show_legend = True ))
#
#     #retangulo com linhas
#     #+geom_segment(aes(x = "start", xend = "finish", y = "h" , yend = "h", color = "stockpiles"),  show_legend = True)
#     #+geom_segment(aes(x="start", xend="finish", y="h+length", yend="h+length", color = "stockpiles"), show_legend=True)
#     #+geom_linerange(aes(x='start', ymin = 'h', ymax = 'h+length', color = "stockpiles"))
#     #+geom_linerange(aes(x='finish', ymin = 'h', ymax = 'h+length', color = "stockpiles"))
#
#     #retangulo - stockpile e pad
#     +geom_rect(aes(xmin = "start", xmax = "finish", ymin = "h", ymax = "h+length", fill = "stockpiles"))
#     +labs(title = "PAD 0", x = "Time", y = "Pad occupation")
#     +scale_fill_continuous(guide = guide_legend())
#     +geom_label(aes(label = "stockpiles",  x = "finish", y = "h+length", size = 0.05))
#
#    # #Berço
#    # +geom_segment(aes(x = 'arrival_time_berth', xend = 'time_departure', y = 'berth_assigned', yend = 'berth_assigned', size = 10, color = "ships"), show_legend = True)
#    # +scale_fill_discrete(guide = guide_legend())
#    # #+geom_segment(aes(x = 'start', xend = 'finish', y = 'h+length', yend = 'h+length'), show_legend = True)
#    # +geom_label(aes(x ="arrival_time_berth", y = "berth_assigned", label = "ships", size = 10, show_legend = False ))
#    # #+scale_fill_continuous(guide = guide_legend())
#
# )
#
# print(graph)
#
# print("\nfim")

# lista = [0,1,2]
# lista = lista[1:]
# print(lista)

lista1 = [-1, -1]
lista2 = [(10,20), -1]
a = 15
if lista1 == [-1, 37]:
    print("funciona")

var = a in range(lista2[0][0],lista2[0][1])
print(var)

print('ola ola')

