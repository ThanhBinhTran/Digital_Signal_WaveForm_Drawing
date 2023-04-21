"""
Digital signal waveform tool.
This tool draws signals of digital circuits for educational purposes.
author: Binh Tran Thanh / email:thanhbinh.hcmut@gmail.com or thanhbinh@hcmut.edu.vn 
"""

from plotter import *

if __name__ == '__main__':
    waveforms = Waveform()

    # declare and prepare signals
    clk = Signal(name='clk', signal_type=Signal.SignalType.clk, clk_frequency=1)
    clk.generate_clk(max_time=waveforms.finish_time)

    data = Signal(name='data_in', signal_type=Signal.SignalType.data, signal_width=8)
    data1 = Signal(name='write_en', signal_type=Signal.SignalType.data, signal_width=1)
    data2 = Signal(name='reset', signal_type=Signal.SignalType.data, signal_width=1)
    
    data.set_data_at_time(time=0, data=54)
    data.set_data_at_time(time=2, data=10)
    data.set_data_at_time(time=6, data=90)
    data.set_data_at_time(time=9, data='x')
    data.set_data_at_time(time=3.2, data=23)

    data1.set_data_at_time(time=3.1, data=1)
    data1.set_data_at_time(time=5.7, data=0)
    data1.set_data_at_time(time=7.1, data=1)
    data1.set_data_at_time(time=9.1, data='x')

    data2.set_data_at_time(time=0.2, data=1)
    data2.set_data_at_time(time=1.2, data=0)

    # add signal to waveform
    waveforms.add_signal(clk)
    waveforms.add_signal(data)
    waveforms.add_signal(data2)
    waveforms.add_signal(data1)

    plotter = Plot_base(size=(7, 3), title='circuit waveform')

    plotter.plot_waveform(waveform=waveforms)
    plotter.plot_time_stamps(f=clk.clk_frequency, height=waveforms.height, maxtime=waveforms.finish_time)
    time_stick = 5.6
    plotter.plot_time_stamp(time_stamp=time_stick, height=waveforms.height + 0.2, label='$t_{' + str(time_stick) + '}$', lw=1)
    
    # save image 
    save_img = False
    if save_img:
        #file_extension='.pdf'
        #file_extension='.pdf'
        file_extension='.png'
        plotter.save_figure(fig_name='wf_img',file_extension=file_extension)
    else:
        plotter.show()
