import pandas as pd

pd.set_option('display.max_columns', None)
df = pd.read_csv('workout_data.csv')


# print(df.head())

# checklist
# pandas(filter, groupby, load_data, agg_func) - in_process
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


class Analysis(object):
    def __init__(self, df):
        self.df = df
        self._converter()
        if not self._valid_col():
            raise ValueError("DataFrame columns have incorrect types")

    def _valid_col(self):
        if self.df['Date'].dtypes == 'datetime64[us]' and all(self.df[col].dtype == 'str' for col in ['Workout_Split', 'Exercise']) and \
            all(self.df[col].dtype == 'int64' for col in ['Sets', 'Reps', 'RPE', 'Duration_min']) and self.df['Weight_kg'].dtype == 'float64':
            print(1)
            return True
        else:
            return False

    def _converter(self):
        self.df['Date'] = pd.to_datetime(df['Date'])

    def max_weight_changes(self, exercise, time_period = 5):
        df['Month_Number'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year
        start_month = min(df['Date']).month
        end_month = start_month +  time_period
        start_year = min(df['Date']).year
        end_year = min(df['Date']).year + end_month // 12
        while end_month > 12:
            end_month = end_month - 12

        first_month = df.query('Month_Number == @start_month and Year == @start_year and Exercise == @exercise')['Weight_kg'].mean()
        if type(first_month) == float: # Если данных нет то first_month будет NaN и его тип будет float, а не int
            print('No data for the first month with this exercise')
            return
        last_month = df.query('Month_Number == @end_month and Year == @end_year and Exercise == @exercise')['Weight_kg'].mean()
        if type(last_month) == float: # Если данных нет то last_month будет NaN и его тип будет float, а не int
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
            print(f"План сбалансирован: среднее время всех сплитов варьируется от {min_duration_min:.1f} до {max_duration_min:.1f} мин.")
            print(f"Субъективная тяжесть (RPE) также равномерна: {min_rpe:.1f} - {max_rpe:.1f} из 10.")
        else:
            hardest_split = stats['RPE'].idxmax()
            longest_split = stats['Duration_min'].idxmax()
            print("Обнаружен дисбаланс в тренировочном плане!")
            if hardest_split == longest_split:
                print(
                    f'Тренировки {hardest_split} объективно самые тяжелые: они длятся {max_duration_min:.1f} мин. и имеют самый высокий средний показатель тяжести (RPE {max_rpe:.1f}/10).')
            else:
                print(f"Самый тяжелый день по RPE: {hardest_split} ({max_rpe:.1f}/10)")
                print(f"Самый долгий день: {longest_split} ({max_duration_min:.1f} мин)")


# df['Date'] = pd.to_datetime(df['Date'])
#
# start_month = max(df['Date']).month
# print(start_month)
# print(int(str(max(df['Date'])).split('-')[1])+6)
a = Analysis(df)
a.hard_exercise()
# 1 осозноный вывод
# arr_exercise = list(df['Exercise'].unique())
# dict_exercise = {}
# for exercise in arr_exercise:
#     changes = a.max_weight_changes(exercise)
#     # print(f'{exercise}: +{changes}')
#     dict_exercise[exercise] = changes
# exercise_with_max_changes, weight = max(dict_exercise.items(), key=operator.itemgetter(1))
# print(exercise_with_max_changes, weight)
