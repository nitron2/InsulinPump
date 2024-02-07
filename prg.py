# prg is the main part of the software that runs in a loop to simulate everything.

import PySimpleGUI as psg
import settings
from Blood import Blood
from InsulinPump import InsulinPump


# Update the "Auto-run" Text Button  text based on auto-run status of prg.
def update_auto_run_text(auto_run, window):
    if auto_run:
        window["AutoRun"].update("AUTORUN: YES")
    else:
        window["AutoRun"].update("AUTORUN: NO")


# Update the text for the alarm indicator
def update_alarm_text(alarm, window):
    if alarm:
        window["Alarm"].update("ALARM: ARMED")
    else:
        window["Alarm"].update("ALARM: DISABLED")


# Logic for making program automatically run or not.
def get_timeout_based_on_auto_run(auto_run):
    if auto_run:
        return settings.TIME_BETWEEN_FRAMES_MS
    return None


# Update all gui states at once.
def update_gui(window, blood):
    window["Image"].update(filename='blood_graph.png')
    window["Insulin"].update(str(round(blood.get_insulin(), 2)) + " UNITS")
    window["Glucose"].update(str(round(blood.get_glucose(), 2)) + " mg/dL")
    window["PumpPower"].update(str(pump.power_state))
    window["Battery"].update(str(round((pump.battery_voltage / settings.BATTERY_CAPACITY_MAX_VOLTAGE) * 100)) + "%")
    update_auto_run_text(auto_run, window)
    update_alarm_text(alarm, window)


# Main loop to simulate everything
if __name__ == "__main__":
    # Initializing all variables
    # PySimpleGui offers many themes and layout options. Set those here.
    psg.theme('Reddit')
    layout = [[psg.Text('PUMP POWER.......................................................................'),
               psg.Text(key="PumpPower", text=settings.INSULIN_PUMP_DEFAULT_POWER_STATE)],
              [psg.Text('BATTERY...............................................................................'),
               psg.Text(key="Battery", text="0")],
              [psg.Text('INSULIN IN BLOODSTREAM:................................................'),
               psg.Text(key="Insulin", text="0")],
              [psg.Text('GLUCOSE.............................................................................'),
               psg.Text(key="Glucose", text="0")],
              [psg.Image(key="Image", filename='blood_graph.png')],
              [psg.Button(key="On", button_text='ON'), psg.Button(key="Off", button_text="OFF"),
               psg.Button(button_text="ADVANCE"), psg.Button(key="AutoRun", button_text="AUTORUN"),
               psg.Button(key="Alarm", button_text="ALARM")]]
    # UI pop up here
    window = psg.Window('Insulin Pump Simulation', layout)
    pump = InsulinPump()
    blood = Blood()
    auto_run = settings.AUTO_ADVANCE_ANIMATION
    alarm = settings.ALARM_ENABLED
    timeout = get_timeout_based_on_auto_run(auto_run)

    # Main loop to simulate the problem
    # All button logic is below:
    while True:
        event, values = window.read(
            timeout=timeout)  # ms to wait until the Read will return IF no other GUI events happen first If timout is None, then don't automatically run
        if event == psg.WIN_CLOSED:  # if user closes window or clicks cancel
            break
        if event == 'On':
            pump.turn_on()
        if event == 'Off':
            pump.turn_off()
        if event == 'AutoRun':
            if auto_run:
                auto_run = False
            else:
                auto_run = True
            timeout = get_timeout_based_on_auto_run(auto_run)
        if event == 'Alarm':
            if alarm:
                alarm = False
                pump.set_alarm(False)
            else:
                alarm = True
                pump.set_alarm(True)

        # Run the blood and pump and update gui every frame.
        blood.run()
        pump.run(blood)
        update_gui(window, blood)

    window.close()
