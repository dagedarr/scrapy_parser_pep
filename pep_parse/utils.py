import csv
import os
from datetime import datetime


class OutputFile:
    """
    Класс для вывода данных в файл.
    """
    @staticmethod
    def cvs_create(results, dir):
        """
        Создает CSV файл со сводкой по статусам и сохраняет его в указанную
        директорию.

        Параметры:
            results: Словарь с количеством PEP в каждом из статусов
            dir: Путь к директории, в которой будет создан CSV файл.
        """

        results_dir = dir / 'results'
        results_dir.mkdir(exist_ok=True)

        now = datetime.now()
        time_mask = now.strftime('%Y-%m-%d_%H-%M-%S')

        file_name = f'status_summary_{time_mask}.csv'
        csv_file_path = os.path.join(results_dir, file_name)

        with open(csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Статус', 'Количество'])

            csv_writer.writerows(
                [status, count] for status, count in results.items()
            )

            csv_writer.writerow(
                ['Всего', sum([count for count in results.values()])]
            )
