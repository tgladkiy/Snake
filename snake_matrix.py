import random
import numpy

"""Модуль матрицы мира змейки
   Массив содержит данные о клетках в игровом поле:  стена = 4,  тело = 1, пустота = 0, голова = 7, еда = 2
   
   - генерирует яблоко
   - рассчитывает значение сенсоров
   - осуществляет следующий и анализирует его последствия
   """

class Mir:

    def __init__(self, size):
        self.size = size + 2
        self.arr = numpy.zeros((self.size, self.size), dtype=int)
        for k in range (0, self.size):
            self.arr[k,0], self.arr[k,self.size-1], self.arr[0,k], self.arr[self.size-1, k]= 4,4,4,4
        self.score = 0                  # очки за игру
        self.count_moves = 0            # количество ходов на 1 явлоко
        self.count_all_moves = 0        # количество ходов на 1 явлоко
        self.snake_sensors = []
        self.sens_lib = {}
        self.head =[]
        self.tail =[]
        self.life = True                # змейка жива = True

    # генерация яблока
    def eat(self):
        self.count_moves = 0            # количество ходов на 1 явлоко
        flag = True
        while flag:
            i = random.randint(0, self.size-1)
            j = random.randint(0, self.size-1)
            if self.arr[i, j] == 0:
                self.apple_pos = [i,j]
                self.arr[i, j] = 2
                flag = False

    # обновление мира
    def new(self):
        self.life = True
        self.score = 0
        self.count_all_moves = 0
        self.arr = numpy.zeros((self.size, self.size), dtype=int)
        for k in range (0, self.size):
            self.arr[k,0], self.arr[k,self.size-1], self.arr[0,k], self.arr[self.size-1, k]= 4,4,4,4
        self.arr[self.size//2-1, self.size//2] = 7
        self.arr[self.size//2, self.size//2] = 1

        self.tail = []
        self.tail.append([self.size//2-1, self.size//2])
        self.tail.append([self.size//2, self.size//2])
        self.eat()

    # делает ход, согласно предсказанию и возвращает состояние змейки
    def move(self, way):

        """Маска значений: список из 0 и 1 - [up,down,left,right].  """
        new_i = self.tail[0][0]-way[0]+way[1]
        new_j = self.tail[0][1]-way[2]+way[3]

        self.count_moves += 1               # змейка сделала ход
        self.count_all_moves += 1           # счетчик всех ходов

        if self.arr[new_i,new_j] == 4 or self.arr[new_i,new_j] ==1 :    # если шаг головы упирается в стену или в хвост
            self.life = False   # змейка погибла

        else:
            self.arr[new_i,new_j] = 7                           # новое валидное поле становится головой
            self.arr[self.tail[0][0],self.tail[0][1]] = 1       # поле головы становится хвостом
            self.tail.insert(0,[new_i,new_j])

            if [new_i,new_j] == self.apple_pos:                 # змейка съела яблоко
                self.score += 1
                self.eat()
            else:
                self.arr[self.tail[-1][0],self.tail[-1][1]] = 0     # последнее поле хвоста становится пустым
                self.tail.pop()

            self.sensors()

        return self.life

    # расчет значений сенсоров
    def sensors(self):
        """Координаты [i,j]  -  i- вертикаль,  j- горизонтать,  [0,0] - левый верхний угол:
        Сенсоры змейки:
        1. Расстояние по прямой до стен - 4 шт
        2. Расстояние по прямой до яблока - 4 шт
        3. Расстояние по прямой до хвоста - 4 шт
        4. Сектор где яблоко: ниже/выше/слева/справо - 4 шт, значения 0/1
        5. Расстояние по диагонали до стен, еды, хвоста - 12 шт
        6. Расстояние от головы до яблока, рассчет по гипотенузе"""

        """ Введем переменные для координат объектов"""
        i, j = self.tail[0][0], self.tail[0][1]      # координаты головы
        i_apl = self.apple_pos[0]                    # координаты еды
        j_apl = self.apple_pos[1]

        """ 1. Сенсоры голова - стены, по вертикали и горизонтали - 4 шт """
        sens_up, sens_down, sens_left,sens_right = 0,0,0,0
        """ 2. Сенсоры голова-яблоко и голова-хвост по вертикали и горизонтали  2x4 шт """
        sens_apl_up, sens_apl_down, sens_apl_left, sens_apl_right = 0,0,0,0
        sens_tail_up, sens_tail_down, sens_tail_left, sens_tail_right = 0,0,0,0

        k = 1
        for iter_i in range (i, 0, -1):
            if self.arr[iter_i-1,j] == 2:
                sens_apl_up = k
                break
            if self.arr[iter_i-1,j] == 1:
                sens_tail_up = k
                break
            if self.arr[iter_i-1,j] == 4:
                sens_up = k
                break
            k = k + 1

        k = 1
        for iter_i in range (i, self.size-1):
            if self.arr[iter_i+1,j] == 2:
                sens_apl_down = k
                break
            if self.arr[iter_i+1,j] == 1:
                sens_tail_down = k
                break
            if self.arr[iter_i+1,j] == 4:
                sens_down = k
                break
            k = k+1

        k = 1
        for iter_j in range (j, 0, -1):
            if self.arr[i, iter_j-1] == 2:
                sens_apl_left = k
                break
            if self.arr[i, iter_j-1] == 1:
                sens_tail_left = k
                break
            if self.arr[i, iter_j-1] == 4:
                sens_left = k
                break
            k = k+1

        k = 1
        for iter_j in range (j, self.size-1):
            if self.arr[i, iter_j+1] == 2:
                sens_apl_right = k
                break
            if self.arr[i, iter_j+1] == 1:
                sens_tail_right = k
                break
            if self.arr[i, iter_j+1] == 4:
                sens_right = k
                break
            k = k+1

        """ 3. Сенсоры сектора в котором яблоко 4 шт """
        sens_sekt_up, sens_sekt_down, sens_sekt_left, sens_sekt_right = 0,0,0,0
        if i_apl < i : sens_sekt_up = 1
        if i_apl > i : sens_sekt_down = 1
        if j_apl < j : sens_sekt_left = 1
        if j_apl > j : sens_sekt_right = 1

        """ 4. Сенсоры растояния до яблока по направлению, гипотенуза 4 шт """
        sens_apl_up_left, sens_apl_up_right, sens_apl_down_left, sens_apl_down_right = 0,0,0,0
        if i_apl < i and j_apl < j :  sens_apl_up_left = ((i-i_apl)**2 + (j - j_apl)**2 ) ** (0.5)
        if i_apl > i and j_apl < j :  sens_apl_down_left = ((i-i_apl)**2 + (j - j_apl)**2 ) ** (0.5)
        if i_apl < i and j_apl > j :  sens_apl_up_right = ((i-i_apl)**2 + (j - j_apl)**2 ) ** (0.5)
        if i_apl > i and j_apl > j :  sens_apl_down_right = ((i-i_apl)**2 + (j - j_apl)**2 ) ** (0.5)

        """ 4. Сенсоры до объектов по диагонялям  3х4 шт """
        sens_45_up_left, sens_45_up_right, sens_45_down_left, sens_45_down_right = 0,0,0,0
        sens_45_apl_up_left, sens_45_apl_up_right, sens_45_apl_down_left, sens_45_apl_down_right = 0,0,0,0
        sens_45_tail_up_left, sens_45_tail_up_right, sens_45_tail_down_left, sens_45_tail_down_right = 0,0,0,0


        for iter in range(1, self.size+1):
            if self.arr[i-iter, j-iter] == 2:
                sens_45_apl_up_left = iter
                break
            if self.arr[i-iter, j-iter] == 1:
                sens_45_tail_up_left = iter
                break
            if self.arr[i-iter, j-iter] == 4:
                sens_45_up_left = iter
                break

        for iter in range(1, self.size + 1):
            if self.arr[i + iter, j - iter] == 2:
                sens_45_apl_down_left = iter
                break
            if self.arr[i + iter, j - iter] == 1:
                sens_45_tail_down_left = iter
                break
            if self.arr[i + iter, j - iter] == 4:
                sens_45_down_left = iter
                break

        for iter in range(1, self.size + 1):
            if self.arr[i-iter, j+iter] == 2:
                sens_45_apl_up_right = iter
                break
            if self.arr[i-iter, j+iter] == 1:
                sens_45_tail_up_right = iter
                break
            if self.arr[i-iter, j+iter] == 4:
                sens_45_up_right = iter
                break

        for iter in range(1, self.size + 1):
            if self.arr[i+iter, j+iter] == 2:
                sens_45_apl_down_right = iter
                break
            if self.arr[i+iter, j+iter] == 1:
                sens_45_tail_down_right = iter
                break
            if self.arr[i+iter, j+iter] == 4:
                sens_45_down_right = iter
                break


        sens = [['стена ↑' , sens_up], ['стена ↓' , sens_down], ['стена ←' , sens_left], ['стена →' , sens_right]]
        sens_apl = [['яблок ↑' , sens_apl_up], ['яблок ↓' , sens_apl_down], ['яблок ←' , sens_apl_left], ['яблок →' , sens_apl_right]]
        sens_apl_sq = [['ябл ↑ ←' , sens_apl_up_left], ['ябл ↑ →' , sens_apl_up_right], ['ябл ↓ ←' , sens_apl_down_left], ['ябл ↓ →' , sens_apl_down_right]]
        sens_tail = [['хвост ↑' , sens_tail_up], ['хвост ↓' , sens_tail_down], ['хвост ←' , sens_tail_left], ['хвост →' , sens_tail_right]]
        sens_sekt = [['сектр ↑' , sens_sekt_up], ['сектр ↓' , sens_sekt_down], ['сектр ←' , sens_sekt_left], ['сектр →' , sens_sekt_right]]
        sens_45 = [['с45 ↑ ←', sens_45_up_left] ,['с45 ↑ →', sens_45_up_right],['с45 ↓ ←', sens_45_down_left],['с45 ↓ →', sens_45_down_right]]
        sens_45_apl = [['я45 ↑ ←', sens_45_apl_up_left] ,['я45 ↑ →', sens_45_apl_up_right],['я45 ↓ ←', sens_45_apl_down_left],['я45 ↓ →', sens_45_apl_down_right]]
        sens_45_tail = [['х45 ↑ ←', sens_45_tail_up_left] ,['х45 ↑ →', sens_45_tail_up_right],['х45 ↓ ←', sens_45_tail_down_left],['х45 ↓ →', sens_45_tail_down_right]]



        lib = {'sens':sens, 'sens_apl':sens_apl, 'sens_apl_sq':sens_apl_sq,
                    'sens_tail':sens_tail, 'sens_sekt':sens_sekt, 'sens_45':sens_45,
                    'sens_45_apl':sens_45_apl, 'sens_45_tail':sens_45_tail}

        """Функция нормолизации численных значений сенсоров по экспоненте, близко - 1, далеко → к нулю"""
        def norm_sens(lib):
            for i in range(0,4):
                if lib['sens'][i][1] !=0 : lib['sens'][i][1] = 1 / (lib['sens'][i][1])
                if lib['sens_apl'][i][1] !=0 : lib['sens_apl'][i][1] = 1 / (lib['sens_apl'][i][1])
                if lib['sens_45'][i][1] !=0 : lib['sens_45'][i][1] = 1 / (lib['sens_45'][i][1])
                if lib['sens_45_apl'][i][1] !=0 : lib['sens_45_apl'][i][1] = 1 / (lib['sens_45_apl'][i][1])
                if lib['sens_45_tail'][i][1] !=0 : lib['sens_45_tail'][i][1] = 1 / (lib['sens_45_tail'][i][1])
                if lib['sens_tail'][i][1] !=0 : lib['sens_tail'][i][1] = 1 / (lib['sens_tail'][i][1])
                if lib['sens_apl_sq'][i][1] !=0 : lib['sens_apl_sq'][i][1] = 1 / (lib['sens_apl_sq'][i][1])

            return lib

        self.sens_lib = norm_sens(lib)
        self.snake_sensors = []
        for s in self.sens_lib:
            for i in range (0,4):
                self.snake_sensors.append(self.sens_lib[s][i][1])

        return self.sens_lib
