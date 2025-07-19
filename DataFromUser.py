
import pandas as pd
from pathlib import Path

def get_table_from_user(file_path):
    if not Path(file_path).exists():
        print("Ошибка: файл не найден!")
        return 0
    elif not file_path.lower().endswith(('.xlsx', '.xls')):
        print("Ошибка: файл должен быть в формате .xlsx или .xls!")
        return 0
    try:
        df = pd.read_excel(file_path, engine='openpyxl')

        print(f"Успешно загружен файл: {file_path}")
        print(f"Количество строк: {len(df)}, столбцов: {len(df.columns)}")
        print(df)


        # print("\nОбработка строк:")
        # for index, row in df.iterrows():
        #     for col_name, value in row.items():
        #         print(f"{col_name}: {value}")



    except Exception as e:
        print(f"Ошибка: {e}")


file_path = input("Введите путь к Excel-файлу: ").strip()
get_table_from_user(file_path)
# C:\Users\vladc\Downloads\ts.xlsx