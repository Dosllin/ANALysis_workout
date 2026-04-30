from src.analysis import Analysis
from src.data_loader import create_data, load_data
from src.decorators import format_output
from colorama import init, Fore
init(autoreset=True)


def pause():
    input("\n[Нажмите Enter, чтобы продолжить...]")

def print_banner():
    banner = """
    ██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗ ██████╗ ██╗   ██╗████████╗
    ██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝██╔═══██╗██║   ██║╚══██╔══╝
    ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ ██║   ██║██║   ██║   ██║   
    ██║███╗██║██║   ██║██╔══██╗██╔═██╗ ██║   ██║██║   ██║   ██║   
    ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗╚██████╔╝╚██████╔╝   ██║   
     ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   
                        A N A L Y T I C S
    """
    # Если используешь colorama, оберни в Fore.CYAN
    print(Fore.CYAN + banner)



@format_output('Подменю', False)
def submenu_analysis(has_settings=False):
    while True:
        print('1. ▶️ Старт')
        if has_settings:
            print('2. ⚙️ Настройки')
        print('0. 🔙 Вернуться назад')

        user_input = input('Введите команду: ')

        # Если настроек нет, но пользователь нажал 2
        if not has_settings and user_input == '2':
            print(Fore.RED + 'Для этого анализа нет настроек.')
            continue

        if user_input in ['0', '1', '2']:
            return user_input
        else:
            print(Fore.RED + 'Такой команды нет')


def menu_progress_analysis(analys):
    time_period = 5
    while True:
        submenu_choise = submenu_analysis(has_settings=True)
        if submenu_choise == '1':
            print(f"Текущие настройки: Период = {time_period} мес.")
            arr_exercise = list(analys.unique_exercise())  # Опа использую генератор
            dict_exercise = {}

            for exercise in arr_exercise:
                changes = analys.max_weight_changes(exercise, time_period)
                if type(changes) != str:
                    print(f'{exercise}: {changes:+0.1f}')
                    dict_exercise[exercise] = changes
            if dict_exercise != {}:
                exercise_with_max_changes, weight = max(dict_exercise.items(), key=lambda x: x[1])
                print(Fore.CYAN + f'🏆 Максимальный прогресс упражнения: {exercise_with_max_changes}: {weight:+0.1f}, кг.')
            else:
                print(Fore.RED + 'Нет данных за данный временной период для всех упражнений')
            pause()
            break
        elif submenu_choise == '2':
            while True:
                print(f"Текущие настройки: Период = {time_period} мес.")
                print('1. Узнать прогресс для определенного упражнения',
                      '2. Указать временной период',
                      '0. Выйти', sep='\n')

                user_command = input('Введите команду: ')

                if user_command == '2':
                    while True:
                        try:
                            time_period = int(input('Введите временной период'))
                            break
                        except ValueError:
                            print(Fore.RED +'Введите число!')
                    print(Fore.GREEN + "Настройки сохранены!")
                    pause()
                elif user_command == '1':
                    user_exercise = input('Введите упражнение: ')
                    print(analys.max_weight_changes(user_exercise, time_period))
                    pause()
                    break
                elif user_command == '0':
                    break
                else:
                    print(Fore.RED + 'Такой команды нет!')
                    pause()
        elif submenu_choise == '0':
            break
        else:
            print(Fore.RED + 'Такой команды нет!')
            pause()


def analysis_menu(analys):
    # Подмен с выводами анализов
    while True:
        print("\n 📊  МЕНЮ АНАЛИТИКИ И ВЫВОДОВ")
        print("1. 📈 Прогресс в упражнении (Разница весов)",
              "2. ⚖️  Баланс тренировочного плана (Сплит-анализ)",
              "3. 🏆 Самый продуктивный месяц (Макс. Тоннаж)",
              "4. 🧠 Влияние тяжести",
              "5. 🦍 Поиск пикового 'хардкорного' дня",
              "6. 📉 Анализ стабильности весов (Numpy)",
              '7. 🩸 Выдача "хардкорных" дней',
              "8. 🏆 Достижения",
              "0. 🔙 Вернуться в главное меню", sep='\n')
        user_command = input("Выберите номер вывода (0-7): ")
        if user_command == '0':
            break
        try:
            if user_command == '1':
                menu_progress_analysis(analys)
            elif user_command == '2':
                if submenu_analysis() == '1':
                    analys.hard_exercise()
                    pause()
            elif user_command == '3':
                if submenu_analysis() == '1':
                    analys.max_weight()
                    pause()
            elif user_command == '4':
                if submenu_analysis() == '1':
                    analys.rpe_correlation()
                    pause()
            elif user_command == '5':
                if submenu_analysis() == '1':
                    analys.pick_activiti()
                    pause()
            elif user_command == '6':
                if submenu_analysis() == '1':
                    print("Доступные упражнения:", ', '.join(analys.df['Exercise'].unique()))
                    user_ex = input("Введите упражнение: ")
                    analys.weight_stability(user_ex)
                    pause()
            elif user_command == '7':
                if submenu_analysis() == '1':
                    while True:
                        try:
                            user_rpe = int(input('Введите минимальный rpe: '))
                            break
                        except ValueError:
                            continue

                    print('#' * 50)
                    for day in analys.get_hardcore_day(user_rpe):
                        print(f'-{day}')
                    print('#' * 50)
                    pause()
            elif user_command == '8':
                analys.get_achievements()
                pause()

        except Exception as e:
            print(f'Произошла ошибка при анализе: {e}')


def interactive_menu():
    while True:
        analys = Analysis()
        print_banner()
        print('1. Провести анализ данных 📊',
              '2. Записать данные о тренеровке 📝',
              '3. Выйти 🚪', sep='\n')
        try:
            user_input = int(input("Введите команду: "))
        except ValueError:
            print('Введите число')
            continue
        if user_input == 2:
            create_data(load_data(False))
        elif user_input == 1:
            analysis_menu(analys)
        elif user_input == 3:
            print("Спасибо за использование программы! Качай железо! 💪\n")
            break
        else:
            print(Fore.RED + "Такой команды не существует!")

