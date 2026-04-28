import pandas as pd
from src.analysis import Analysis

pd.set_option('display.max_columns', None)

# print(df.head())

# checklist
# pandas(filter, groupby, load_data, agg_func) - done
# numpy(std,mean,median, job_with_massive) - in_process
# generator(2) - done
# decorater(2) - in_process
# cli - in process
# pytest - in_process
# visual - in_process
#


# Идеи:
# Декараторы:
# Авто оформление текста рамками ------
# Логирование действий и изменений
# Время выполнения



# df['Date'] = pd.to_datetime(df['Date'])
#
# start_month = max(df['Date']).month
# print(start_month)
# print(int(str(max(df['Date'])).split('-')[1])+6)
a = Analysis()
# a.hard_exercise()
# print(a.max_weight())
# print(a.rpe_correlation())
# print(a.pick_activiti())
for i in a.get_hardcore_day(1):
    print(i)
# 1 осозноный вывод
# arr_exercise = list(df['Exercise'].unique())
# dict_exercise = {}
# for exercise in arr_exercise:
#     changes = a.max_weight_changes(exercise)
#     # print(f'{exercise}: +{changes}')
#     dict_exercise[exercise] = changes
# exercise_with_max_changes, weight = max(dict_exercise.items(), key=operator.itemgetter(1))
# print(exercise_with_max_changes, weight)
