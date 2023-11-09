import random
import numpy as np

""" Модуль нейросети
    - получает веса змеи, данные матрицы состояния мира змейки 
    - выдает решение о следуюзем ходе 
    - смешивает веса по 2м алгоритмам: для семейств; для этапа супер-семей 
"""



class Perceptron:

    def __init__(self, in_l_q, lay_1_q, lay_2_q, out_l_q):
        self.in_l_q = in_l_q
        self.lay_1_q = lay_1_q
        self.lay_2_q = lay_2_q
        self.out_l_q = out_l_q

    def relu(self, x):
        return np.maximum(x, 0)

    def new_pct(self):
        #self.inp_l = np.zeros(self.in_l_q)
        self.lay_1 = np.zeros(self.lay_1_q)
        self.lay_2 = np.zeros(self.lay_2_q)
        self.out_l = np.zeros(self.out_l_q)

    # генерация случайных весов
    def rand_w(self):
        self.w_in = np.random.uniform(-1, 1, (self.in_l_q, self.lay_1_q))
        self.w_lay = np.random.uniform(-1, 1, (self.lay_1_q, self.lay_2_q))
        self.w_out = np.random.uniform(-1, 1, (self.lay_2_q, self.out_l_q))

    # принимает данные весов
    def get_w(self, rw_in, rw_lay, rw_out):
        self.w_in = rw_in
        self.w_lay = rw_lay
        self.w_out = rw_out

    # цикл перемешивания весов
    def shuff(self, w1, w2, probability_a=70, probability_b=30,  k=0):  # k - вероятность мутации
        a = w1.ravel()  # форматируем в одномерный массив
        b = w2.ravel()
        c = []
        for i in range(0, len(a)):
            c.append(random.choices([a[i], b[i], random.uniform(-1, 1)], weights=[probability_a, probability_b, k]))
        new_w = np.array(c)
        new_w = new_w.reshape(w1.shape)  # форматируем в массив по образу входящего веса
        return new_w

    # функция перемешивания весов для этапа семей
    def w_suffle(self, wl ,probability_a ,probability_b, k):
        w_in_list = []
        w_lay_list = []
        w_out_list = []
        deti_list = []

        for ves in wl:
                    w_in_list.append(ves[0])
                    w_lay_list.append(ves[1])
                    w_out_list.append(ves[2])
                    deti_list.append([ves[0], ves[1], ves[2]])


        for i in range(0, len(w_in_list)):
            for j in range(0, len(w_in_list)):
                child_in = self.shuff(w_in_list[i], w_in_list[j], probability_a, probability_b, k)  # Вероятность мутации есть
                child_lay = self.shuff(w_lay_list[i], w_lay_list[j], probability_a, probability_b, k)
                child_out = self.shuff(w_out_list[i], w_out_list[j], probability_a, probability_b, k)
                deti_list.append([child_in, child_lay, child_out])

                child_in = self.shuff(w_in_list[i], w_in_list[j], probability_a, probability_b, 0)  # Вероятности мутации нет
                child_lay = self.shuff(w_lay_list[i], w_lay_list[j], probability_a, probability_b, 0)
                child_out = self.shuff(w_out_list[i], w_out_list[j], probability_a, probability_b, 0)
                deti_list.append([child_in, child_lay, child_out])


        return deti_list

    # функция перемешивания весов для этапа супер-семей
    def w_suffle_superfam(self, wl ,probability_a ,probability_b, k):
        w_in_list = []
        w_lay_list = []
        w_out_list = []
        deti_list = []

        for ves in wl:
                    w_in_list.append(ves[0])
                    w_lay_list.append(ves[1])
                    w_out_list.append(ves[2])
                    deti_list.append([ves[0], ves[1], ves[2]])


        for i in range(0, len(w_in_list)):
            deti_list.append([w_in_list[i], w_lay_list[i], w_out_list[i]])

            for j in range(0, len(w_in_list)):
                child_in = self.shuff(w_in_list[i], w_in_list[i], probability_a, probability_b, k)  # Вероятность мутации есть
                child_lay = self.shuff(w_lay_list[i], w_lay_list[i], probability_a, probability_b, k)
                child_out = self.shuff(w_out_list[i], w_out_list[i], probability_a, probability_b, k)
                deti_list.append([child_in, child_lay, child_out])

                child_in = self.shuff(w_in_list[i], w_in_list[j], probability_a, probability_b, k)  # Вероятности мутации нет
                child_lay = self.shuff(w_lay_list[i], w_lay_list[j], probability_a, probability_b, k)
                child_out = self.shuff(w_out_list[i], w_out_list[j], probability_a, probability_b, k)
                deti_list.append([child_in, child_lay, child_out])

        return deti_list

    # расчет решения о ходе
    def calculation(self, inp_l):
        self.inp_l = inp_l
        self.lay_1 = self.relu(np.dot(self.inp_l, self.w_in))
        self.lay_2 = self.relu(np.dot(self.lay_1, self.w_lay))
        self.out_l = np.dot(self.lay_2, self.w_out)

    # список с направлением следующего движения
    def solution(self):
        n = np.argmax(self.out_l)
        sol = [0,0,0,0]
        sol[n] = 1
        return sol
