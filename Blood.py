import math

import settings
import numpy as np
import matplotlib.pyplot as plt


class Blood:

    # Set instance attributes
    def __init__(self, glucose=settings.DEFAULT_BLOOD_GLUCOSE, insulin=settings.DEFAULT_BLOOD_INSULIN):
        self.glucose = glucose
        self.insulin = insulin
        self.minute = 0
        self.glucose_measurements = []
        self.minutes = []

    # Iteratively run every simulation frame.
    def run(self):
        self.glucose = self.get_next_blood_glucose()
        self.glucose_measurements.append(self.glucose)
        self.minutes.append(self.minute)
        self.save_line_graph_of_blood_glucose_png()
        self.metabolize_insulin()
        self.minute = self.minute + 10

    # Per project requirements, the blood lgucose has a random component, but operates by having a "next glucose reading"
    # that is adjecent to the current one. So, the glucose follows a trend.
    def get_next_blood_glucose(self):
        anomaly = np.random.choice([True, False], p=[settings.PROBABILITY_OF_BLOOD_GLUCOSE_ANOMALY,
                                                     1 - settings.PROBABILITY_OF_BLOOD_GLUCOSE_ANOMALY])
        if anomaly:
            glucose = np.random.choice(np.arange(settings.BLOOD_GLUCOSE_MIN, settings.BLOOD_GLUCOSE_MAX))
            return glucose

        # Using two reference arrays, one with insulin value possibilities corresponding to another array with
        # probabilities of glucose going down with a given blood insulin amount,
        position_of_blood_insulin_rounded_in_reference_array = settings.BLOOD_INSULIN_LEVEL_REFERENCE.index(
            math.ceil(self.insulin))
        probability_blood_glucose_down = settings.PROBABILITY_OF_BLOOD_GLUCOSE_DECREASE_REFERENCE[
            position_of_blood_insulin_rounded_in_reference_array]
        glucose_down = np.random.choice([True, False],
                                        p=[probability_blood_glucose_down, 1 - probability_blood_glucose_down])
        # Now that we have chosen glucose up or down, we choose a new glucose, going either up or down within a window.
        if glucose_down:
            blood_glucose_change_window = np.arange(
                max(settings.BLOOD_GLUCOSE_MIN, self.glucose - settings.TYPICAL_BLOOD_GLUCOSE_VARIATION), self.glucose)
        # Case: glucose up
        else:
            blood_glucose_change_window = np.arange(self.glucose, min(settings.BLOOD_GLUCOSE_MAX,
                                                                      self.glucose + settings.TYPICAL_BLOOD_GLUCOSE_VARIATION))
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
            return (vf - vi) / time_interval_minutes
        return 0

    def on_insulin_injected(self, amount):
        if self.insulin + amount > settings.BLOOD_INSULIN_LEVEL_REFERENCE[-1] or self.insulin == \
                settings.BLOOD_INSULIN_LEVEL_REFERENCE[-1]:
            self.insulin = settings.BLOOD_INSULIN_LEVEL_REFERENCE[-1]
        else:
            self.insulin = self.insulin + amount

    def metabolize_insulin(self):
        if self.insulin - settings.INSULIN_UNITS_METABOLIZED_PER_10_MIN < 0 or self.insulin == 0:
            self.insulin = 0
        else:
            self.insulin = self.insulin - settings.INSULIN_UNITS_METABOLIZED_PER_10_MIN

    # Purely Visual
    def save_line_graph_of_blood_glucose_png(self):
        plt.plot(self.minutes, self.glucose_measurements)  # Plot the chart
        plt.axline((0, settings.BLOOD_GLUCOSE_LOW_BOUNDARY), (1, settings.BLOOD_GLUCOSE_LOW_BOUNDARY), linewidth=1,
                   color='r')
        plt.axline((0, settings.BLOOD_GLUCOSE_HIGH_BOUNDARY), (1, settings.BLOOD_GLUCOSE_HIGH_BOUNDARY), linewidth=1,
                   color='g')
        plt.xlabel('Time (min)')
        plt.ylabel('Blood Glucose (mg/dL)')
        plt.savefig('blood_graph.png')
