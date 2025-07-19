from math import exp, pi

def plank_func(t, length):
    c1 = 3.7412 * 10 ** -16
    c2 = 1.4388 * 10 ** -2
    e0 = c1 / (length ** 5 * (exp(c2 / (length * t)) - 1))
    return e0 * 10 ** -9


for wavelength in range(380, 1101):
    print(wavelength, plank_func(2700, wavelength * 10 ** -9))
