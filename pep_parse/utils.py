import csv
import os
from datetime import datetime

from sqlalchemy import func


class OutputFile:
    """
    Класс для вывода данных в файл.
    """
    @staticmethod
    def cvs_create(session, model, dir):
        """
        Создает CSV файл со сводкой по статусам и сохраняет его в указанную
        директорию.

        Параметры:
            session: Объект сессии SQLAlchemy для выполнения запросов к
                     базе данных.
            model: Модель SQLAlchemy, представляющая таблицу, из которой будут
                   получены данные.
            dir: Путь к директории, в которой будет создан CSV файл.
        """

        status_counts = session.query(
            model.status, func.count(model.status)
        ).group_by(model.status).all()

        results_dir = dir / 'results'
        results_dir.mkdir(exist_ok=True)

        now = datetime.now()
        time_mask = now.strftime("%Y-%m-%d_%H-%M-%S")

        file_name = f'status_summary_{time_mask}.csv'
        csv_file_path = os.path.join(results_dir, file_name)

        with open(csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Статус', 'Количество'])
            total_count = 0
            for status, count in status_counts:
                csv_writer.writerow([status, count])
                total_count += count
            csv_writer.writerow(['Всего', str(total_count)])
