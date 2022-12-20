import statisticsReport
import vacanciesTable

input_data = input('Вакансии статистика: ')

if __name__ == '__main__':
    if input_data == 'Вакансии':
        vacanciesTable.main()
    elif input_data == 'Статистика':
        statisticsReport.main()