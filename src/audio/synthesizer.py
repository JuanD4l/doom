"""
================================================================================
CAPA DE AUDIO PROCEDURAL (Audio Infrastructure Layer)
================================================================================
Genera ondas PCM de 16-bit estéreo en memoria para sintetizar efectos sonoros
(disparos, impactos, explosiones, fanfarrias) sin depender de archivos de audio externos.
================================================================================
"""

import math
import random
import struct
import pygame

class SoundSynthesizer:
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        self.enabled = True
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=2, buffer=512)
            self.sounds = {
                "shotgun": self._generate_shotgun(),
                "hitmarker": self._generate_hitmarker(),
                "laser": self._generate_laser(),
                "explosion": self._generate_explosion(),
                "hurt": self._generate_hurt(),
                "wave": self._generate_wave(),
            }
        except Exception as e:
            print(f"[Audio] Error al inicializar sintetizador: {e}")
            self.enabled = False
            self.sounds = {}

    def _pack_samples(self, samples):
        buf = bytearray()
        for s in samples:
            val = int(max(-1.0, min(1.0, s)) * 32767)
            raw = struct.pack('<h', val)
            buf.extend(raw) # Izquierda
            buf.extend(raw) # Derecha
        return pygame.mixer.Sound(buffer=bytes(buf))

    def _generate_shotgun(self):
        duration = 0.35
        n = int(self.sample_rate * duration)
        samples = []
        for i in range(n):
            t = i / self.sample_rate
            freq = 110.0 - 70.0 * (t / duration)
            bass = math.sin(2.0 * math.pi * freq * t)
            noise = (random.random() * 2.0 - 1.0)
            amp = math.exp(-7.5 * (t / duration))
            sample = (bass * 0.7 + noise * 0.55) * amp
            samples.append(sample)
        return self._pack_samples(samples)

    def _generate_hitmarker(self):
        duration = 0.06
        n = int(self.sample_rate * duration)
        samples = []
        for i in range(n):
            t = i / self.sample_rate
            freq = 1800.0 - 600.0 * (t / duration)
            amp = math.exp(-22.0 * (t / duration))
            sample = math.sin(2.0 * math.pi * freq * t) * amp * 0.8
            samples.append(sample)
        return self._pack_samples(samples)

    def _generate_laser(self):
        duration = 0.18
        n = int(self.sample_rate * duration)
        samples = []
        for i in range(n):
            t = i / self.sample_rate
            freq = 1200.0 * (0.25 ** (t / duration))
            amp = math.exp(-6.5 * (t / duration))
            sample = math.sin(2.0 * math.pi * freq * t) * amp * 0.6
            samples.append(sample)
        return self._pack_samples(samples)

    def _generate_explosion(self):
        duration = 0.5
        n = int(self.sample_rate * duration)
        samples = []
        prev = 0.0
        for i in range(n):
            t = i / self.sample_rate
            white = random.random() * 2.0 - 1.0
            low_noise = prev * 0.82 + white * 0.18
            prev = low_noise
            sub = math.sin(2.0 * math.pi * 50.0 * t)
            amp = math.exp(-4.5 * (t / duration))
            sample = (low_noise * 0.75 + sub * 0.35) * amp
            samples.append(sample)
        return self._pack_samples(samples)

    def _generate_hurt(self):
        duration = 0.22
        n = int(self.sample_rate * duration)
        samples = []
        for i in range(n):
            t = i / self.sample_rate
            freq = 160.0 - 90.0 * (t / duration)
            square = 1.0 if math.sin(2.0 * math.pi * freq * t) > 0 else -1.0
            amp = math.exp(-6.0 * (t / duration))
            sample = square * amp * 0.5
            samples.append(sample)
        return self._pack_samples(samples)

    def _generate_wave(self):
        duration = 0.7
        n = int(self.sample_rate * duration)
        samples = []
        freqs = [330.0, 440.0, 554.0, 660.0]
        step = duration / len(freqs)
        for i in range(n):
            t = i / self.sample_rate
            idx = min(int(t / step), len(freqs) - 1)
            freq = freqs[idx]
            sub_t = t - (idx * step)
            amp = math.exp(-3.5 * (sub_t / step))
            sample = (math.sin(2.0 * math.pi * freq * t) + 0.3 * math.sin(4.0 * math.pi * freq * t)) * amp * 0.5
            samples.append(sample)
        return self._pack_samples(samples)

    def play(self, name):
        if self.enabled and name in self.sounds:
            try:
                self.sounds[name].play()
            except Exception:
                pass
