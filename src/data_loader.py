from datetime import datetime
import os
import pandas as pd
from colorama import init, Fore

init(autoreset=True)


def check_data():
    if not os.path.exists('workout_data.csv'):
        print("Нужно создать базу тренеровок!")
        df = pd.DataFrame(
            columns=['Date', 'Workout_Split', 'Exercise', 'Sets', 'Reps', 'Weight_kg', 'RPE', 'Duration_min'])
        create_data(df)


def create_data(df):
    print(Fore.CYAN + "=== Режим добавления тренировок ===")

    while True:
        user_data = input("\nВведите дату тренировки в формате ГГГГ-ММ-ДД или stop если хотите остановиться: ")

        if user_data.lower() == 'stop':
            if len(df) == 0:
                print(Fore.RED + "В базе пока нет данных, введите хотя бы 1 тренировку!")
                continue
            else:
                break

        try:
            valid_date = datetime.strptime(user_data, '%Y-%m-%d')
            date = valid_date.strftime('%Y-%m-%d')
        except ValueError:
            print(Fore.RED +'Некоретный ввод даты, пример даты: 2021-12-31')
            continue
        workout_split = input("Введите тип тренировки (Chest/Triceps, Back/Biceps, Legs/Shoulders): ")
        exercise = input("Введите конкретное упражнение (Deadlift, Pull-up, Squat и т.д.): ")
        while True:
            try:
                sets = int(input("Введите количество подходов: "))
                reps = int(input("Введите количество повторений в подходе: "))
                break
            except ValueError:
                print(Fore.RED + 'Введите целое число!!!')

        while True:
            try:
                weight_kg = float(input("Введите рабочий вес (kg): "))
                break
            except ValueError:
                print(Fore.RED +'Введите число (Можно не целое, например 40.1)!!!!')

        while True:
            try:
                rpe = int(input("Введите шкала тяжести от 1 до 10: "))
                if 1 <= rpe <= 10:
                    break
                else:
                    print('Введите число от 1-10!!!!')
            except ValueError:
                print(Fore.RED +'Введите целое число!!!')

        while True:
            try:
                duration_min = int(input("Введите общая длительность тренировки (min): "))
                break
            except ValueError:
                print(Fore.RED +"Введите целое число!")

        new_row = {
            'Date': date,
            'Workout_Split': workout_split,
            'Exercise': exercise,
            'Sets': sets,
            'Reps': reps,
            'Weight_kg': weight_kg,
            'RPE': rpe,
            'Duration_min': duration_min
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        print(Fore.GREEN + "Тренировка успешно добавлена!")

    df.to_csv('workout_data.csv', index=False)
    print(Fore.GREEN + f"\n💾 Данные успешно сохранены в 'workout_data.csv'. Всего записей: {len(df)}")


def load_data(check_y_or_n=True):
    if check_y_or_n:
        check_data()
    return pd.read_csv('workout_data.csv')
