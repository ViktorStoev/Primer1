from interactions import slash_command, SlashContext
import interactions
import os
import aiohttp
from sympy import symbols  # Импорт функции symbols из библиотеки sympy
from typing import List, Tuple
import matplotlib.pyplot as plt

def print_with_stars(message: str, n_stars=10):
    """
    Функция печати со звездочками - с побочными эффектом (нечистая) - вывод в консоль
    :param message: сообщение для печати
    :param n_stars: количество звездочек
    """
    print("*" * n_stars + message + "*" * n_stars)

print_with_stars("Вычисления не через функцию - немасштабируем, не оптимально")

k, T, C, L = symbols('k T C L')
#1 способ
C_ost = 1000000
Am_lst = []
C_ost_lst = []
for i in range(15):
    Am = (C - L) / T
    C_ost -= Am.subs({C: 1000000, T: 15, L: 0})
    Am_lst.append(round(Am.subs({C: 1000000, T: 15, L: 0}), 2))
    C_ost_lst.append(round(C_ost, 2))
print(f'Am_lst={Am_lst}\nC_ost_lst={C_ost_lst}')

# Проведение рефакторинга, оптимизация, аннотация типов, документация

# Библиотеку sympy здесь нет необходимости использовать
# Она предназначен для математических вычислений, сложных систем уравнений, интегралов, упрощения выражений, матриц и т.д.
def amortization1(C: float, T: int, L: float) -> Tuple[float, List[float]]:
    """
    Функция расчета амортизации по линейной формуле
    :param: C: первоначальная стоимость объекта
    :param: T: срок полезного использования (в целых годах)
    :param: L: ликвидационная стоимость объекта основных средств
    """
    Am = (C - L) / T
    C_history = []
    for _ in range(T):
        C -= Am
        C_history.append(round(C, 2))
    return Am, C_history

# Теперь можно получать резултат по заданным параметрам.
# Чистая функция - результат зависит исключительно от параметров - нет побочных эффектов
print_with_stars("Вычисления через функцию")
Am, C_history = amortization1(C=1000000, T=15, L=0)
print(f"Am = {Am}\nC_history = {C_history}")

print('\n')
print_with_stars("Способ 2")
# #2 способ
Aj = 0
C_ost = 1000000
Am_lst_2 = []
C_ost_lst_2 = []

for i in range(15):
    Am = k * 1 / T * (C - Aj)
    C_ost -= Am.subs({C: 1000000, T: 15, k: 2})
    Am_lst_2.append(round(Am.subs({C: 1000000, T: 15, k: 2}), 2))
    Aj += Am
    C_ost_lst_2.append(round(C_ost, 2))
print('Am_lst_2:', Am_lst_2)
print('C_ost_lst_2:', C_ost_lst_2)

# Снова перепишем через функцию
def amortization2(C: float, T: int, k: float) -> Tuple[List[float], List[float]]:
    """
    Функция расчета амортизации не по линейной формуле
    :param: C: первоначальная стоимость объекта
    :param: T: срок полезного использования (в целых годах)
    :param: k: амортизационный коэффициент
    """
    Am_history = []
    C_history = []
    Aj = 0
    C_i = C

    for _ in range(T):
        Am_i = k * (C - Aj) / T
        C_i -= Am_i
        Am_history.append(round(Am_i, 2))
        C_history.append(round(C_i, 2))
        Aj += Am_i
    return Am_history, C_history

print('\n')
print_with_stars("Способ 2 - через функцию")
Am_history_2, C_history_2 = amortization2(C=1000000, T=15, k=2)
print(f"Am_history_2 = {Am_history_2}\nC_history_2 = {C_history_2}")

# #Контейнер табличного вывода

print('\n')
print_with_stars("Работа с pandas")

import pandas as pd

def build_frame(C_history, Am_history):
    colums = ['Y', 'C_history', 'Am_history']
    y = range(1, len(C_history) + 1)
    table = list(zip(y, C_history, Am_history))
    return pd.DataFrame(table, columns=colums)

tframe = build_frame(C_ost_lst, Am_lst)
tframe2 = build_frame(C_ost_lst_2, Am_lst_2)

print(tframe)
print(tframe2)

print('\n')
print_with_stars("Визуализация")
# #Контейнер визуализации

plt.plot(tframe['Y'], tframe['C_history'], label='Am')
plt.plot(tframe2['Y'], tframe2['C_history'], label='Am_2')
plt.show()

def show_pie(Am_lst):
    vals = Am_lst
    labels = list(range(1, len(Am_lst) + 1))
    explode = [0.1] * len(Am_lst)
    fig, ax = plt.subplots()
    ax.pie(vals,
           labels=labels,
           autopct='%1.1f%%',
           shadow=True,
           explode=explode,
           wedgeprops={
               'lw': 1,
               'ls': '--',
               'edgecolor': "k"
           },
           rotatelabels=True)
    ax.axis("equal")
    plt.show()

show_pie(Am_lst)  # Доли амортизации при линейной
show_pie(Am_lst_2)  # Доли амортизации при НЕлинейной

def show_bar(tframe):
    plt.bar(tframe['Y'], tframe['Am_history'])
    plt.show()

show_bar(tframe)  # Диаграмма амортизации при линейной
show_bar(tframe2)  # Диаграмма амортизации при НЕлинейной

# Рассчет с другими параметраами

print("\n")
print_with_stars("Вариант 5")
# Вариант 5
Am_linear, C_history_linear = amortization1(C=1000000, T=15, L=0)
print(f"\nЛинейная амортизация\nAm={Am_linear}\nC_history = {C_history}")

Am_history_2, C_history_2 = amortization2(C=1000000, T=15, k=2)
print(
    f"\nНЕлинейная амортизация\nAm={Am_history_2}\nC_history = {C_history_2}")

print('\n')
print("Фреймы")
# Фреймы
tframe_var5 = build_frame(C_history_linear,
                          [Am_linear] * len(C_history_linear))
tframe2_var5 = build_frame(C_history_2, Am_history_2)

print(tframe_var5)
print(tframe2_var5)

print('\n')
print("Визуализация")

plt.plot(tframe_var5['Y'], tframe_var5['C_history'], label='Am')
plt.plot(tframe2_var5['Y'], tframe2_var5['C_history'], label='Am_2')
plt.show()

show_pie([Am_linear] * len(C_history))
show_pie(Am_history_2)

show_bar(tframe_var5)
show_bar(tframe2_var5)
