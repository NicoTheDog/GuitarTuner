import pyaudio # 音声を録音するためのライブラリ   
import numpy as np
import matplotlib.pyplot as plt # 描画用のライブラリ
import scipy
import tkinter as tk

SAMP_RATE = 44100 #サンプリングレート
FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 1

Regular_Tuner = {
    "E" : 82,
    "A" : 110,
    "D" : 147,
    "G" : 196,
    "B" : 247,
    "E" : 330
}

root = tk.Tk()
root.geometry('600x400')
root.title('サンプル画面')

label = tk.Label(
    root,
    width=20,
    height=1
)
label.pack()

def Record_Audio():
    audio = pyaudio.PyAudio()
    record_data = audio.open(
        format = FORMAT,
        channels = CHANNELS,
        rate = SAMP_RATE,
        input = True,
        frames_per_buffer = CHUNK
    )

    return record_data,audio

def Record_Stop(record_data,audio):
    record_data.stop_stream()
    record_data.close()
    audio.terminate()

def Detect_Peak(x,y):
    # 録ったデータのピークを全て調べる
    peaks,index =  scipy.signal.find_peaks(y,prominence=0.01,height=(0,440))
    list_peaks = []
    # 基音（440Hz未満のピーク値だけを抽出する）
    for p in peaks:
        if(x[p] > 440):
            break
        list_peaks.append(p)
    return list_peaks


def GetNearestValue(values):
    # 差が最小の値のindexを取得する
    tuner = ""
    diff = 1000
    for key in Regular_Tuner.keys():
        for v in values:
            if(abs(Regular_Tuner[key] - v) < abs(diff) ):
                diff = Regular_Tuner[key] - v
                tuner = key
    return tuner,int(diff)

def Display_Window(x,y):
    peaks = Detect_Peak(x,y)
    # print(peaks)
    (tuner,diff) = GetNearestValue(x[peaks])
    # print(str(tuner) + " : " + str(diff))
    if tuner:
        label.config(
            text = str(tuner) + ":" + str(diff),
            font = ("MSゴシック","20","bold")
        )
        label.update()

def Display_Data(x,y):
    peaks = Detect_Peak(x,y)
    plt.plot(x,y)
    plt.scatter(x[peaks],y[peaks],color = 'red')
    plt.xlabel("frequency [Hz]")
    plt.ylabel("amplitude spectrum[V]")
    plt.xlim(1,1024)
    plt.grid()
    plt.draw()
    plt.pause(0.001)
    plt.cla()

def Fourier_Transform(record_data):
    data = record_data.read(1024)
    audio_data = np.frombuffer(data,dtype='int16')
    # 取得したデータをフーリエ変換をする(複素配列)
    F = np.fft.fft(audio_data)
    # 振幅を求める
    F = F / (SAMP_RATE / 2)
    window = scipy.signal.hann(SAMP_RATE)
    F = F * (SAMP_RATE / np.sum(window))
    amp = np.abs(F)
    # 周波数を求める
    freq = np.fft.fftfreq(1024,d=(1/SAMP_RATE))
    # パワースペクトルを求める
    amp = pow(amp,2)
    # Display_Data(freq[:1024//2],amp[:1024//2])
    Display_Window(freq[:1024//2],amp[:1024//2])
if __name__ == "__main__":

    (record_data,audio) = Record_Audio()

    while True:
        try:
            Fourier_Transform(record_data)
        except KeyboardInterrupt:
            break
    
    Record_Stop(record_data,audio)

root.mainloop()