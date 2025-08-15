---
title: MaixCAM MaixPy Real-time voice recognition
update:
  - date: 2024-10-08
    author: 916BGAI
    version: 1.0.0
    content: Initial document
  - date: 2025-05-13
    author: lxowalle
    version: 1.0.1
    content: Added usage instructions for Whisper
---

## Introduction

`MaixCAM` has ported the `Maix-Speech` offline speech library, enabling continuous Chinese numeral recognition, keyword recognition, and large vocabulary speech recognition capabilities. It supports audio recognition in `PCM` and `WAV` formats, and can accept input recognition via the onboard microphone.

Speech recognition model support list:

|         | MaixCAM | MaixCAM Pro | MaixCAM2 |
| ------- | ------- | ----------- | -------- |
| Whisper | ❌       | ❌           | ✅        |
| Speech  | ✅       | ✅           | ❌        |

In addition, we have ported OpenAI's Whisper speech recognition model to the `MaixCAM2`, enabling powerful speech-to-text functionality even on resource-constrained devices.

## Using Whisper for Speech-to-Text

> Note: MaixCAM and MaixCAM Pro do not support the Whisper model.

Currently, only the base version of the Whisper model is supported. It accepts single-channel WAV audio with a 16kHz sample rate and can recognize both Chinese and English.

```python
from maix import nn

whisper = nn.Whisper(model="/root/models/whisper-base/whisper-base.mud")

wav_path = "/maixapp/share/audio/demo.wav"

res = whisper.transcribe(wav_path)

print('whisper:', res)
```

Notes:
1. First, import the nn module to create the Whisper model object:
```python
from maix import nn
```
2. Load the model. Currently, only the `base` version is supported:
```python
whisper = nn.Whisper(model="/root/models/whisper-base/whisper-base.mud", language="en")
```
3. Prepare a WAV audio file with 1 channel and 16kHz sample rate, and run inference. The result will be returned directly:
```python
wav_path = "/maixapp/share/audio/demo.wav"
res = whisper.forward(wav_path)
print('whisper:', res)
```
4. Sample output:
```shell
whisper: Have fun exploring!
```
5. Give it a try yourself!

By default, it recognizes Chinese. To recognize English, pass the language parameter when initializing the object.
```python
whisper = nn.Whisper(model="/root/models/whisper-base/whisper-base.mud", language="en")
```

## Maix-Speech

[`Maix-Speech`](https://github.com/sipeed/Maix-Speech) is an offline speech recognition library specifically designed for embedded environments. It has been deeply optimized for speech recognition algorithms, significantly reducing memory usage while maintaining excellent recognition accuracy. For detailed information, please refer to the [Maix-Speech Documentation](https://github.com/sipeed/Maix-Speech/blob/master/usage_zh.md).

### Continuous Large Vocabulary Speech Recognition

```python
from maix import app, nn

speech = nn.Speech("/root/models/am_3332_192_int8.mud")
speech.init(nn.SpeechDevice.DEVICE_MIC)

def callback(data: tuple[str, str], len: int):
    print(data)

lmS_path = "/root/models/lmS/"

speech.lvcsr(lmS_path + "lg_6m.sfst", lmS_path + "lg_6m.sym", \
             lmS_path + "phones.bin", lmS_path + "words_utf.bin", \
             callback)

while not app.need_exit():
    frames = speech.run(1)
    if frames < 1:
        print("run out\n")
        break
```

### Usage

1. Import the `app` and `nn` modules

```python
from maix import app, nn
```

2. Load the acoustic model

```python
speech = nn.Speech("/root/models/am_3332_192_int8.mud")
```

- You can also load the `am_7332` acoustic model; larger models provide higher accuracy but consume more resources.

3. Choose the corresponding audio device

```python
speech.init(nn.SpeechDevice.DEVICE_MIC)
speech.init(nn.SpeechDevice.DEVICE_MIC, "hw:0,0")   # Specify the audio input device
```

- This uses the onboard microphone and supports both `WAV` and `PCM` audio as input.

```python
speech.init(nn.SpeechDevice.DEVICE_WAV, "path/audio.wav")   # Using WAV audio input
```

```python
speech.init(nn.SpeechDevice.DEVICE_PCM, "path/audio.pcm")   # Using PCM audio input
```

- Note that `WAV` must be `16KHz` sample rate with `S16_LE` storage format. You can use the `arecord` tool for conversion.

```shell
arecord -d 5 -r 16000 -c 1 -f S16_LE audio.wav
```

- When recognizing `PCM/WAV` , if you want to reset the data source, such as for the next WAV file recognition, you can use the `speech.device` method, which will automatically clear the cache:

```python
speech.device(nn.SpeechDevice.DEVICE_WAV, "path/next.wav")
```

4. Set up the decoder

```python
def callback(data: tuple[str, str], len: int):
    print(data)

lmS_path = "/root/models/lmS/"

speech.lvcsr(lmS_path + "lg_6m.sfst", lmS_path + "lg_6m.sym", \
             lmS_path + "phones.bin", lmS_path + "words_utf.bin", \
             callback)
```
- The user can configure multiple decoders simultaneously. `lvcsr` decoder is registered to output continuous speech recognition results (for fewer than 1024 Chinese characters).

- When setting up the `lvcsr` decoder, you need to specify the paths for the `sfst` file, the `sym` file (output symbol table), the path for `phones.bin` (phonetic table), and the path for `words.bin` (dictionary). Lastly, a callback function must be set to handle the decoded data.

- If a decoder is no longer needed, you can deinitialize it by calling the `speech.dec_deinit` method.

```python
speech.dec_deinit(nn.SpeechDecoder.DECODER_LVCSR)
```

5. Recognition

```python
while not app.need_exit():
    frames = speech.run(1)
    if frames < 1:
        print("run out\n")
        break
```

- Use the `speech.run` method to run speech recognition. The parameter specifies the number of frames to run each time, returning the actual number of frames processed. Users can choose to run 1 frame each time and then perform other processing, or run continuously in a single thread, stopping it with an external thread.

- To clear the cache of recognized results, you can use the `speech.clear` method.

- When switching decoders during recognition, the first frame after the switch may produce incorrect results. You can use `speech.skip_frames(1)` to skip the first frame and ensure the accuracy of subsequent results.

### Recognition Results

If the above program runs successfully, speaking into the onboard microphone will yield real-time speech recognition results, such as:

```shell
### SIL to clear decoder!
('今天天气 怎么样 ', 'jin1 tian1 tian1 qi4 zen3 me yang4 ')
```