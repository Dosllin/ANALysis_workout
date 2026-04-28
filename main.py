import pandas as pd
from src.analysis import Analysis
from src.data_loader import create_data, load_data


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
# a.hard_exercise()
# print(a.max_weight())
# print(a.rpe_correlation())
# print(a.pick_activiti())
# for i in a.get_hardcore_day(1):
#     print(i)
# 1 осозноный вывод
# arr_exercise = list(df['Exercise'].unique())
# dict_exercise = {}
# for exercise in arr_exercise:
#     changes = a.max_weight_changes(exercise)
#     # print(f'{exercise}: +{changes}')
#     dict_exercise[exercise] = changes
# exercise_with_max_changes, weight = max(dict_exercise.items(), key=operator.itemgetter(1))
# print(exercise_with_max_changes, weight)
def pause():
    input("\n[Нажмите Enter, чтобы продолжить...]")

def analysis_menu(analys):
    # Подмен с выводами анализов
    while True:
        print(" 📊  МЕНЮ АНАЛИТИКИ И ВЫВОДОВ")
        print("1. 📈 Прогресс в упражнении (Разница весов)",
            "2. ⚖️  Баланс тренировочного плана (Сплит-анализ)",
            "3. 🏆 Самый продуктивный месяц (Макс. Тоннаж)",
            "4. 🧠 Влияние тяжести",
            "5. 🦍 Поиск пикового 'хардкорного' дня",
            "0. 🔙 Вернуться в главное меню", sep='\n')
        choice = input("Выберите номер вывода (0-7): ")
        if choice == '0':
            break
        try:
            if choice == '1':
                user_exercise = input('Введите упражнение: ')
                print(analys.max_weight_changes(user_exercise))
                pause()
            elif choice == '2':
                print(analys.hard_exercise())
                pause()
            elif choice == '3':
                print(analys.max_weight())
                pause()
            elif choice == '4':
                print(analys.rpe_correlation())
                pause()
            elif choice == '5':
                print(analys.pick_activiti())
                pause()
        except Exception as e:
            print(f'Произошла ошибка при анализе: {e}')

def main():
    while True:
        analys = Analysis()
        print(" 🏋️‍♂️  АНАЛИЗАТОР ТРЕНИРОВОК (Workout Analytics)  🏋️‍♂️")
        print('1. Записать данные о тренеровке 📝',
              '2. Провести анализ данных 📊',
              '3. Выйти 🚪', sep='\n')
        try:
            user_input = int(input())
        except ValueError:
            print('Введите число')
            continue
        if user_input == 1:
            create_data(load_data(False))
        elif user_input == 2:
            analysis_menu(analys)
        elif user_input == 3:
            print("Спасибо за использование программы! Качай железо! 💪\n")
            break
        else:
            print("Такой команды не существует")
if __name__ == "__main__":
    main()
