import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
am15g = pd.read_csv('data.txt', delim_whitespace=True, skiprows=1, header=None,
                    usecols=[0, 1], names=['Wavelength', 'Spectral_irradiance'])

am15g = am15g[(am15g['Wavelength'] >= 380) & (am15g['Wavelength'] <= 1100)]
common_wls = np.arange(380, 1101, 1)

solar_spectrum = np.interp(
    common_wls,
    am15g['Wavelength'].values.astype(float),
    am15g['Spectral_irradiance'].values.astype(float),
    left=0,
    right=0
)
lamps = ['L1', 'L2', 'L3', 'L4', 'L5']
lamp_names = {
    "L1": "УФ-Светодиод 395НМ",
    "L2": "Синий FullSpectrum",
    "L3": "Белый Солнечный",
    "L4": "Теплый Белый",
    "L5": "ИК-Модуль 950НМ"
}
lamp_spectra = {}
lamp_coeffs = {
    "L1": 0.75,
    "L2": 1.20,
    "L3": 0.95,
    "L4": 1.10,
    "L5": 0.85
}

for lamp_id in lamps:
    df = pd.read_csv(f'{lamp_id}_spectrum.csv')
    lamp_spectra[lamp_id] = np.interp(
        common_wls,
        df['Wavelength'].values.astype(float),
        df['Intensity'].values.astype(float),
        left=0,
        right=0
    )

synthetic_spectrum = np.zeros_like(common_wls, dtype=float)
for lamp_id in lamps:
    synthetic_spectrum += lamp_coeffs[lamp_id] * lamp_spectra[lamp_id]

plt.figure(figsize=(14, 8))

plt.plot(common_wls, solar_spectrum, 'k-', linewidth=2.5, label='Солнечный спектр AM 1.5G')

plt.plot(common_wls, synthetic_spectrum, 'r--', linewidth=1.8, label='Синтезированный спектр')

colors = ['violet', 'blue', 'green', 'orange', 'red']
for i, lamp_id in enumerate(lamps):
    contrib = lamp_coeffs[lamp_id] * lamp_spectra[lamp_id]
    plt.plot(common_wls, contrib, color=colors[i], linestyle=':',
             alpha=0.8, label=f'{lamp_names[lamp_id]}')
plt.fill_between(common_wls, solar_spectrum, synthetic_spectrum,
                 where=(synthetic_spectrum > solar_spectrum),
                 color='red', alpha=0.15, label='Превышение эталона')
plt.fill_between(common_wls, solar_spectrum, synthetic_spectrum,
                 where=(synthetic_spectrum < solar_spectrum),
                 color='blue', alpha=0.15, label='Недостаток до эталона')

plt.title('Сравнение синтезированного спектра с солнечным', fontsize=16)
plt.xlabel('Длина волны (нм)', fontsize=12)
plt.ylabel('Спектральная освещенность (Вт·м⁻²·нм⁻¹)', fontsize=12)
plt.legend(loc='upper right', fontsize=9)
plt.grid(alpha=0.2)
plt.xlim(380, 1100)
plt.ylim(0, 1.2 * max(solar_spectrum.max(), synthetic_spectrum.max()))

# Сохранение и отображение
plt.savefig('solar_vs_synthetic.png', dpi=300, bbox_inches='tight')
plt.show()

print("График сохранен как 'solar_vs_synthetic.png'")
