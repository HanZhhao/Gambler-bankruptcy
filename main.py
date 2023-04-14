import random
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

a_init_property = 50
b_init_property = 500
a_cost = 1
b_cost = 1
a_win_prob = 0.5
b_win_prob = 0.5
default_round = 100
sample_number = 10000

def play(init_property, cost, win_prob, model=1, rate=0, round=default_round):
    property = init_property
    for i in range(round):
        if win_prob < random.random():
            # it means a has winned
            if model == 1:
                property += cost
            elif model == 3:
                property += int(rate * property * 1000) / 1000
        else:
            if model == 1:
                property -= cost
            elif model == 3:
                property -= int(0.5 * rate * property * 1000) / 1000 
        krupt = check_krupt(property)
        if krupt:
            return -1
        if model == 1:
            if property >= a_init_property + b_init_property:
                return a_init_property + b_init_property
    return property

def check_krupt(money):
    if money <= 0.1:
        return 1
    return 0

def cal_sum(list):
    sum = 0
    for i in list:
        sum += i
    return sum

def model1():
    matrix = np.matrix([[1,0,0,0,0,0,0,0],[0.5,0,0.5,0,0,0,0,0],[0,0.5,0,0.5,0,0,0,0],[0,0,0.5,0,0.5,0,0,0],[0,0,0,0.5,0,0.5,0,0],[0,0,0,0,0.5,0,0.5,0],[0,0,0,0,0,0.5,0,0.5],[0,0,0,0,0,0,0,1]])
    result = matrix
    for i in range(3):
        result = np.matmul(result, matrix)
    sns.set(style='darkgrid', color_codes=True)
    sns.heatmap(data=result, annot=True, cmap="RdBu_r")
    plt.show()

def cal_krupt(result):
    kr2000 = 0
    kr3000 = 0
    kr4000 = 0
    kr5000 = 0
    for person in result:
        if person[0] == 0:
            if person[1] == 2000:
                kr2000 +=1
            elif person[1] == 3000:
                kr3000 +=1
            elif person[1] == 4000:
                kr4000 +=1
            elif person[1] == 5000:
                kr5000 +=1
    return (kr2000, kr3000, kr4000, kr5000)

def model2():
    for initial_property in range(10, 51,10):
        result = []
        for i in range(2000, 5001, 1000):
            for gam in range(sample_number):
                result1 = play(initial_property, a_cost, a_win_prob, round = i)
                if result1 == -1:
                    result1 = 0
                    result2 = a_init_property + b_init_property
                else:
                    result2 = a_init_property + b_init_property - result1
                result.append([result1, i, "a"])
                #result.append([result2, i, "b"])
        kr2000, kr3000, kr4000, kr5000 = cal_krupt(result)
        print(f"初始资金{initial_property}下，2000轮有百分之{kr2000/sample_number}的人破产，")
        print(f"初始资金{initial_property}下，3000轮有百分之{kr3000/sample_number}的人破产，")
        print(f"初始资金{initial_property}下，4000轮有百分之{kr4000/sample_number}的人破产，")
        print(f"初始资金{initial_property}下，5000轮有百分之{kr5000/sample_number}的人破产，")
    df = pd.DataFrame(result, columns=['property', 'round', 'person'])
    sns.boxplot(x="round", y="property", data=df)
    plt.show()

def cal_model3(rate, total_list):
    initial_property = 1
    for gam in range(sample_number):
        result1 = play(initial_property, 1, 0.5, 3, rate)
        if result1 == -1:
            result1 = 0
        total_list.append([result1, rate])

def model3():
    total_list = []
    for rate in [0.1, 0.2, 0.25, 0.3, 0.5]:
        cal_model3(rate, total_list)
    df = pd.DataFrame(total_list, columns=['property', 'rate'])
    df2 = df[df['property'] <= 300]
    sns.boxenplot(x="rate", y="property", data=df2)
    plt.show()

if __name__ == '__main__':
    random.seed(43)
    sns.set(style="whitegrid")
    choose = int(input("Which model would you test:(1,2,3):"))
    if choose == 1:
        model1()
    elif choose == 2:
        model2()
    elif choose == 3:
        model3()
    else:
        print("Wrong input!")
