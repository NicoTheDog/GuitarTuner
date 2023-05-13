import pyaudio # 音声を録音するためのライブラリ   
import numpy as np
import matplotlib.pyplot as plt # 描画用のライブラリ
import scipy

SAMP_RATE = 44100 #サンプリングレート
FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 1

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

def Detect_Peak(y):
    return scipy.signal.find_peaks(y,prominence=0.1)

def Display_Data(x,y):
    peaks,_ = Detect_Peak(y)
    plt.plot(x,y)
    plt.scatter(x[peaks],y[peaks],color = 'red')
    plt.xlabel("frequency [Hz]")
    plt.ylabel("amplitude spectrum[V]")
    plt.xlim(1,4096)
    plt.grid()
    plt.draw()
    plt.pause(0.1)
    plt.cla()

def Fourier_Transform(record_data):
    data = record_data.read(1024)
    # 一次元データに変換する
    audio_data = np.frombuffer(data,dtype='int16')
    # 取得したデータをフーリエ変換をする(複素配列)
    F = np.fft.fft(audio_data)
    # 振幅を求める
    F = F / (SAMP_RATE / 2)
    amp = np.abs(F)
    # 周波数をもとめる
    freq = np.fft.fftfreq(1024,d=(1/SAMP_RATE))
    Display_Data(freq[:1024//2],amp[:1024//2])

if __name__ == "__main__":

    (record_data,audio) = Record_Audio()

    while True:
        try:
            Fourier_Transform(record_data)
        except KeyboardInterrupt:
            break
    
    Record_Stop(record_data,audio)