import random
import numpy as np


# Symulacja odczytu wilgotności z czujników z różnymi błędami
def generate_sensor_data(true_value, num_sensors=5, error_type='random'):
    data = []
    for _ in range(num_sensors):
        if error_type == 'constant':
            # Stały błąd np. +3% do wyniku
            data.append(true_value * 1.03)
        elif error_type == 'random':
            # Losowy błąd w zakresie -5% do +5%
            error = random.uniform(-0.05, 0.05)
            data.append(true_value * (1 + error))
        elif error_type == 'noise':
            # Szum (gaussowski) np. odchylenie standardowe 2%
            noise = np.random.normal(0, 0.02)
            data.append(true_value * (1 + noise))
        else:
            data.append(true_value)
    return data


# Algorytm głosowania większościowego
def majority_voting(sensor_data):
    # Zakładamy, że dane są w zakresie np. wilgotności 0-100%
    rounded_data = [round(d) for d in sensor_data]
    return max(set(rounded_data), key=rounded_data.count)


# Algorytm głosowania medianowego
def median_voting(sensor_data):
    return np.median(sensor_data)


# Funkcja oceny poprawności systemu
def evaluate_accuracy(true_value, system_value):
    error = abs(true_value - system_value) / true_value * 100
    return 100 - error  # zwraca procent poprawności


# Symulacja systemu z 5 czujnikami
true_humidity = 50  # rzeczywista wilgotność
num_sensors = 5

# Testowanie różnych modeli błędów
for error_type in ['constant', 'random', 'noise']:
    print(f"\nModel błędów: {error_type}")

    # Generowanie danych z czujników
    sensor_data = generate_sensor_data(true_humidity, num_sensors, error_type)
    print(f"Dane z czujników: {sensor_data}")

    # Głosowanie większościowe
    majority_result = majority_voting(sensor_data)
    accuracy_majority = evaluate_accuracy(true_humidity, majority_result)
    print(f"Wynik głosowania większościowego: {majority_result}, Poprawność: {accuracy_majority:.2f}%")

    # Głosowanie medianowe
    median_result = median_voting(sensor_data)
    accuracy_median = evaluate_accuracy(true_humidity, median_result)
    print(f"Wynik głosowania medianowego: {median_result}, Poprawność: {accuracy_median:.2f}%")