"""
Digital signal waveform tool.
This tool draws signals of digital circuits for educational purposes.
author: Binh Tran Thanh / email:thanhbinh.hcmut@gmail.com or thanhbinh@hcmut.edu.vn 
"""

import enum
import numpy as np
from configuration import *


class Signal:
    class SignalType(enum.Enum):
        clk = 0
        data = 1

    def __init__(self, name='clk', signal_width=1, clk_frequency=1, signal_type=SignalType.data):
        self.set_name(name=name)
        self.signal_width = signal_width
        self.signal_type = signal_type
        self.clk_frequency = clk_frequency
        self.wf_data = np.zeros((1, 2))

    @staticmethod
    def invert(x):
        return int(not x)

    def print_data(self):
        print(f'signal name {self.name}')
        print(f'_wareform_data: {self.wf_data}')

    def set_name(self, name):
        self.name = name

    def set_frequency(self, f):
        if self.signal_type == Signal.SignalType.clk:
            self.clk_frequency = f

    def generate_clk(self, max_time=12):
        self.wf_data = np.zeros((1, 2))
        current_level = 0
        f = self.clk_frequency
        for i in range(100):
            last = self.wf_data[-1]
            if last[0] >= max_time:
                break
            current_level = self.invert(current_level)
            new = last[0], current_level * signal_height
            new1 = last[0] + f / 2, current_level * signal_height
            current_level = self.invert(current_level)
            new2 = last[0] + f / 2, current_level * signal_height
            new3 = last[0] + f, current_level * signal_height
            self.wf_data = np.vstack((self.wf_data, new, new1, new2, new3))

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def set_data_at_time(self, time, data):
        if self.is_number(data):
            indata = data
        else:
            indata = float('inf')
        if time == 0:
            self.wf_data[0][1] = indata
        else:
            self.wf_data = np.vstack((self.wf_data, (time, indata)))
            self.wf_data = self.wf_data[np.argsort(self.wf_data[:, 0])]

    def set_signal_width(self, signal_width):
        self.signal_width = signal_width


class Waveform:
    def __init__(self, finish_time=10):
        self.finish_time = finish_time
        self.signals = []
        self.height = 1.5

    def set_finish_time(self, finish_time=10):
        self.finish_time = finish_time

    def add_signal(self, signal: Signal):
        self.signals.append(signal)
        self.set_height()

    def set_height(self):
        self.height = len(self.signals) * waveform_hspace
