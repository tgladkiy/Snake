import snake_ai as pct
import snake_matrix as st
import pandas as pd
import multiprocessing as mp


""" Модуль для генерации и отбора лучших зней в каждое семейство 
    Получает на вход данные 
    - об игровом мире 
    - параметрах нейросети
    - количество семей, ТОП отбора и т.д.  
    - временную метку расчета 
    
    На выходе словарь. Ключ - семейсто, данные  - список с вложениями: веса, результаты ТОП змеек """



class Random_snakes_class():
    def __init__(self, razmer_pole, random_snakes_quantity, number_of_families, parents_quantity,
                 input_layer_quantity, neurons_layer_quantity_1, neurons_layer_quantity_2, otput_layer_quantity,time_label):
        self.razmer_pole = razmer_pole
        self.random_snakes_quantity = random_snakes_quantity
        self.number_of_families = number_of_families
        self.parents_quantity = parents_quantity
        self.input_layer_quantity = input_layer_quantity
        self.neurons_layer_quantity_1 = neurons_layer_quantity_1
        self.neurons_layer_quantity_2 = neurons_layer_quantity_2
        self.otput_layer_quantity = otput_layer_quantity
        self.time_label = time_label
        self.df_family = pd.DataFrame(columns=['ai_format', 'family', 'epoch', 'score', 'moves',
                                           'desk_size', 'sensors', 'lay_1', 'lay_2',
                                           'top_parents_by_epoch', 'first_random_snakes', 'time_label'])


    # создаёт несколько потоков по количеству семей
    def give_me_random_snakes(self):
        self.mir = st.Mir(self.razmer_pole)
        self.ai = pct.Perceptron( self.input_layer_quantity, self.neurons_layer_quantity_1, self.neurons_layer_quantity_2,
                            self.otput_layer_quantity)

        self.mir.new()
        self.mir.sensors()
        self.ai.new_pct()

        manager = mp.Manager()
        return_dict = manager.dict()

        #i_family = mp.cpu_count()
        potoks = []
        for i_family in range(1, self.number_of_families+1):
            p = mp.Process(target=self.random_snakes, args=(i_family, return_dict))
            p.start()
            potoks.append(p)

        for potok in potoks:
            potok.join()

        return return_dict

    # проводит игры змеек со случайными весами и отбирает лучших
    def random_snakes(self, fam_num, return_dict): #

        def top_list(tl):  # функция отбирает данные по змеям и отдает на выход список весов ТОПа
            tl.sort(key=lambda i: i[0], reverse=True)
            tl_top = tl[:self.parents_quantity]  # отобрали установленное количество лучших родителей
            top_wghts = []
            top_scores = []

            for i in tl_top:
                top_wghts.append(i[4])
                self.df_family.loc[len(self.df_family.index)] = {'ai_format': str(self.razmer_pole) + 'x' + str(self.razmer_pole) + '_' + str(
                    self.input_layer_quantity) + 'in' + str(self.neurons_layer_quantity_1) + '_' + str(self.neurons_layer_quantity_2),
                                   'family': fam_num,
                                   'epoch': i[3],
                                   'score': i[0],
                                   'moves': i[1],
                                   'desk_size': self.razmer_pole,
                                   'sensors': self.input_layer_quantity,
                                   'lay_1': self.neurons_layer_quantity_1,
                                   'lay_2': self.neurons_layer_quantity_2,
                                   'top_parents_by_epoch': self.parents_quantity,
                                   'first_random_snakes': self.random_snakes_quantity, #random_snakes_quantity
                                   'time_label': self.time_label}

            return top_wghts, self.df_family  # выводим в консоль топ результатов и на выход функции - список из весов топ 15

        n_snake = 0
        rnd_snakes_list = []
        self.ai.rand_w()                                 #задали случайные веса для первой змеи
        while n_snake <= self.random_snakes_quantity:
            self.mir.sensors()
            self.ai.calculation(self.mir.snake_sensors)
            if self.mir.move(self.ai.solution()) == False or self.mir.count_moves > 100:    #Если змейка погибла
                rnd_snakes_list.append([self.mir.score,                                     #Сохранили параметры
                                           self.mir.count_all_moves,
                                           fam_num, 0,
                                           [self.ai.w_in, self.ai.w_lay, self.ai.w_out]])
                self.ai.new_pct()
                self.ai.rand_w()
                self.mir.new()
                n_snake += 1

        return_list = top_list(rnd_snakes_list)
        return_dict[fam_num] = return_list

