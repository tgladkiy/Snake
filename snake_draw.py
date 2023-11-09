import pygame

"""Модуль отрисовки окна с игровым полем и данными статистики"""


class Pole:

    def __init__(self, size, cell, win_h, win_v):
        """Задаем длину и ширину поля"""
        self.size = size
        self.cell = cell
        self.win_h = win_h
        self.win_v = win_v
        self.otstup = 10
        self.otstup_block = 10
        self.pole_size = self.cell*2 + self.size*self.cell

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 128, 0)
        self.GREY = (36,36,36)
        self.L_WHITE = (100,100,100)
        self.text_font = pygame.font.SysFont("Arial", 19)
        self.text_font_sm = pygame.font.SysFont("Arial", 16)
        self.text_font_smm = pygame.font.SysFont("Arial", 14)
        self.text_col = (255, 255, 255)
        self.text_col_yellow = (250, 249, 170)
        self.img_stat = pygame.image.load('snake_plot_clean.png')

    # отрисовка игрового поля
    def draw(self, window, arr):
        self.window = window
        self.window.fill(self.BLACK)
        frame_color = self.WHITE
        self.rect_pole = pygame.Rect((0,0,
                                     self.pole_size + self.otstup_block,
                                     self.pole_size + 50))

        pygame.draw.rect(self.window, frame_color, (self.otstup,                                      #рисуем рамку поля, она покрывает значения стен матрицы
                                               self.otstup,
                                               self.pole_size,
                                               self.pole_size), self.cell-1)

        block_color = self.BLACK

        for i in range(1, len(arr)-1):
            for j in range(1, len(arr)-1):
                if arr[i,j] != 11:   #поменять на 0 ести нужно отключить сетку поля
                    if arr[i,j] == 1: block_color = self.WHITE
                    if arr[i,j] == 7: block_color = self.RED
                    if arr[i,j] == 2: block_color = self.GREEN
                    if arr[i,j] == 0: block_color = self.GREY
                    x_pos = self.otstup + self.cell*(j)
                    y_pos = self.otstup + self.cell*(i)
                    pygame.draw.rect(self.window, block_color, (x_pos, y_pos, self.cell-1, self.cell-1))

    # отрисовка таблицы ТОП эпохи
    def now_top(self, df_now, fam, epoch, population=200):
        x= self.win_h - self.otstup - 790 - 160 - self.otstup_block
        y= self.otstup
        surf_actual_top = pygame.Surface((160, 300))
        surf_actual_top.fill(self.GREY)
        pygame.draw.line(surf_actual_top, self.L_WHITE, [5, 30], [155, 30])
        pygame.draw.line(surf_actual_top, self.L_WHITE, [5, 270], [155, 270])
        self.window.blit(surf_actual_top, (x, y))
        txt_head = "Family: " + str(fam) + "   Epoch: " + str(epoch)
        self.window.blit(self.text_font_sm.render(txt_head, True, self.text_col), (x + 10, y + 10))

        otstup_y = 35
        dy = 20
        dict = df_now.to_dict('list')

        self.window.blit(self.text_font_sm.render("Score", True, self.text_col), (x + 10, y + otstup_y))
        self.window.blit(self.text_font_sm.render("Moves", True, self.text_col), (x + 90, y + otstup_y))


        for i in range(0, len(dict[list(dict.keys())[0]])):
            self.window.blit(self.text_font_sm.render(str(dict['score'][i]), True, self.text_col), (x + 20 , y + 10 + otstup_y + dy))
            self.window.blit(self.text_font_sm.render(str(dict['moves'][i]), True, self.text_col), (x + 100, y + 10 + otstup_y + dy))

            y += dy


        self.window.blit(self.text_font_sm.render(str("Population:  " + str(population)), True, self.text_col),
                         (x + 10, 285))

    # отрисовка таблицы данных по семьям и эпохам
    def pivot_score(self, df):
        x= self.win_h - self.otstup - 790
        y= self.otstup
        otstup_x = 35
        otstup_y = 26
        surf_pivot_score = pygame.Surface((790, 300))
        surf_pivot_score.fill(self.GREY)
        pygame.draw.line(surf_pivot_score, self.L_WHITE, [5, 29], [845, 29])
        pygame.draw.line(surf_pivot_score, self.L_WHITE, [37, 5], [37, 295])
        self.window.blit(surf_pivot_score, (x, y))




        dx = otstup_x
        for i in df.columns.values.tolist():
            self.window.blit(self.text_font_smm.render(str(i), True, self.text_col),
                             (x + 15 + dx, y + 10))
            dx += otstup_x

        dy = otstup_y
        for i in df.index.tolist():
            self.window.blit(self.text_font_smm.render(str(i), True, self.text_col),
                             (x + 10, y + 10 + dy))
            dy += otstup_y

        dy = 0
        for ind in df.index.tolist():
            dx = 0
            for clm in df.columns.values.tolist():
                self.window.blit(self.text_font_smm.render(str(df.loc[ind][clm]), True, self.text_col),
                                 (x + 15 + otstup_x + dx, y + 10 + otstup_y + dy))
                dx += otstup_x
            dy += otstup_y

    # отображение графика
    def show_plot(self):
        self.img_stat = pygame.image.load('snake_plot.png')

        x= self.win_h - self.otstup - 700
        y= self.otstup + 300 + self.otstup_block
        self.window.blit(self.img_stat, (x, y))

    # отрисовка данных таблицы результатов по семьям и эпохам
    def table_scores(self, score, count_moves, count_all_moves):
        x = self.otstup + self.cell
        y = self.pole_size + 15
        dy = 25
        table_font = pygame.font.SysFont("Arial", 18)

        text = 'Score:  ' + str(score) + '       Moves:  ' + str(count_all_moves)
        img = table_font.render(text, True, self.text_col)
        self.rect_scores = img.get_rect()
        self.window.blit(img, (x,y))

    # отрисовка таблицы параметров игры
    def param_table(self, tl, rp, sens, sl1, sl2, fam, ep, pop):
        x= self.otstup
        y= self.otstup + 420
        surf_param_table = pygame.Surface((410, 200))
        self.rect_param_table = surf_param_table.get_rect()
        surf_param_table.fill(self.GREY)
        pygame.draw.line(surf_param_table, self.L_WHITE, [5, 32], [405, 32])
        self.window.blit(surf_param_table, (x, y))
        dy = 22
        dx = 200
        self.window.blit(self.text_font_sm.render("Game №:", True, self.text_col), (x+10, y+10))
        self.window.blit(self.text_font_sm.render(str(tl), True, self.text_col), (x+10+dx, y+10))

        self.window.blit(self.text_font_sm.render("Board size:", True, self.text_col), (x+10, y+15+1*dy))
        self.window.blit(self.text_font_sm.render(str(str(rp)+'x'+str(rp)), True, self.text_col), (x+10+dx, y+15+1*dy))
        self.window.blit(self.text_font_sm.render("Sensors:", True, self.text_col), (x+10, y+15+2*dy))
        self.window.blit(self.text_font_sm.render(str(sens), True, self.text_col), (x+10+dx, y+15+2*dy))
        self.window.blit(self.text_font_sm.render("Hidden layer №1:", True, self.text_col), (x+10, y+15+3*dy))
        self.window.blit(self.text_font_sm.render(str(sl1), True, self.text_col), (x+10+dx, y+15+3*dy))
        self.window.blit(self.text_font_sm.render("Hidden layer №2:", True, self.text_col), (x+10, y+15+4*dy))
        self.window.blit(self.text_font_sm.render(str(sl2), True, self.text_col), (x+10+dx, y+15+4*dy))
        self.window.blit(self.text_font_sm.render("Families:", True, self.text_col), (x+10, y+15+5*dy))
        self.window.blit(self.text_font_sm.render(str(fam), True, self.text_col), (x+10+dx, y+15+5*dy))
        self.window.blit(self.text_font_sm.render("Epochs: ", True, self.text_col), (x+10, y+15+6*dy))
        self.window.blit(self.text_font_sm.render(str(ep), True, self.text_col), (x+10+dx, y+15+6*dy))
        self.window.blit(self.text_font_sm.render("Zero population:", True, self.text_col), (x+10, y+15+7*dy))
        self.window.blit(self.text_font_sm.render(str(pop), True, self.text_col), (x+10+dx, y+15+7*dy))


    # отрисовка таблицы ТОП за все время
    def top_table(self, df_all):
        x= self.win_h - 700 - self.otstup_block - 250 - self.otstup
        y= self.otstup + 300 + self.otstup_block - 1
        surf_top_table = pygame.Surface((250, 310))
        surf_top_table.fill(self.GREY)
        pygame.draw.line(surf_top_table, self.L_WHITE, [5, 30], [245, 30], 1)
        self.window.blit(surf_top_table, (x, y))
        self.window.blit(self.text_font_sm.render("TOP score table:", True, self.text_col), (x+self.otstup, y+self.otstup))

        otstup_y = 30
        dy = 23
        dict = df_all.to_dict('list')

        self.window.blit(self.text_font_sm.render("Score", True, self.text_col), (x + 10, y + 35))
        self.window.blit(self.text_font_sm.render("Moves", True, self.text_col), (x + 70, y + 35))
        self.window.blit(self.text_font_sm.render("Family", True, self.text_col), (x + 135, y + 35))
        self.window.blit(self.text_font_sm.render("Epoch", True, self.text_col), (x + 195, y + 35))

        for i in range(0, len(dict[list(dict.keys())[0]])):
            self.window.blit(self.text_font_sm.render(str(dict['score'][i]), True, self.text_col), (x + 15 , y + 10 + otstup_y + dy))
            self.window.blit(self.text_font_sm.render(str(dict['moves'][i]), True, self.text_col), (x + 75, y + 10 + otstup_y + dy))
            self.window.blit(self.text_font_sm.render(str(dict['family'][i]), True, self.text_col), (x + 150, y + 10 + otstup_y + dy))
            self.window.blit(self.text_font_sm.render(str(dict['epoch'][i]), True, self.text_col), (x + 210, y + 10 + otstup_y + dy))
            y += dy


    # отрисовка строки статуса и информации о горячих клавишах
    def draw_status(self, text=""):
        x= self.otstup
        y= self.win_v - self.otstup - 30
        surf_status = pygame.Surface((670, 30))
        surf_status.fill(self.GREY)
        self.window.blit(surf_status, (x, y))

        img = self.text_font_sm.render(text, True, self.text_col_yellow)
        self.window.blit(img, (x+10, y+5))




