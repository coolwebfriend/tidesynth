from abc import ABC, abstractmethod
import numpy as np
from scipy.io import wavfile
import math
import csv
import time
import click

class Oscillator(ABC):
    def __init__(self, freq=440, phase=0, amp=1, \
                 sample_rate=44_100, wave_range=(-1, 1)):
        self._freq = freq
        self._amp = amp
        self._phase = phase
        self._sample_rate = sample_rate
        self._wave_range = wave_range
        
        # Properties that will be changed
        self._f = freq
        self._a = amp
        self._p = phase
        
    @property
    def init_freq(self):
        return self._freq
    
    @property
    def init_amp(self):
        return self._amp
    
    @property
    def init_phase(self):
        return self._phase
    
    @property
    def freq(self):
        return self._f
    
    @freq.setter
    def freq(self, value):
        self._f = value
        self._post_freq_set()
        
    @property
    def amp(self):
        return self._a
    
    @amp.setter
    def amp(self, value):
        self._a = value
        self._post_amp_set()
        
    @property
    def phase(self):
        return self._p
    
    @phase.setter
    def phase(self, value):
        self._p = value
        self._post_phase_set()
    
    def _post_freq_set(self):
        pass
    
    def _post_amp_set(self):
        pass
    
    def _post_phase_set(self):
        pass
    
    @abstractmethod
    def _initialize_osc(self):
        pass
    
    @staticmethod
    def squish_val(val, min_val=0, max_val=1):
        return (((val + 1) / 2 ) * (max_val - min_val)) + min_val

    @abstractmethod
    def __next__(self):
        return None
    
    def __iter__(self):
        self.freq = self._freq
        self.phase = self._phase
        self.amp = self._amp
        self._initialize_osc()
        return self
    

class SineOscillator(Oscillator):
    def _post_freq_set(self):
        self._step = (2 * math.pi * self._f) / self._sample_rate
        
    def _post_phase_set(self):
        self._p = (self._p / 360) * 2 * math.pi
        
    def _initialize_osc(self):
        self._i = 0
        
    def __next__(self):
        val = math.sin(self._i + self._p)
        self._i = self._i + self._step
        if self._wave_range != (-1, 1):
            val = self.squish_val(val, *self._wave_range)
        return val * self._a
    

def wave_to_file(wav, wav2=None, fname="temp.wav", amp=0.1, sample_rate=44100):
    wav = np.array(wav)
    wav = np.int16(wav * amp * (2**15 - 1))
    
    if wav2 != None:
        wav2 = np.array(wav2)
        wav2 = np.int16(wav2 * amp * (2 ** 15 - 1))
        wav = np.stack([wav, wav2]).T
    
    wavfile.write(fname, sample_rate, wav)
    

class WaveAdder:
    def __init__(self, *oscillators):
        self.oscillators = oscillators
        self.n = len(oscillators)
    
    def __iter__(self):
        [iter(osc) for osc in self.oscillators]
        return self
    
    def __next__(self):
        return sum(next(osc) for osc in self.oscillators) / self.n
    
class SawtoothOscillator(Oscillator):
    def _post_freq_set(self):
        self._period = self._sample_rate / self._f
        self._post_phase_set
        
    def _post_phase_set(self):
        self._p = ((self._p + 90)/ 360) * self._period
    
    def _initialize_osc(self):
        self._i = 0
    
    def __next__(self):
        div = (self._i + self._p )/self._period
        val = 2 * (div - math.floor(0.5 + div))
        self._i = self._i + 1
        if self._wave_range != (-1, 1):
            val = self.squish_val(val, *self._wave_range)
        return val * self._a
    
class SquareOscillator(SineOscillator):
    def __init__(self, freq=440, phase=0, amp=1, \
                 sample_rate=44_100, wave_range=(-1, 1), threshold=0):
        super().__init__(freq, phase, amp, sample_rate, wave_range)
        self.threshold = threshold
    
    def __next__(self):
        val = math.sin(self._i + self._p)
        self._i = self._i + self._step
        if val < self.threshold:
            val = self._wave_range[0]
        else:
            val = self._wave_range[1]
        return val * self._a
    
class TriangleOscillator(SawtoothOscillator):
    def __next__(self):
        div = (self._i + self._p)/self._period
        val = 2 * (div - math.floor(0.5 + div))
        val = (abs(val) - 0.5) * 2
        self._i = self._i + 1
        if self._wave_range != (-1, 1):
            val = self.squish_val(val, *self._wave_range)
        return val * self._a


def row_to_oscillator(row, M2, fund):
    return SineOscillator(
            freq=fund*(float(row["Speed"])/float(M2["Speed"])),
            phase=float(row["Phase"])/360, 
            amp=64*float(row["Amplitude"])/float(M2["Amplitude"])
            )

def read_tides(path):
    with open(path) as f:
        tides = [{k: str(v) for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]
    return tides
    
def main():
    print(r"""##################################################################################

 _______ ,-.  ,'|"\    ,---.      .---. .-.   .-. .-. .-.  _______  .-. .-. 
|__   __||(|  | |\ \   | .-'     ( .-._) \ \_/ )/ |  \| | |__   __| | | | | 
  )| |   (_)  | | \ \  | `-.    (_) \     \   (_) |   | |   )| |    | `-' | 
 (_) |   | |  | |  \ \ | .-'    _  \ \     ) (    | |\  |  (_) |    | .-. | 
   | |   | |  /(|`-' / |  `--. ( `-'  )    | |    | | |)|    | |    | | |)| 
   `-'   `-' (__)`--'  /( __.'  `----'    /(_|    /(  (_)    `-'    /(  (_) 
                      (__)               (__)    (__)              (__)    

##################################################################################

TideSynth v0.1

by @coolwebfriend and @jgillner



""")
    
    input_filepath = click.prompt("\n\n\n\n provide the input CSV file path\n", type=str)
    fund = click.prompt("provide a fundamental frequency in hertz\n", type=int)
    duration = click.prompt("provide an audio duration in seconds\n", type=int)
    output = click.prompt("where should I save the .wav file? (full path)\n", type=str)

    tides = read_tides(input_filepath)
    M2 = tides[0]
    tides_with_amp = list(filter(lambda x: float(x["Amplitude"]) > 0, tides))
    oscillators = iter(list(map(lambda x: row_to_oscillator(x, M2, fund), tides_with_amp)))
    
    now = str(time.time())
    gen = iter(WaveAdder(*oscillators))
    wave_to_file([next(gen) for _ in range(44100 * duration)],
                 fname=output)
    
    print(f"saved output to {output}, thanks for playing")
    
if __name__ == "__main__":
    main()
