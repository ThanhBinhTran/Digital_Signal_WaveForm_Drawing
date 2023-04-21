"""
Digital signal waveform tool.
This tool draws signals of digital circuits for educational purposes.
author: Binh Tran Thanh / email:thanhbinh.hcmut@gmail.com or thanhbinh@hcmut.edu.vn 
"""

import matplotlib.pyplot as plt
import numpy as np

from configuration import *
from waveform import Waveform, Signal


def format_wf(data, radix='h'):
    if data == float('inf'):
        wf_data = 'xxx'
    else:
        if radix == 'h':
            wf_data = hex(int(data))
        elif radix == 'b':
            wf_data = bin(data)
        else:
            wf_data = int(data)
    return wf_data


class Plot_base:
    def __init__(self, size=(6, 6), title="Digital system circuit waveform"):
        self.plt = plt
        self.fig, self.ax = plt.subplots(figsize=size)
        self.fig.canvas.manager.set_window_title(title)
        self.set_equal()
        self.plt.grid(False)
        self.plt.axis("off")  # turns off axes
        # self.plt.axis("tight")  # gets rid of white border

    show = lambda self: self.plt.show()
    pause = lambda self, x: self.plt.pause(x)
    clear = lambda self: self.plt.cla()
    set_equal = lambda self: self.plt.axis("equal")
    show_grid = lambda self: self.plt.grid(True)
    set_axis = lambda self, x0, y0, x1, y1: self.plt.axis([x0, x1, y0, y1])

    ''' plot point(s)'''
    point = lambda self, point, ls=".r": self.plt.plot(point[0], point[1], ls)
    points = lambda self, points, ls=".r": self.plt.plot(points[:, 0], points[:, 1], ls)

    @staticmethod
    def wform_bus(start, end, y_offset):
        line = np.array([(start, signal_height / 2), (start + 0.1, signal_height), (end - 0.1, signal_height),
                         (end, signal_height / 2), (end - 0.1, 0), (start + 0.1, 0), (start, signal_height / 2)])
        return line + (0, y_offset)

    @staticmethod
    def wform_wire(start, end, y_offset, data):
        if data:
            line = np.array([(start, 0), (start, signal_height), (end, signal_height)])
        else:
            line = np.array([(start, signal_height), (start, 0), (end, 0)])
        return line + (0, y_offset)

    @staticmethod
    def wform_retangle(start, end, y_offset):
        line = np.array([(start, 0), (start, signal_height), (end, signal_height), (end, 0), (start, 0)])
        return line + (0, y_offset)

    def plot_text(self, x=0, y=0, text='text', horizontal_alignment='center'):
        self.plt.text(x, y, text, verticalalignment='bottom', horizontalalignment=horizontal_alignment)

    def plot_name_and_initial(self, name='clk', y_offset=0):
        offset = y_offset + text_y_offset
        wf_shape = self.wform_retangle(start=initial_space_len, end=0, y_offset=y_offset)
        # display name
        self.plot_text(x=initial_space_len - 0.1, y=offset, text=name, horizontal_alignment='right')

        # display don't care value
        self.plt.fill(wf_shape[:, 0], wf_shape[:, 1], color='k', alpha=0.3)
        self.plot_text(x=initial_space_len / 2, y=offset, text='xxx')

    def plot_clk(self, signal=None, ls='-', y_offset=0, lw=0.5, color='k'):
        clk_draw = signal.wf_data + (0, y_offset)
        self.plt.plot(clk_draw[:, 0], clk_draw[:, 1], ls=ls, c=color, lw=lw)

    def plot_datasignal(self, signal: Signal, finish_time=100, y_offset=5, color='b', num_radix='h', lw=0.5,
                        fillcolor=None):
        for i in range(len(signal.wf_data)):
            start = signal.wf_data[i][0]
            data = signal.wf_data[i][1]
            if i == len(signal.wf_data) - 1:
                end = finish_time
            else:
                end = signal.wf_data[i + 1][0]

            wf_data = format_wf(data=data, radix=num_radix)

            if signal.signal_width > 1:
                wf_shape = self.wform_bus(start=start, end=end, y_offset=y_offset)
                self.plot_text(x=(start + end) / 2, y=y_offset + text_y_offset, text=wf_data)
                if fillcolor is not None:
                    self.plt.fill(wf_shape[:, 0], wf_shape[:, 1], color=fillcolor, alpha=0.3)
            else:
                if wf_data == 'xxx':
                    wf_shape = self.wform_retangle(start=start, end=end, y_offset=y_offset)
                    self.plot_text(x=(start + end) / 2, y=y_offset + text_y_offset, text=wf_data)
                    self.plt.fill(wf_shape[:, 0], wf_shape[:, 1], color=fillcolor, alpha=0.3)
                else:
                    wf_shape = self.wform_wire(start=start, end=end, y_offset=y_offset, data=data)
            self.plt.plot(wf_shape[:, 0], wf_shape[:, 1], c=color, lw=lw)

    def plot_time_stamp(self, time_stamp, height=5, label='$t$', lw=0.2):
        tstamp = np.array([(0, 0), (0, height + 0.5)])
        tstamp = tstamp + (time_stamp, 0)
        self.plt.plot(tstamp[:, 0], tstamp[:, 1], ':k', lw=lw)
        self.plt.text(tstamp[1][0], tstamp[1][1], label)

    def plot_time_stamps(self, f, height=5, lw=0.2, maxtime=12):
        tstick = np.array([(0, 0),
                           (0, height + 0.5)])
        transit = np.array((f, 0))
        for i in range(100):
            ts_line = tstick + i * transit
            if ts_line[0][0] > maxtime:
                break
            ts_label = '$t_{' + str(i*f) + '}$'
            self.plot_time_stamp(time_stamp=i * f, height=height, label=ts_label)

    def plot_waveform(self, waveform: Waveform):
        for idx, signal in enumerate(waveform.signals):
            # signal.print_data()
            y_offset = idx * waveform_hspace
            self.plot_name_and_initial(name=signal.name, y_offset=y_offset)
            if signal.signal_type == Signal.SignalType.clk:
                self.plot_clk(signal=signal, ls='-', y_offset=y_offset)
            else:
                self.plot_datasignal(signal=signal, y_offset=y_offset, finish_time=waveform.finish_time, fillcolor='g')
    
    def save_figure(self, fig_name="image", file_extension=".png", dpi=150):
            full_path = fig_name + file_extension
            self.plt.axis("off")   # turns off axes
            self.plt.axis("tight")  # gets rid of white border
            self.plt.savefig(full_path, bbox_inches="tight", dpi=dpi)
            print(f"saved: {full_path}")