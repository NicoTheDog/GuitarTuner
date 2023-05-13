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
    return scipy.signal.find_peaks(y,prominence=0.01,height=(0,440))

def Display_Data(x,y):
    (peaks,index) = Detect_Peak(y)
    print(index)
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
    Display_Data(freq[:1024//2],amp[:1024//2])

if __name__ == "__main__":

    (record_data,audio) = Record_Audio()

    while True:
        try:
            Fourier_Transform(record_data)
        except KeyboardInterrupt:
            break
    
    Record_Stop(record_data,audio)