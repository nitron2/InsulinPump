import settings
import numpy as np
import PySimpleGUI as psg


# Only fires if alarm is on
def safety_check(blood):
    if blood.get_glucose() < settings.BLOOD_GLUCOSE_LOW_BOUNDARY:
        psg.popup('WARNING!', 'GLUCOSE < 100 mg/dL. EAT SOMETHING IMMEDIATELY.')


class InsulinPump:

    # Set all attributes
    def __init__(self):
        self.battery_voltage = settings.BATTERY_CAPACITY_MAX_VOLTAGE
        self.alarm = settings.ALARM_ENABLED
        self.power_state = settings.INSULIN_PUMP_DEFAULT_POWER_STATE
        self.glucose_accelerations = []

    # Main simulation frame method here
    def run(self, blood):
        if self.power_state:
            self.battery_check()
            if self.alarm:
                safety_check(blood)
            self.compute_injection(blood)

    def turn_on(self):
        self.power_state = True

    def turn_off(self):
        self.power_state = False

    def set_alarm(self, alarm):
        self.alarm = alarm

    # Fulfills project insulting injection requirement.
    # Computed injection found by getting current blood glucose acceleration and finding out what that is as a percent
    # of the average acceleration. Very Complicated. I don't really know how this works exactly, it mutated. One of those
    # funny software engineering monsters.
    # TODO: Does it make sense that blood is capable of telling the pump its acceleration? No. Change this to be
    #  computing only the pump.
    def compute_injection(self, blood):
        self.drain_battery(settings.INSULIN_CHECK_BATTERY_TOLL_VOLTAGE)
        if blood.get_glucose() > settings.BLOOD_GLUCOSE_HIGH_BOUNDARY:
            glucose_acceleration = blood.get_blood_glucose_acceleration()
            self.glucose_accelerations.append(glucose_acceleration)
            if glucose_acceleration > 0:
                percent_power = np.abs(glucose_acceleration / self.get_average_glucose_acceleration())
                self.drain_battery(settings.INSULIN_INJECT_BATTERY_TOLL_VOLTAGE)
                blood.on_insulin_injected(percent_power * settings.STANDARD_INSULIN_DOSE_UNITS)
            if glucose_acceleration == 0:
                self.drain_battery(settings.INSULIN_INJECT_BATTERY_TOLL_VOLTAGE)
                blood.on_insulin_injected(settings.STANDARD_INSULIN_DOSE_UNITS)

    def get_average_glucose_acceleration(self):
        return sum(self.glucose_accelerations) / len(self.glucose_accelerations)

    def drain_battery(self, voltage_to_drain):
        new_voltage = self.battery_voltage - voltage_to_drain
        if new_voltage <= settings.BATTERY_CAPACITY_MIN_VOLTAGE:
            new_voltage = settings.BLOOD_GLUCOSE_MIN
        self.battery_voltage = new_voltage

    def battery_check(self):
        if (self.get_battery_voltage() / settings.BATTERY_CAPACITY_MAX_VOLTAGE) <= settings.BATTERY_PERCENT_LOW_WARNING:
            self.replace_battery()
            psg.popup('WARNING!', 'BATTERY LOW. REPLACE BATTERY.')

    def replace_battery(self):
        self.battery_voltage = settings.BATTERY_CAPACITY_MAX_VOLTAGE

    def get_battery_voltage(self):
        return self.battery_voltage
