import pandas as pd

pd.set_option('display.max_columns', None)
df = pd.read_csv('workout_data.csv')


# print(df.head())

# checklist
# pandas(filter, groupby, load_data, agg_func) - done
# numpy(std,mean,median, job_with_massive) - in_process
# generator(2) - in_process
# decorater(2) - in_process
# cli - in process
# pytest - in_process
# visual - in_process
#
#Двнные доступные мне:
# Date - дата тренировки
# Workout_Split - тип тренировки (Грудь/Трицепс, Спина/Бицепс, Ноги/Плечи)
# Exercise - конкретное упражнение (Жим лежа, Присед, Становая и т.д.)
# Sets - количество подходов (3-5)
# Reps - количество повторений в подходе (5-12)
# Weight_kg - рабочий вес в килограммах
# RPE (Rate of Perceived Exertion) - шкала тяжести от 1 до 10
# Duration_min - общая длительность тренировки в минутах

# Идеи:
# Декараторы:
# Авто оформление текста рамками ------
# Логирование действий и изменений
# Время выполнения

class Analysis(object):
    def __init__(self, df):
        self.df = df
        self.dict_month = {
            1: 'Январь',
            2: "Февраль",
            3: "Март",
            4: "Апрель",
            5: "Май",
            6: "Июнь",
            7: "Июль",
            8: "Август",
            9: "Сентябрь",
            10: "Октябрь",
            11: "Ноябрь",
            12: "Декабрь",
        }
        self._converter()
        if not self._valid_col():
            raise ValueError("DataFrame columns have incorrect types")


    def _valid_col(self):
        try:
            is_date = pd.api.types.is_datetime64_any_dtype(self.df['Date'])
            is_str = all(pd.api.types.is_string_dtype(self.df[col]) for col in ['Workout_Split', 'Exercise'])
            is_num = all(pd.api.types.is_numeric_dtype(self.df[col]) for col in
                         ['Sets', 'Reps', 'RPE', 'Duration_min', 'Weight_kg'])
            return is_date and is_str and is_num
        except KeyError:  # Если какой-то колонки вообще нет
            return False

    def _converter(self):
        self.df['Date'] = pd.to_datetime(df['Date'])
        self.df['Month_Number'] = df['Date'].dt.month
        self.df['Year'] = df['Date'].dt.year

    def max_weight_changes(self, exercise, time_period = 5):
        start_month = min(self.df['Date']).month
        end_month = start_month +  time_period
        start_year = min(self.df['Date']).year
        end_year = min(self.df['Date']).year + end_month // 12
        while end_month > 12:
            end_month = end_month - 12

        first_month = self.df.query('Month_Number == @start_month and Year == @start_year and Exercise == @exercise')['Weight_kg'].mean()
        if pd.isna(first_month):
            print('No data for the first month with this exercise')
            return
        last_month = self.df.query('Month_Number == @end_month and Year == @end_year and Exercise == @exercise')['Weight_kg'].mean()
        if pd.isna(last_month):
            print('No data for the last month with this exercise')
            return

        return last_month - first_month

    def hard_exercise(self):
        stats = self.df.groupby('Workout_Split').agg({'Duration_min': 'mean', 'RPE': 'mean'})
        max_duration_min = stats['Duration_min'].max()
        min_duration_min = stats['Duration_min'].min()
        duration_dif = max_duration_min - min_duration_min
        max_rpe = stats['RPE'].max()
        min_rpe = stats['RPE'].min()
        rpe_dif = max_rpe - min_rpe
        if duration_dif < 5 and rpe_dif < 0.5:
            return (f"План сбалансирован: среднее время всех сплитов варьируется от {min_duration_min:.1f} до {max_duration_min:.1f} мин"
                f"Субъективная тяжесть (RPE) также равномерна: {min_rpe:.1f} - {max_rpe:.1f} из 10")
        else:
            hardest_split = stats['RPE'].idxmax()
            longest_split = stats['Duration_min'].idxmax()
            print()
            if hardest_split == longest_split:
                return ("Обнаружен дисбаланс в тренировочном плане!"
                    f'\nТренировки {hardest_split} объективно самые тяжелые: они длятся {max_duration_min:.1f} мин. и имеют самый высокий средний показатель тяжести (RPE {max_rpe:.1f}/10)')
            else:
                return ("Обнаружен дисбаланс в тренировочном плане!"
                    f"\n Самый тяжелый день по RPE: {hardest_split} ({max_rpe:.1f}/10)"
                    f"Самый долгий день: {longest_split} ({max_duration_min:.1f} мин)")

    def max_weight(self):
        self.df['Tonnage'] = self.df['Sets'] * self.df['Reps'] * self.df['Weight_kg']
        monthly_tonnage = self.df.groupby(['Year', 'Month_Number'])['Tonnage'].sum()

        best_year, best_month = monthly_tonnage.idxmax()
        best_tonnage = monthly_tonnage.max()

        if best_month == 1:
            prev_month = 12
            prev_year = best_year - 1
        else:
            prev_month = best_month - 1
            prev_year = best_year

        month_name = self.dict_month[best_month]

        if (prev_year, prev_month) in monthly_tonnage.index:
            prev_tonnage = monthly_tonnage[(prev_year, prev_month)]
            diff = best_tonnage - prev_tonnage
            percent = (diff / prev_tonnage) * 100

            return (f"Самым продуктивным месяцем стал {month_name} {best_year} года: "
                    f"суммарно поднято {int(best_tonnage)} кг "
                    f"Это на {int(diff)} кг ({percent:.1f}%) больше, чем в предыдущем месяце")
        else:
            return (f"Самым продуктивным месяцем стал {month_name} {best_year} года: "
                    f"суммарно было поднято {int(best_tonnage)} кг. железа.")

    def rpe_correlation(self):
        hard_exercises = ['Squat', 'Deadlift', 'Bench Press']  # Сложные упражнения
        easy_exercises = ['Tricep Extension', 'Barbell Curl']  # Полегче упражнения

        hard_rpe = self.df[self.df['Exercise'].isin(hard_exercises)]['RPE'].mean()
        easy_rpe = self.df[self.df['Exercise'].isin(easy_exercises)]['RPE'].mean()

        diff = hard_rpe - easy_rpe

        if diff > 0.5:
            return (f"Выявлена зависимость: тяжёлые базовые упражнения (Присед, Становая, Жим) "
                    f"истощают сильнее. \nИх средняя тяжесть оценивается в {hard_rpe:.1f}/10 баллов, "
                    f"тогда как упражнения на руки (бицепс, трицепс) даются легче — {easy_rpe:.1f}/10 баллов")
        elif diff < -0.5:
            return (f"Аномалия: упражнения на руки даются тяжелее тяжёлых базовых "
                    f"RPE упражнений на руки: {easy_rpe:.1f}, RPE тяжёлой базы: {hard_rpe:.1f}")
        else:
            return (f"Уровень напряжения (RPE) одинаков для всех групп мышц "
                    f"Тяжёлая база: {hard_rpe:.1f}/10, упражнения на руки: {easy_rpe:.1f}/10")

    def pick_activiti(self):
        if "Tonnage" not in self.df.columns:
            self.df['Tonnage'] = self.df['Sets'] * self.df['Reps'] * self.df['Weight_kg']
        pick = self.df.groupby('Date').agg({'Duration_min': 'sum', 'RPE': 'mean', 'Tonnage': 'sum'})
        date_pick = pick["Tonnage"].idxmax()
        max_tonnage = pick.loc[date_pick, 'Tonnage']
        max_duration = pick.loc[date_pick, 'Duration_min']
        avg_rpe = pick.loc[date_pick, 'RPE']
        formated_date = date_pick.strftime('%d.%m.%Y')
        return (f"Самый активный ('хардкорный') день за всё время: {formated_date}\n"
                f"В этот день суммарный поднятый вес превысил: {int(max_tonnage)} кг. за сессию\n"
                f"Тренировка длилась рекордные {int(max_duration)} минут, а средняя тяжесть (RPE) составила {avg_rpe:.1f}/10")

    # Генераторы
    def unique_exercise(self):
        exercises = self.df['Exercise'].unique()
        for exercise in exercises:
            yield exercise

    def get_hardcore_day(self, user_rpe = 9.0):
        days = self.df.groupby('Date')['RPE'].mean()
        for day, rpe in days.items():
            if rpe >= user_rpe:
                yield f'Хардкорный день: {day.strftime("%d.%m.%Y")} с RPE {rpe:.1f}/10'

# df['Date'] = pd.to_datetime(df['Date'])
#
# start_month = max(df['Date']).month
# print(start_month)
# print(int(str(max(df['Date'])).split('-')[1])+6)
a = Analysis(df)
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
