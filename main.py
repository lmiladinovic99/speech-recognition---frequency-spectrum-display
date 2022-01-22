from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

window_function = 0
window_size = 480
path = ""
samplerate = 0
data = []
data2 = []
T = []
words_list = []

def openFile():
    global path
    filepath = askopenfilename(filetypes=[("Wav files", "*.wav")])
    path = filepath
    #print(path)

def loadFile(path):
    samplerate, data = wavfile.read(path)
    dataTmp = 0
    if data.shape == (len(data), 2):
        #print(dataTmp)
        dataTmp = data.sum(axis=1) / 2
        data = dataTmp
    #print(data.shape, " ", samplerate)
    T = [i / samplerate for i in range(0, len(data))]
    plt.style.use('ggplot')
    return samplerate, data, T

def noise_avg(data, samplerate):
    win_num = 0
    sum = 0
    while win_num < 0.1 * samplerate:
        sum += abs(data[win_num])
        win_num += 1
    std = np.std(abs(data[:int(0.1*samplerate)]))
    L = sum / (0.1*samplerate) + 2*std
    #print("sum ", sum)
    #print("bound*sr", bound*samplerate)
    #print("std ", std)
    #print(L)
    return L

def endpoint(win_size, data, L):
    words_list = []
    index = 0
    check = 0
    for i in data:
        if index == win_size:
            check = check / win_size
            #print(check, " " , L)
            if check < L:
                words_list.append(0)
            else:
                words_list.append(1)
            index = 0
            check = 0
        check += abs(i)
        index += 1
    return words_list

def flattenup(p, words_list):
    curr_len = 0
    index = 0
    for i in words_list:
        if i == 0:
            curr_len += 1
        else:
            if p > curr_len > 0:
                for j in range(index-curr_len, index):
                    words_list[j] = 1
            curr_len = 0
        index += 1

def flattendown(q, words_list):
    curr_len = 0
    index = 0
    for i in words_list:
        if i == 1:
            curr_len += 1
        else:
            if q > curr_len > 0:
                for j in range(index-curr_len, index):
                    words_list[j] = 0
            curr_len = 0
        index += 1

def cut(words, data, win_size, T):
    begin = words.index(1) - 1
    end = len(words) - words[::-1].index(1)
    #print(begin, " ", end)
    data2 = data[begin * win_size: end * win_size]
    f = plt.figure(111)
    plt.plot(T[::], data[::], 'b')
    plt.axvline(x = T[begin*win_size], color = 'r')
    plt.axvline(x = T[end*win_size], color = 'r')
    f.show()
    return data2

def phase1(win_size):
    global samplerate
    global window_size
    global data
    global data2
    global T
    global words_list
    p = 6
    q = 6
    global path
    #print(path)
    try:
        samplerate, data, T = loadFile(path)
    except:
        messagebox.showinfo("Error", "File not loaded")
    window_size = int(win_size*samplerate*0.001)
    L = noise_avg(data, samplerate)
    words_list = endpoint(window_size, data, L)
    # if 1 not in words_list:
    #     print("error")
    #     messagebox.showinfo("Error", "File is noise")
    #     return
    #print(words_list)
    flattenup(p, words_list)
    flattendown(q, words_list)
    try:
        data2 = cut(words_list, data, window_size, T)
    except:
        messagebox.showinfo("Error", "File is noise")

def furije(y, N):
    y_temp = np.fft.fft(y)[0:int(N / 2)] / N
    y_temp[1:] = 2 * y_temp[1:]
    FFT_y = np.abs(y_temp)
    return FFT_y

def dft(data2, N):
    fft_data = []
    data_window = []
    i = 0
    while i < len(data2):
        if (len(data2) - i < N):
            data_window[i:] = data2[i:]
            if window_function == 1:
                data_window[i:] = data_window[i:] * np.bartlett(N)
            elif window_function == 2:
                data_window[i:] = data_window[i:] * np.hamming(N)
            elif window_function == 3:
                data_window[i:] = data_window[i:] * np.hanning(N)
            elif window_function == 4:
                data_window[i:] = data_window[i:] * np.blackman(N)
        else:
            data_window[i:i+N] = data2[i:i+N]
            if window_function == 1:
                data_window[i:i+N] = data_window[i:i+N] * np.bartlett(N)
            elif window_function == 2:
                data_window[i:i+N] = data_window[i:i+N] * np.hamming(N)
            elif window_function == 3:
                data_window[i:i+N] = data_window[i:i+N] * np.hanning(N)
            elif window_function == 4:
                data_window[i:i+N] = data_window[i:i+N] * np.blackman(N)
        i = i + N
    #fft_data = furije(data, N)
    fft_data_window = furije(data_window, N)
    fft_data_window = np.interp(fft_data_window, (fft_data_window.min(), fft_data_window.max()), (0, 100))
    #freq = samplerate*np.arange(N/2)/N;
    return fft_data_window

def histogram(data, N):
    if len(data) == 0:
        messagebox.showinfo("Error", "File not processed")
        return
    fft_data = dft(data, N)
    dw = 1
    w = np.linspace(0, N*dw-dw, N)
    h1 = abs(fft_data[0:N])
    h2 = np.flip(h1)
    h = np.append(h1, h2)
    f = plt.figure(10)
    plt.title("Histogram")
    plt.xlabel("Frekvencija")
    plt.ylabel("Magnituda")
    plt.bar(w, height=h, align='center', width=dw)
    f.show()

def histogramFull(data, N):
    if len(data) == 0:
        messagebox.showinfo("Error", "File not processed")
        return
    fft_data = dft(data, N)
    dw = 1
    w = np.linspace(0, len(data)*dw-dw, len(data))
    h1 = abs(fft_data[::])
    #print(h1)
    h2 = np.flip(h1)
    #print(h2)
    h = np.append(h1, h2)
    #print(len(w),' ', len(h))
    f = plt.figure(10)
    plt.title("Histogram")
    plt.xlabel("Frekvencija")
    plt.ylabel("Magnituda")
    plt.bar(w, height=h, align='center', width=dw)
    f.show()

def spectogram():
    if len(data) == 0:
        messagebox.showinfo("Error", "File not processed")
        return
    f = plt.figure(1)
    plt.title("Spectrogram")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency")
    plt.specgram(data, Fs=samplerate)
    try:
        begin = words_list.index(1) - 1
        end = len(words_list) - words_list[::-1].index(1)
        plt.axvline(x = T[begin*window_size], color = 'r')
        plt.axvline(x = T[end*window_size], color = 'r')
        f.show()
    except:
        messagebox.showinfo("Error", "File is noise")

def select_window_function(w_fun):
    global window_function
    window_function = int(w_fun.get())
    #print(window_function)

def begin():
    window = tk.Tk()
    window.geometry("600x200")
    window.title("PG_domaci1")

    win_size = tk.StringVar(value="10")
    w_fun = tk.IntVar()

    btn_load = tk.Button(window, text="Load File", command=openFile)

    label1 = tk.Label(window, text = "WINDOW SIZE (ms):")
    input = tk.Entry(window, text="win_size", width=10, textvariable=win_size)
    label2 = tk.Label(window, text = "SELECT A WINDOW FUNCTION:")

    empty = tk.Radiobutton(window, text="no function", value=0, variable=w_fun, command=lambda: select_window_function(w_fun))
    triangle = tk.Radiobutton(window, text="Triangle", value=1, variable=w_fun, command=lambda: select_window_function(w_fun))
    hamming = tk.Radiobutton(window, text="Hamming", value=2, variable=w_fun, command=lambda: select_window_function(w_fun))
    hanning = tk.Radiobutton(window, text="Hanning", value=3, variable=w_fun, command=lambda: select_window_function(w_fun))
    blackman = tk.Radiobutton(window, text="Blackman", value=4, variable=w_fun, command=lambda: select_window_function(w_fun))

    btn_cut = tk.Button(window, text="Cut Word", command=lambda: phase1(int(win_size.get())))
    btn_histogram = tk.Button(window, text="Histogram", command=lambda: histogram(data2, window_size))
    btn_histogram_full = tk.Button(window, text="Histogram Full", command=lambda: histogram(data2, window_size))
    btn_spectrogram = tk.Button(window, text="Spectrogram", command=lambda: spectogram())

    btn_load.grid(row=0, column=2, padx=(10,10), pady=(5,5))
    label1.grid(row=1, column=1, padx=(10,10), pady=(5,5))
    input.grid(row=1, column=2, padx=(10,10), pady=(5,5))
    label2.grid(row=2, column=1, padx=(10,10), pady=(10,0), columnspan=2)
    empty.grid(row=3, column=0, padx=(10,10), pady=(0,5))
    triangle.grid(row=3, column=1, padx=(10,10), pady=(0,5))
    hamming.grid(row=3, column=2, padx=(10,10), pady=(0,5))
    hanning.grid(row=3, column=3, padx=(10,10), pady=(0,5))
    blackman.grid(row=3, column=4, padx=(10,10), pady=(0,5))
    btn_cut.grid(row=4, column=1, padx=(10,10), pady=(5,5))
    btn_histogram.grid(row=4, column=2, padx=(10,10), pady=(5,5))
    btn_spectrogram.grid(row=4, column=3, padx=(10,10), pady=(5,5))
    #btn_histogram_full.grid(row=5, column=2, padx=(10,10), pady=(5,5))

    window.mainloop()

if __name__ == '__main__':
    begin()




