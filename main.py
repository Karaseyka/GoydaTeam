from itertools import combinations
def select_bulbs(bulbs_dict, target_spectrum, max_bulbs=6, beam_width=100):
    keys = list(bulbs_dict.keys())
    n_bulbs = len(keys)
    
    # Вычисление MSE для заданного спектра
    def compute_mse(spectrum):
        mse = 0.0
        for i in range(721):
            diff = spectrum[i] - target_spectrum[i]
            mse += diff * diff
        return mse / 721
    
    # Переборный метод для n_bulbs <= 25
    if n_bulbs <= 25:
        candidates = []
        # Добавление пустого набора
        empty_spec = [0.0] * 721
        empty_mse = compute_mse(empty_spec)
        candidates.append((empty_mse, 0, 0.0, ()))
        
        # Перебор комбинаций от 1 до max_bulbs ламп
        max_size = min(max_bulbs, n_bulbs)
        for r in range(1, max_size + 1):
            for combo in combinations(keys, r):
                total_spec = [0.0] * 721
                total_cost = 0.0
                for bulb in combo:
                    spec, price = bulbs_dict[bulb]
                    total_spec = [total_spec[i] + spec[i] for i in range(721)]
                    total_cost += price
                mse_val = compute_mse(total_spec)
                candidates.append((mse_val, r, total_cost, combo))
        
        # Сортировка кандидатов: сначала по MSE, затем по количеству ламп, затем по стоимости
        candidates.sort(key=lambda x: (x[0], x[1], x[2]))
        best_combo = candidates[0][3]
        return list(best_combo)
    
    # Beam search для n_bulbs > 25
    else:
        # Инициализация пустого набора
        empty_spec = [0.0] * 721
        empty_mse = compute_mse(empty_spec)
        beam = [((), empty_spec, 0.0, empty_mse)]
        all_candidates = beam.copy()
        
        # Последовательное добавление ламп до max_bulbs
        for size in range(1, max_bulbs + 1):
            candidates_dict = {}
            for state in beam:
                current_set, current_spec, current_cost, current_mse = state
                for bulb in keys:
                    if bulb in current_set:
                        continue
                    # Создание нового набора
                    new_set = tuple(sorted(current_set + (bulb,)))
                    if new_set in candidates_dict:
                        continue
                    # Вычисление нового спектра и стоимости
                    spec_bulb, price_bulb = bulbs_dict[bulb]
                    new_spec = [current_spec[i] + spec_bulb[i] for i in range(721)]
                    new_cost = current_cost + price_bulb
                    mse_val = compute_mse(new_spec)
                    candidates_dict[new_set] = (new_set, new_spec, new_cost, mse_val)
            
            # Сортировка кандидатов по MSE
            candidates = list(candidates_dict.values())
            candidates.sort(key=lambda x: x[3])
            beam = candidates[:beam_width]
            all_candidates.extend(beam)
        
        # Выбор лучшего кандидата из всех рассмотренных
        all_candidates = [
            (mse, len(set_bulbs), cost, set_bulbs)
            for set_bulbs, spec, cost, mse in all_candidates
        ]
        all_candidates.sort(key=lambda x: (x[0], x[1], x[2]))
        best_set = all_candidates[0][3]
        return list(best_set)

# Пример использования
bulbs_dict = {
    'lamp1': ([1.0]*721, 100),
    'lamp2': ([2.0]*721, 200),
    # ... другие лампочки
}
target_spectrum = [3.0]*721  # Целевой спектр

selected_bulbs = select_bulbs(bulbs_dict, target_spectrum)
print("Выбранные лампочки:", selected_bulbs)
