import random
import time

import numpy as np
from numpy.ma.extras import average


def smoothing_voter(inputs, prev_output=None, voter_threshold=0.1, smoothing_threshold=1.0):
    """
    Determines the output using the smoothing voter algorithm.

    Parameters:
    - inputs (list of float): The set of variant results.
    - prev_output (float or None): The previous successful voter output. None if first cycle.
    - voter_threshold (float): The threshold for determining majority agreement.
    - smoothing_threshold (float): The threshold for smoothing in case of disagreement.

    Returns:
    - float or None: The selected output, or None if no valid output can be determined.
    """
    n = len(inputs)
    if n < 3:
        raise ValueError("Smoothing voter requires at least three inputs.")

    # Sort inputs in ascending order
    sorted_inputs = sorted(inputs)

    # Step 1: Majority agreement check
    m = (n + 1) // 2
    for i in range(n - m + 1):
        subset = sorted_inputs[i:i + m]
        if max(subset) - min(subset) <= voter_threshold:
            # Majority found within the threshold
            return subset[m // 2]  # Median of the subset

    # Step 2: Disagreement handling
    if prev_output is None:
        # If no previous output, default to the median of all inputs
        return sorted_inputs[n // 2]

    closest_input = min(inputs, key=lambda x: abs(x - prev_output))
    if abs(closest_input - prev_output) <= smoothing_threshold:
        return closest_input

    # Step 3: No valid output
    return None



# Symulacja odczytu wilgotności z czujników z różnymi błędami
def generate_sensor_data(true_value, num_sensors=3, error_type='random'):
    data = []
    for _ in range(num_sensors):
        if error_type == 'constant':
            # Stały błąd np. +3% do wyniku
            data.append(round(true_value * 1.03, 2))
        elif error_type == 'random':
            # Losowy błąd w zakresie -5% do +5%
            error = random.uniform(-0.05, 0.05)
            data.append(round(true_value * (1 + error), 2))
        elif error_type == 'noise':
            # Szum (gaussowski) np. odchylenie standardowe 2%
            noise = np.random.normal(0, 0.02)
            data.append(round(true_value * (1 + noise), 2))
        else:
            data.append(true_value)
    return data



# Algorytm głosowania medianowego
def median_voting(sensor_data):
    return np.median(sensor_data)


# Funkcja oceny poprawności systemu
def evaluate_accuracy(true_value, system_value):
    error = abs(true_value - system_value) / true_value * 100
    return 100 - error  # zwraca procent poprawności


# Symulacja systemu z 5 czujnikami
true_humidity = 50  # rzeczywista wilgotność
num_sensors = 3
prev_smoothing_voter_output = None

median_voting_results = []
smoothing_voter_results = []

try:
    while True:
        # Generowanie danych z czujników
        sensor_data = generate_sensor_data(true_humidity, num_sensors, 'noise')
        print(f"Dane z czujników: {sensor_data}")

        # Głosowanie medianowe
        median_result = median_voting(sensor_data)
        accuracy_median = evaluate_accuracy(true_humidity, median_result)
        print(f"Wynik głosowania medianowego: {median_result}, Poprawność: {accuracy_median:.2f}%")

        median_voting_results.append(median_result)

        # Smoothing voter
        voter_threshold = 0.7
        smoothing_threshold = 2.0

        smoothing_result = smoothing_voter(sensor_data, prev_smoothing_voter_output, voter_threshold, smoothing_threshold)
        if smoothing_result is None:
            print("Smothing voter: No valid output")
        else:
            accuracy_smoothing = evaluate_accuracy(true_humidity, smoothing_result)
            print(f"Smothing voter: {smoothing_result}, Accuracy: {accuracy_smoothing:.2f}%")

        smoothing_voter_results.append(smoothing_result)
        prev_smoothing_voter_output = smoothing_result

        print("\n")

        time.sleep(1)
except KeyboardInterrupt:
    print("Simulation stopped by user")
    print("Median voting average accuracy:", average(median_voting_results))
    print("Smoothing voter average accuracy:", average(smoothing_voter_results))