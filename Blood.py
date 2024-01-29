import math

import settings
import numpy as np
import matplotlib.pyplot as plt

class Blood:
    minute = 0
    glucose_measurements = []
    minutes = []
    glucose = 0
    insulin = 0

    # Instance attribute
    def __init__(self, glucose=settings.DEFAULT_BLOOD_GLUCOSE, insulin=settings.DEFAULT_BLOOD_INSULIN):
        self.glucose = glucose
        self.insulin = insulin

    def run(self):
        self.glucose = self.get_next_blood_glucose()
        self.glucose_measurements.append(self.glucose)
        self.minutes.append(self.minute)
        plt.plot(self.minutes, self.glucose_measurements)  # Plot the chart
        plt.axline((0, settings.BLOOD_GLUCOSE_LOW_BOUNDARY), (1, settings.BLOOD_GLUCOSE_LOW_BOUNDARY), linewidth=2, color='r')
        plt.axline((0, settings.BLOOD_GLUCOSE_HIGH_BOUNDARY), (1, settings.BLOOD_GLUCOSE_HIGH_BOUNDARY), linewidth=2, color='g')
        plt.savefig('blood_graph.png')
        self.minute = self.minute + 10
        if self.insulin - settings.INSULIN_BLEED < 0 or self.insulin == 0:
            self.insulin = 0
        else:
            self.insulin = self.insulin - settings.INSULIN_BLEED

    def get_next_blood_glucose(self):
        anomaly = np.random.choice([True, False], p=[settings.PROBABILITY_OF_BLOOD_GLUCOSE_ANOMALY, 1 - settings.PROBABILITY_OF_BLOOD_GLUCOSE_ANOMALY])
        if anomaly:
            glucose = np.random.choice(np.arange(settings.BLOOD_GLUCOSE_MIN, settings.BLOOD_GLUCOSE_MAX))
            return glucose
        else:
            position_of_blood_insulin_rounded_in_reference_array = settings.BLOOD_INSULIN_LEVEL_REFERENCE.index(math.ceil(self.insulin))
            probability_blood_glucose_down = settings.PROBABILITY_OF_BLOOD_GLUCOSE_DECREASE_REFERENCE[position_of_blood_insulin_rounded_in_reference_array]
            glucose_down = np.random.choice([True, False], p=[probability_blood_glucose_down, 1 - probability_blood_glucose_down])
            if glucose_down:
                if self.glucose - settings.TYPICAL_BLOOD_GLUCOSE_VARIATION < settings.BLOOD_GLUCOSE_MIN or self.glucose == settings.BLOOD_GLUCOSE_MIN:
                    lower_number = settings.BLOOD_GLUCOSE_MIN
                else:
                    lower_number = self.glucose - settings.TYPICAL_BLOOD_GLUCOSE_VARIATION
                blood_glucose_change_window = np.arange(lower_number, self.glucose + 1)
            else:
                if self.glucose + settings.TYPICAL_BLOOD_GLUCOSE_VARIATION > settings.BLOOD_GLUCOSE_MAX or self.glucose == settings.BLOOD_GLUCOSE_MAX:
                    higher_number = settings.BLOOD_GLUCOSE_MAX
                else:
                    higher_number = self.glucose + settings.TYPICAL_BLOOD_GLUCOSE_VARIATION
                blood_glucose_change_window = np.arange(self.glucose, higher_number)
            glucose = np.random.choice(blood_glucose_change_window)
            return glucose

    def get_glucose(self):
        return self.glucose

    def get_insulin(self):
        return self.insulin

    def get_blood_glucose_acceleration(self, time_interval_minutes=10):
        if len(self.glucose_measurements) >= 3:
            vf = (self.glucose_measurements[-1] - self.glucose_measurements[-2]) / time_interval_minutes
            vi = (self.glucose_measurements[-2] - self.glucose_measurements[-3]) / time_interval_minutes
            #print("Glucose[-1]: " + str(self.glucose_measurements[-1]))
            #print("Glucose[-2]: " + str(self.glucose_measurements[-2]))
            #print("vi: " + str(vi))
            #print("vf: " + str(vf))
            return (vf - vi) / time_interval_minutes
        return 0

    def on_insulin_injected(self, amount):
        if self.insulin + amount > settings.BLOOD_INSULIN_LEVEL_REFERENCE[-1] or self.insulin == settings.BLOOD_INSULIN_LEVEL_REFERENCE[-1]:
            self.insulin = settings.BLOOD_INSULIN_LEVEL_REFERENCE[-1]
        else:
            self.insulin = self.insulin + amount
