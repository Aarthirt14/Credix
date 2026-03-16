import wave, struct, math
framerate = 16000
seconds = 1.2
frequency = 440.0
amplitude = 12000
frames = int(framerate * seconds)
with wave.open('backend/test-tone.wav', 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(framerate)
    for i in range(frames):
        value = int(amplitude * math.sin(2 * math.pi * frequency * i / framerate))
        w.writeframes(struct.pack('<h', value))
print('created backend/test-tone.wav')


 