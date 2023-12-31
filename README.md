# Snake
 
<b>Программа – тренажёр для обучения AI играть в игру-змейку. Генетический алгоритм</b>  
Видео: <a>https://youtu.be/Js6FjtkmcQc</a>

<b>Файлы и модули:</b>  
`snake_main` - основной файл тренажера  
`snake_matrix`  - поле и змейка, формирует матрицу игрового поля, генерирует яблоки, хранит информацию о состоянии и текущем положении змейки, рассчитывает данные сенсоров  
`rnd_snakes`  - генерация нулевых популяций и отбор лучших змей в семьях  
`snake_ai` – нейросеть, предсказание следующего хода  
`snake_draw`  - наполнение окна игры, отрисовки графики и таблиц  
`plot_to_img`  - скрипт открывается в отдельном процессе, берет данные из сохраненного файла статистики, генерирует график результатов семейств по эпохам, сохраняет график в файл.   
  
`snake_plot_clean.png` - картинка с пустым графиком  
`snake_plot.png` - график результатов, генерируется после каждой эпохи  
`snake_best_weights_ХХХХХХ_ХХХХ.bin` - файл с весами и результатами, генерируется каждый запуск программы   
`snake_statistics_ХХХХХХ_ХХХХ.csv` - файл со статистикой, генерируется каждый запуск программы  

  
<b>Стандартные и популярные библиотеки:</b>  
`os, time, datetime, pickle, shutil` – размещения окна, время, дата и работа с файлами (сохранение весов, статистики, графиков, копирование)  
`pygame` – окно игры, анимация, вывод таблиц результатов  
`pandas, matplotlib` – работа с данными, построение графиков обучения  
`multiprocessing` – создание нескольких потоков для расчета случайных весов на несколько семей одновременно   
`subprocess` – создает процесс, открывая скрипт построения графика, сохраняет график в файл  

  
<b>Алгоритм работы:</b>  
Каждая змейка - перцептрон с 2 скрытыми слоями, слоем сенсоров на входе и слоем направления следующего шага.  
  
<b>Этапы обучения:</b>  
- формируется несколько семейств из большого количества змей с рандомными весами  (10.000-100.000)  
- отбор змей с лучшими результатами из рандомных  
- многократное скрещивание змей в каждом семействе + мутация 1-5% и отбор лучших по количеству очков и ходов  
- скрещивание лучших змей из семей после 100 эпох - формирование супер-семьи  
- бесконечный цикл: игры-отбор лучших-скрещивание  
