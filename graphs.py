## Filename: main.py
import math
import threading
import time
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
import numpy as np

from kivy.garden.graph import Graph, LinePlot


NUMBEROFPOINTS = 20


class Chart(MDBoxLayout):
    volume_graph = Graph(xlabel='time', ylabel='volume', x_ticks_minor=1,
                       x_ticks_major=5, y_ticks_major=1,
                       y_grid_label=True, x_grid_label=True, padding=5,
                       x_grid=True, y_grid=True, xmin=0, xmax=50, ymin=-1, ymax=1)
    pressure_graph = Graph(xlabel='time', ylabel='pressure', x_ticks_minor=1,
                         x_ticks_major=5, y_ticks_major=1,
                         y_grid_label=True, x_grid_label=True, padding=5,
                         x_grid=True, y_grid=True, xmin=0, xmax=50, ymin=-1, ymax=1)
    flow_graph = Graph(xlabel='time', ylabel='flow', x_ticks_minor=1,
                         x_ticks_major=5, y_ticks_major=1,
                         y_grid_label=True, x_grid_label=True, padding=5,
                         x_grid=True, y_grid=True, xmin=0, xmax=50, ymin=-1, ymax=1)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.plot_pressure = LinePlot(color=[1, 0, 0, 1], line_width=2)
        self.plot_flow = LinePlot(color=[1, 0, 0, 1], line_width=2)
        self.plot_volume = LinePlot(color=[1, 0, 0, 1], line_width=2)
        self.data = {'time':[], 'pressure':[], 'flow':[], 'volume':[]}
        threading.Thread(target=self.generate_data, daemon=True).start()
        self.start()

    def start(self):
        self.pressure_graph.add_plot(self.plot_pressure)
        self.flow_graph.add_plot(self.plot_flow)
        self.volume_graph.add_plot(self.plot_volume)
        self.add_widget(self.pressure_graph)
        self.add_widget(self.flow_graph)
        self.add_widget(self.volume_graph)
        Clock.schedule_interval(self.get_value, 0.05)

    def stop(self):
        Clock.unschedule(self.get_value)

    def get_value(self, dt):
        self.update_axis()
        self.plot_pressure.points = [(x, self.data['pressure'][i]) for i, x in enumerate(self.data['time'])]
        self.plot_flow.points = [(x, self.data['flow'][i]) for i, x in enumerate(self.data['time'])]
        self.plot_volume.points = [(x, self.data['volume'][i]) for i, x in enumerate(self.data['time'])]

    def update_axis(self, *args):
        if len(self.data['time']) == NUMBEROFPOINTS:
            self.pressure_graph.xmin = self.data['time'][0]
            self.pressure_graph.xmax = self.data['time'][-1]
            self.flow_graph.xmin = self.data['time'][0]
            self.flow_graph.xmax = self.data['time'][-1]
            self.volume_graph.xmin = self.data['time'][0]
            self.volume_graph.xmax = self.data['time'][-1]

    def generate_data(self):
        x = -10
        while True:
            current_pressure_value = math.cos(x)
            current_flow_value = math.sin(x)
            current_volume_value = -math.cos(x)
            if len(self.data['time']) == NUMBEROFPOINTS:
                for data in self.data:                  # deleting the first elements to keep the number of elements constant
                    del self.data[data][0]

            self.data['pressure'].append(current_pressure_value)
            self.data['flow'].append(current_flow_value)
            self.data['volume'].append(current_volume_value)
            self.data['time'].append(x)

            x += 1                  # Incrementing the horizontal axis or the time axis
            time.sleep(.1)