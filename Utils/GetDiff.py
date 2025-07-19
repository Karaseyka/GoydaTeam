import numpy as np
import pandas as pd
from DataFromUser import get_table_from_user


def get_difference(file_path1, file_path2):
    data_ref = get_table_from_user(file_path1)
    data_comb = get_table_from_user(file_path2)
    sirr_ref = data_ref["Spectral irradiance W⋅m^–2⋅nm^–1"].values
    sirr_comb = data_comb["Spectral irradiance W⋅m^–2⋅nm^–1"].values
    relative_diff = np.abs(sirr_comb - sirr_ref) / sirr_ref
    average_deviation = np.sum(relative_diff) * 100
    return average_deviation
print(f"Сумма относительное отклонение: {get_difference('C:/Users/vladc/Downloads/ts.xlsx', 'C:/Users/vladc/Downloads/ts.xlsx'):.2f}%")