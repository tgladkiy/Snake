import pandas as pd
import pygame
import os
import shutil
import time
import pickle
import datetime
import snake_matrix as st  # модуль мира змейки, матрица данных о состоянии поля
import snake_ai as pct     # модуль нейросети, расчет весов, выбор направления
import snake_draw as snd   # модуль отрисовки графики и таблиц
import rnd_snakes as rsc   # модуль многопоточной генерации случайных весов
import subprocess          # библиотека для открытия стороннего скрипта - построение графика


# Объект класса содержит данные статистики, веса змей
class Sesion_snake():
    def __init__(self, fams, epochs, time_label, max_best_w=10):
        self.time_label = time_label
        self.max_best_w = max_best_w
        self.epoch_clmns = [i for i in range(0, epochs, 5)]
        if self.epoch_clmns[-1] != epochs:
            self.epoch_clmns.append(epochs)
        fams_rows = [i for i in range(1, fams + 1)]
        self.df_pivot_scores = pd.DataFrame(columns=self.epoch_clmns).reindex(fams_rows).fillna('-')
        self.df_cols = self.df_pivot_scores.columns.values.tolist()

        self.deti_list = []
        self.snake_weights_data = []
        self.snake_top_weights = []          #[ [score, moves, [w_in, w_lay, w_out] ] ,  [score, moves, [w_in, w_lay, w_out] ], ....]
        self.era_snakes_list = []            #[ [mir.score, mir.count_all_moves, family_number, era, [ai.w_in, ai.w_lay, ai.w_out] ] ]
        self.era_scores_list = []
        self.era_weights_list = []
        self.era_moves_list = []
        self.snake_statistics = pd.DataFrame(columns=['ai_format', 'family', 'epoch', 'score', 'moves',
                                    'desk_size', 'sensors', 'lay_1', 'lay_2',
                                    'top_parents_by_epoch', 'first_random_snakes', 'time_label'])

    # функция сортирует данные по змеям, формирует ТОП-лист змей, добавляет данные статистики
    def select_the_best(self, fam, ep, pq):
        self.era_snakes_list.sort(key=lambda i: (-i[0], -i[1]))
        self.era_snakes_list = self.era_snakes_list[:pq]  # отобрали установленное количество лучших родителей

        self.era_weights_list = []
        self.era_scores_list = []
        self.era_moves_list = []

        for i in self.era_snakes_list:
            self.era_weights_list.append(i[4])
            self.era_scores_list.append(i[0])
            self.era_moves_list.append(i[1])
            self.snake_statistics.loc[len(self.snake_statistics.index)] = {'ai_format': str(razmer_pole) + 'x' + str(razmer_pole) + '_' + str(
                            input_layer_quantity) + 'in' + str(neurons_layer_quantity_1) + '_' + str(neurons_layer_quantity_2),
                               'family': i[2],
                               'epoch': i[3],
                               'score': i[0],
                               'moves': i[1],
                               'desk_size': razmer_pole,
                               'sensors': input_layer_quantity,
                               'lay_1': neurons_layer_quantity_1,
                               'lay_2': neurons_layer_quantity_2,
                               'top_parents_by_epoch': parents_quantity,
                               'first_random_snakes': random_snakes_quantity,
                               'time_label': self.time_label}
            self.snake_top_weights.append([i[0], i[1], i[4]])

        self.snake_top_weights.sort(key=lambda i: (-i[0], -i[1]))
        self.snake_top_weights = self.snake_top_weights[:self.max_best_w]
        self.snake_weights_data.append([fam, ep, self.era_weights_list, self.era_scores_list, self.era_moves_list])

    #функция сохранения данных статистики
    def save_game_stat(self):
        file_name = "snake_statistics_" + str(self.time_label) + ".csv"
        try:
            self.snake_statistics.to_csv(file_name, mode='w', index=False)
        except:
            print('Произошла ошибка при записи статистики в файл. Данные не сохранены')

    #функция сохранения данных и весов
    def save_best_weights(self):
        file_name = "snake_best_weights_" + str(self.time_label) + ".bin"
        try:
            with open(file_name, "wb") as file:
                pickle.dump(self.snake_weights_data, file)
        except:
            print("Произошла ошибка при записи весов лучших змей в файл")

    #функция обновления табличных данных на экране
    def update_pivot_scores(self, fam, epoch):
        if epoch in self.df_cols:
            temp_df = (
                self.snake_statistics
                .query('family == @fam and epoch == @epoch and time_label == @self.time_label')
                .sort_values(by='score', ascending=False)
                .head(3)
            )
            self.df_pivot_scores.at[fam, epoch] = temp_df['score'].max()

    #сортирует таблицу данных
    def add_super_family_to_pivot_scores(self, fam):
        if len(self.df_pivot_scores.index.to_list()) > 9:
            self.df_pivot_scores['sum'] = self.df_pivot_scores.sum(axis=1)
            self.df_pivot_scores = self.df_pivot_scores.sort_values(by='sum', ascending=False).head(9).drop(columns=['sum'])
        self.df_pivot_scores = self.df_pivot_scores.reindex(self.df_pivot_scores.index.values.tolist() + [fam]).fillna('-')

    #форматирует данные для таблицы ТОП эпохи
    def df_now(self, fam, epoch, empty=False):
        max_top_lines = 10
        if empty:
            table_top_now = pd.DataFrame({'score': ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                                          'moves': ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']})
        else:
            table_top_now = (
                self.snake_statistics
                .query('time_label == @self.time_label and family == @fam and epoch ==@epoch')
                .sort_values(by=['score','moves'], ascending=[False, True])
                .head(max_top_lines)[['score', 'moves', 'family', 'epoch']]
            )
            table_top_now = table_top_now[['score', 'moves']]

        return table_top_now

    #форматирует данные для таблицы ТОП за все время
    def df_all(self, empty=False):
        max_top_lines = 10
        if empty:
            table_top_all = pd.DataFrame({'score': ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                                          'moves': ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                                          'family': ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                                          'epoch': ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']})
        else:
            table_top_all = (
                self.snake_statistics
                .query('time_label == @time_label')
                .sort_values(by=['score','moves'], ascending=[False, True])
                .head(max_top_lines)[['score', 'moves', 'family', 'epoch']]
            )

        return table_top_all

#проверка нажатия клавиш: анимация, скорость анимации, выход
def check_keypressed():
    global speed_snake
    global show_scr
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_q: exit()
            if i.key == pygame.K_p: show_scr = True
            if i.key == pygame.K_o: show_scr = False
            if i.key == pygame.K_s: speed_snake = speed_snake * 1.5
            if i.key == pygame.K_f: speed_snake = speed_snake / 1.5

#функция включения анимации в нужный момент отбора, для записи видео
def demo_game(best_w):

        for snake_weight in best_w:
            mir.new()
            mir.sensors()
            ai.new_pct()
            ai.get_w(snake_weight[0], snake_weight[1], snake_weight[2])
            snake_is_alive = True
            while snake_is_alive:
                mir.sensors()
                ai.calculation(mir.snake_sensors)
                if mir.move(
                        ai.solution()) == False or mir.count_moves > razmer_pole * razmer_pole:  # Если змейка погибла
                    snake_is_alive = False

                pole.draw(win, mir.arr)
                pole.table_scores(mir.score, mir.count_moves, mir.count_all_moves)
                pygame.display.update(pole.rect_pole)
                time.sleep(speed_snake)  # скорость движения змеки
                check_keypressed()


if __name__ == "__main__":

    """--------------------  Параметры игрового поля, окна и параметров нейросети --------------------------"""

    razmer_pole = 15  # размер игрового поля - "клеток внутри стен"
    razmer_cell = 22  # размер блоков змейки, яблок и стен в pxl
    win_h = 1400      # Ширина экрана
    win_v = 680       # Высота экрана
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (40, 40)  # позиционирование окна приложения, левый верхний угол

    input_layer_quantity = 32      # размер словя сенсоров
    neurons_layer_quantity_1 = 16  # первый скрытый слой
    neurons_layer_quantity_2 = 12  # второй скрытый слой
    otput_layer_quantity = 4       # слой на выходе: ↑ ↓ ← →

    number_of_families = 10         # Количество циклов для отбора новых семейств
    epochs = 100                    # Количество эпох для семьи
    parents_quantity = 15           # Количество родителей из ТОП для скрещивания
    parents_quantity_s_fam = 15     # Количество родителей из ТОП для скрещивания супер-семьи
    random_snakes_quantity = 50000  # Количество рандомных весов для выбора 0-й популяции
    probability_a = 50              # Вероятность взять гены родителя №1
    probability_b = 50              # Вероятность взять гены родителя №2
    probability_mutation = 5        # Вероятность мутации генов в поруляции с мутацией
    probability_mutation_s_fam = 1  # Вероятность мутации генов в поруляции с мутацией супер-семей
    speed_snake = 0.02              # скорость анимации змеек

    time_label = datetime.datetime.today().strftime("%y%m%d_%H%M")  # метка игры  (год месяц день час минута запуска)
    shutil.copy('snake_plot_clean.png', 'snake_plot.png')

    df_base = pd.DataFrame(columns=['ai_format', 'family', 'epoch', 'score', 'moves',
                                    'desk_size', 'sensors', 'lay_1', 'lay_2',
                                    'top_parents_by_epoch', 'first_random_snakes', 'time_label'])
    df_stat = df_base.copy()

    pygame.init()
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((win_h, win_v))   # Ширина и высота поля в pix
    pygame.display.set_caption("Snake")             # Заголовок окна
    font_name = pygame.font.match_font('calibri')   # Шрифт заголовка окна
    text_undthl = "Hot keys:       Animation on/off:  O / P         Snakes speed:   S / F            Quit game:  Q"

    """-----------------------------------------------------------------------------------------------------"""
    # Инициализация модулей
    mir = st.Mir(razmer_pole)
    pole = snd.Pole(razmer_pole, razmer_cell, win_h, win_v)
    ai = pct.Perceptron(input_layer_quantity, neurons_layer_quantity_1, neurons_layer_quantity_2, otput_layer_quantity)
    ses = Sesion_snake(number_of_families, epochs, time_label)

    mir.new()
    mir.sensors()
    ai.new_pct()
    pole.draw(win, mir.arr)

    pole.param_table(time_label, razmer_pole, input_layer_quantity, neurons_layer_quantity_1,
                     neurons_layer_quantity_2, number_of_families, epochs, random_snakes_quantity)

    pole.pivot_score(ses.df_pivot_scores)
    pole.now_top(ses.df_now(0,0, empty=True),0,0, random_snakes_quantity)
    pole.top_table(ses.df_all(empty=True))
    pole.draw_status("Generating weights for the zero population: " + str(random_snakes_quantity) + " snakes х " + str(number_of_families) + " families" )
    pole.show_plot()
    pygame.display.update()

    rs = rsc.Random_snakes_class(razmer_pole, random_snakes_quantity, number_of_families, parents_quantity*3,
                                 input_layer_quantity, neurons_layer_quantity_1, neurons_layer_quantity_2,
                                 otput_layer_quantity,
                                 time_label)

    #Запуск цикла отбора нулевой популяции в многопоточном режиме
    rs_dict = rs.give_me_random_snakes()
    rs_dict_keys = sorted(rs_dict.keys())           #ответ в виде словаря списков


    """--------------------------    Цикл игр семейств    ---------------------------------------------------"""
    first_time_flag = True
    for family_number in rs_dict_keys:              # цикл семейств

        ses.snake_statistics = pd.concat([ses.snake_statistics, rs_dict[family_number][1]], axis=0)
        ses.deti_list = ai.w_suffle(rs_dict[family_number][0], probability_a, probability_b, probability_mutation)

        show_scr = False

        # форматируем данные и выводим их на экран
        pole.draw(win, mir.arr)
        pole.param_table(time_label, razmer_pole, input_layer_quantity, neurons_layer_quantity_1,
                         neurons_layer_quantity_2, number_of_families, epochs, random_snakes_quantity)
        ses.update_pivot_scores(family_number, 0)
        pole.pivot_score(ses.df_pivot_scores)
        pole.now_top(ses.df_now(0,0, empty=True), family_number, 0, len(ses.deti_list))
        pole.top_table(ses.df_all())
        pole.draw_status(text_undthl)
        pole.show_plot()
        pygame.display.update()

        for era in range(1, epochs+1):              # цикл эпох в семействе

            ses.era_snakes_list = []
            for snake_weight in ses.deti_list:      # цикл игр змеек в эпохе
                mir.new()
                mir.sensors()
                ai.new_pct()
                ai.get_w(snake_weight[0], snake_weight[1], snake_weight[2])
                snake_is_alive = True
                while snake_is_alive:               # цикл игры одной змейки
                    mir.sensors()
                    ai.calculation(mir.snake_sensors)
                    if mir.move(ai.solution()) == False or mir.count_moves > razmer_pole*razmer_pole:  # Если змейка погибла
                        snake_is_alive = False
                        ses.era_snakes_list.append([mir.score,                                         # Сохранили параметры
                                                    mir.count_all_moves,
                                                    family_number, era,
                                                    [ai.w_in, ai.w_lay, ai.w_out]])


                    if show_scr == True:            # проверка, включили ли мы отображение движений змейки
                        pole.draw(win, mir.arr)
                        pole.table_scores(mir.score, mir.count_moves, mir.count_all_moves)
                        pygame.display.update(pole.rect_pole)
                        time.sleep(speed_snake)     # скорость движения змеки
                    check_keypressed()

            # отбор лучших:
            ses.select_the_best(family_number, era, parents_quantity)
            # формирования списка после скрещивания:
            ses.deti_list = ai.w_suffle(ses.era_weights_list, probability_a, probability_b, probability_mutation)

            # обновление статистических данных на экране
            pole.now_top(ses.df_now(family_number, era),family_number, era, len(ses.deti_list))
            pole.top_table(ses.df_all())
            if era in ses.df_cols: ses.update_pivot_scores(family_number, era)
            pole.pivot_score(ses.df_pivot_scores)
            pole.param_table(time_label, razmer_pole, input_layer_quantity, neurons_layer_quantity_1,
                             neurons_layer_quantity_2, number_of_families, epochs, random_snakes_quantity)
            pole.draw_status(text_undthl)
            pole.show_plot()
            pygame.display.update()

            ses.save_best_weights()

        #demo_game(ses.era_weights_list)  # визуализация игр лучших в эпохе, для видео

        ses.save_game_stat()

        # запуск стороннего скрипта для обновления графика (из-за конфликта matplotlib и pygame в одном "окне")
        subprocess.call(['python.exe', 'plot_to_img.py', str(time_label)])
        first_time_flag = False


    family_number = 900

    # формирование списка змей из лучших змей для скрещивания
    weights_to_deti_list = []
    for i in ses.snake_weights_data:
        if i[1] == epochs:
            for k in i[2]:
                weights_to_deti_list.append(k)

    for i in ses.snake_top_weights:
        weights_to_deti_list.append(i[2])

    ses.deti_list = ai.w_suffle(weights_to_deti_list, probability_a, probability_b, probability_mutation)


    """--------------------------    Цикл игр супер - семейств  ---------------------------------------------------"""

    parents_quantity = parents_quantity_s_fam               #Если решили поменять тактику отбора по количеству ТОП
    probability_mutation = probability_mutation_s_fam       #Если решили поменять тактику отбора по % мутации

    while True:             # отбор длится пока не закрыто окно или нажата кнопка "q"

        ses.add_super_family_to_pivot_scores(family_number)
        pole.now_top(ses.df_now(family_number, 0), family_number, 0, len(ses.deti_list))
        pole.top_table(ses.df_all())
        pole.pivot_score(ses.df_pivot_scores)
        pole.param_table(time_label, razmer_pole, input_layer_quantity, neurons_layer_quantity_1,
                         neurons_layer_quantity_2, number_of_families, epochs, random_snakes_quantity)
        pole.draw_status(text_undthl)
        pole.show_plot()
        pygame.display.update()


        show_scr = False

        for era in range(0, epochs+1):
            ses.era_snakes_list = []
            for snake_weight in ses.deti_list:
                mir.new()
                mir.sensors()
                ai.new_pct()
                ai.get_w(snake_weight[0], snake_weight[1], snake_weight[2])
                snake_is_alive = True
                while snake_is_alive:
                    mir.sensors()
                    ai.calculation(mir.snake_sensors)
                    if mir.move(ai.solution()) == False or mir.count_moves > razmer_pole*razmer_pole:  # Если змейка погибла
                        snake_is_alive = False
                        ses.era_snakes_list.append([mir.score,                    # Сохранили параметры
                                                    mir.count_all_moves,
                                                    family_number, era,
                                                    [ai.w_in, ai.w_lay, ai.w_out]])


                    if show_scr == True:
                        pole.draw(win, mir.arr)
                        pole.table_scores(mir.score, mir.count_moves, mir.count_all_moves)
                        pygame.display.update(pole.rect_pole)
                        time.sleep(speed_snake)

                    check_keypressed()

            ses.select_the_best(family_number, era, parents_quantity)
            ses.save_best_weights()

            weights_to_deti_list = []
            for i in ses.snake_top_weights:
                weights_to_deti_list.append(i[2])

            ses.deti_list = ai.w_suffle_superfam(weights_to_deti_list + ses.era_weights_list, probability_a,
                                                 probability_b, probability_mutation)


            pole.now_top(ses.df_now(family_number, era), family_number, era, len(ses.deti_list))
            pole.top_table(ses.df_all())
            if era in ses.df_cols: ses.update_pivot_scores(family_number, era)
            pole.pivot_score(ses.df_pivot_scores)
            pole.param_table(time_label, razmer_pole, input_layer_quantity, neurons_layer_quantity_1,
                             neurons_layer_quantity_2, number_of_families, epochs, random_snakes_quantity)
            pole.draw_status(text_undthl)
            pole.show_plot()
            pygame.display.update()

        #demo_game(ses.era_weights_list)  # демо игры

        ses.save_game_stat()
        subprocess.call(['python.exe', 'plot_to_img.py', str(time_label)])

        family_number += 1


    pygame.quit()