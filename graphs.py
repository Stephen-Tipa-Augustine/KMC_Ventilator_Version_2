## Filename: main.py
import math
import threading
import time
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from kivy.properties import ObjectProperty

from kivy.garden.graph import Graph, LinePlot

NUMBER_OF_POINTS = 20
VOLUME_Y_LIMITS = 0, 2
PRESSURE_Y_LIMITS = 0, 2
FLOW_Y_LIMITS = 0, 2


class Chart(MDBoxLayout):
    volume_graph = ObjectProperty(
        defaultvalue=Graph(xlabel='Time (s)', ylabel='Volume (ml)', x_ticks_minor=1,
                           x_ticks_major=1, y_ticks_major=1,
                           y_grid_label=True, x_grid_label=True, padding=5,
                           xmin=0, xmax=50, ymin=VOLUME_Y_LIMITS[0], ymax=VOLUME_Y_LIMITS[1])
    )
    pressure_graph = ObjectProperty(
        defaultvalue=Graph(xlabel='Time (s)', ylabel='Pressure (cm H20)', x_ticks_minor=1,
                           x_ticks_major=1, y_ticks_major=1,
                           y_grid_label=True, x_grid_label=True, padding=5,
                           xmin=0, xmax=50, ymin=PRESSURE_Y_LIMITS[0],
                           ymax=PRESSURE_Y_LIMITS[1])
    )
    flow_graph = ObjectProperty(
        defaultvalue=Graph(xlabel='Time (s)', ylabel='Flow (l/min)', x_ticks_minor=1,
                           x_ticks_major=1, y_ticks_major=1,
                           y_grid_label=True, x_grid_label=True, padding=5,
                           xmin=0, xmax=50, ymin=FLOW_Y_LIMITS[0], ymax=FLOW_Y_LIMITS[1])
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.plot_pressure = LinePlot(color=[1, 0, 0, 1], line_width=2)
        self.plot_flow = LinePlot(color=[1, 0, 0, 1], line_width=2)
        self.plot_volume = LinePlot(color=[1, 0, 0, 1], line_width=2)
        self.data = {'time': [], 'pressure': [], 'flow': [], 'volume': []}
        threading.Thread(target=self.generate_data, daemon=True).start()
        self.start()

    def start(self):
        self.pressure_graph.add_plot(self.plot_pressure)
        self.flow_graph.add_plot(self.plot_flow)
        self.volume_graph.add_plot(self.plot_volume)
        self.add_widget(self.pressure_graph)
        self.add_widget(self.flow_graph)
        self.add_widget(self.volume_graph)
        # Clock.schedule_interval(self.get_value, 0.05)
        threading.Thread(target=self.get_value, args=(0.05, ), daemon=True).start()

    def stop(self):
        Clock.unschedule(self.get_value)

    def get_value(self, delay=.05):
        while True:
            self.update_axis()
            self.plot_pressure.points = [(x, self.data['pressure'][i]) for i, x in enumerate(self.data['time'])]
            self.plot_flow.points = [(x, self.data['flow'][i]) for i, x in enumerate(self.data['time'])]
            self.plot_volume.points = [(x, self.data['volume'][i]) for i, x in enumerate(self.data['time'])]

            # Make the program sleep before resuming the iteration
            time.sleep(delay)

    def update_axis(self, *args):
        # Modifying the x-axis
        if len(self.data['time']) == NUMBER_OF_POINTS:
            self.pressure_graph.xmin = self.data['time'][0]
            self.pressure_graph.xmax = self.data['time'][-1]
            self.flow_graph.xmin = self.data['time'][0]
            self.flow_graph.xmax = self.data['time'][-1]
            self.volume_graph.xmin = self.data['time'][0]
            self.volume_graph.xmax = self.data['time'][-1]

        # Modifying the y-axis
        if max(self.data['pressure']) >= PRESSURE_Y_LIMITS[1]:
            self.pressure_graph.ymax = max(self.data['pressure']) + 1
        if max(self.data['flow']) >= FLOW_Y_LIMITS[1]:
            self.flow_graph.ymax = max(self.data['flow']) + 1
        if max(self.data['volume']) >= VOLUME_Y_LIMITS[1]:
            self.volume_graph.ymax = max(self.data['volume']) + 1

    def generate_data(self):
        x = -10
        while True:
            if ((x - (x % 10))/10) % 2 == 0:
                current_pressure_value = self.triangular_wave(t=x,period=2,scale=1,duty_cycle=.5)
                current_flow_value = self.triangular_wave(t=x,period=2,scale=1,duty_cycle=.2)
                current_volume_value = self.triangular_wave(t=x,period=2,scale=4,duty_cycle=.6)
            else:
                current_pressure_value = self.triangular_wave(t=x, period=2, scale=1, duty_cycle=.5)
                current_flow_value = self.triangular_wave(t=x, period=2, scale=2, duty_cycle=.2)
                current_volume_value = self.triangular_wave(t=x, period=2, scale=1, duty_cycle=.6)
            if len(self.data['time']) == NUMBER_OF_POINTS:
                for data in self.data:  # deleting the first elements to keep the number of elements constant
                    del self.data[data][0]

            self.data['pressure'].append(current_pressure_value)
            self.data['flow'].append(current_flow_value)
            self.data['volume'].append(current_volume_value)
            self.data['time'].append(x)

            x += .2  # Incrementing the horizontal axis or the time axis
            time.sleep(.1)

    @staticmethod
    def triangular_wave(t, period, scale=1, duty_cycle=.5):
        actual_time = t % period
        if actual_time <= duty_cycle * period:
            return scale * actual_time
        else:
            return 0
