from .report import InputConnect

vacancies = 'вакансии'
statistics = 'статистика'
inputs = (vacancies, statistics)
input_text = 'Вакансии или статистика? '
error = 'Некорректное значение ввода, попробуйте, пожалуйста, ещё раз.'
file_name = '*.csv'
vacancy = 'Программист'
while True:
    result_input = str(input(input_text)).lower()
    if result_input.lower() in inputs:
        break
    print(error)
input_connect = InputConnect(file_name, vacancy)
if result_input == statistics:
    input_connect.generate_statistics(True)
elif result_input == vacancies:
    statistics1, statistics2, statistics3, statistics4, statistics5, statistics6 = input_connect.generate_statistics()
    input_connect.generate_vacancies(statistics1, statistics2, statistics3, statistics4, statistics5, statistics6)