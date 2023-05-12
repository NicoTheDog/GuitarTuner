import pyaudio # 音声を録音するためのライブラリ   
import numpy as np  
import wave # waveファイルを扱うためのライブラリ
import matplotlib.pyplot as plt # 描画用のライブラリ

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

def Display_Record_Data(record_data):
    data = record_data.read(1024)
    audio_data = np.frombuffer(data,dtype='int16')

    plt.plot(audio_data)
    plt.draw()
    plt.pause(1)
    plt.cla()

if __name__ == "__main__":

    (record_data,audio) = Record_Audio()

    while True:
        try:
            Display_Record_Data(record_data)
        except KeyboardInterrupt:
            break
    
    Record_Stop(record_data,audio)