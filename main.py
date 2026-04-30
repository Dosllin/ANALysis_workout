import argparse
from fake_progress_bars import progress_bar
from src.analysis import Analysis
from src.data_loader import create_data, load_data
from src.decorators import format_output
from src.display import interactive_menu
from colorama import init, Fore
init(autoreset=True)



# checklist
#
# pytest - in_process
# visual - in_process






def main():
    parser = argparse.ArgumentParser(description="Анализатор тренировок (CLI)")
    parser.add_argument(
        'command',
        nargs='?',
        choices=["menu", "add", "analyze", 'stats', 'report', 'hardcore_days', 'motivation'],
        default='menu',
        help='Команда для выполнения: menu, add, analyze, stats, report, hardcore_days'
    )

    args = parser.parse_args()

    analys = Analysis()

    if args.command == 'menu':
        interactive_menu()

    elif args.command == 'add':
        create_data(load_data(False))

    elif args.command == 'analyze':
        analysis_menu(analys)
    elif args.command == 'stats':
        analys.pick_activiti()
        analys.hard_exercise()
        analys.max_weight()

    elif args.command == 'report':
        print('#' * 50)
        print("📄 ГЕНЕРАЦИЯ ПОЛНОГО ОТЧЕТА ПО ТРЕНИРОВКАМ 📄")
        print('#' * 50)

        progress_bar(
            time=5,  # Время завершения индикатора
            size=50,  # Размер индикатора в символах
            step=10,  # Увеличение прогресса на каждом шаге
            label='Обработка...',  # Метка перед индикатором
            variability=0.1,  # Допустимое отклонение времени каждого шага
            progress='◼️',  # Символ, отображающий текущий прогресс
            remaining='·',  # Символ для оставшегося процента
            outside='⏺',  # Символ для границы
            percentage=True  # Отображать процент справа от индикатора
        )

        # 1 вывод
        print('=' * 10, 'Прогресс в упражнении'.capitalize(), '=' * 10)
        arr_exercise = list(analys.unique_exercise())  # Опа использую генератор
        dict_exercise = {}

        for exercise in arr_exercise:
            changes = analys.max_weight_changes(exercise)
            if type(changes) != str:
                print(f'{exercise}: {changes:+0.1f}')
                dict_exercise[exercise] = changes
        if dict_exercise != {}:
            exercise_with_max_changes, weight = max(dict_exercise.items(), key=lambda x: x[1])
            print(f'🏆 Максимальный прогресс упражнения: {exercise_with_max_changes}: {weight:+0.1f}, кг.')
        else:
            print('Нет данных за данный временной период для всех упражнений')
        print("=" * (22 + len('Прогресс в упражнении')))

        analys.hard_exercise()
        analys.max_weight()
        analys.rpe_correlation()
        analys.pick_activiti()
        [analys.weight_stability(x) for x in arr_exercise]
        print("\n✅ Отчет успешно сгенерирован!")

    elif args.command == 'hardcore_days':
        while True:
            try:
                user_rpe = int(input('Введите минимальный rpe: '))
                break
            except ValueError:
                continue
        print('#'*50)
        for day in analys.get_hardcore_day(user_rpe):
            print(f'-{day}')
        print('#'*50)

    elif args.command == 'motivation':
        quotes = [
            "Легкие веса не делают тебя сильнее! 💪",
            "No pain, no gain! 🦍",
            "Дисциплина бьет класс. Иди на тренировку! 🏋️‍♂️"
        ]
        import random
        print(Fore.CYAN + random.choice(quotes))


if __name__ == "__main__":
    main()
