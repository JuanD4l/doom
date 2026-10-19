/**
 * SINTETIZADOR DE AUDIO PROCEDURAL (Web Audio API)
 * Genera todos los efectos y música ambiental en tiempo de ejecución.
 */
class SoundSynthesizer {
    constructor() {
        this.ctx = null;
        this.initialized = false;
        this.ambientGain = null;
    }

    init() {
        if (this.initialized) return;
        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.ctx = new AudioContext();
            this.initialized = true;
            this._startAmbientDrone();
        } catch (e) {
            console.warn("Web Audio API no soportada:", e);
        }
    }

    _ensureContext() {
        if (this.ctx && this.ctx.state === "suspended") {
            this.ctx.resume();
        }
    }

    playShotgun() {
        if (!this.initialized) return;
        this._ensureContext();
        const t = this.ctx.currentTime;

        // Golpe de graves
        const osc = this.ctx.createOscillator();
        const oscGain = this.ctx.createGain();
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(120, t);
        osc.frequency.exponentialRampToValueAtTime(30, t + 0.3);
        oscGain.gain.setValueAtTime(0.7, t);
        oscGain.gain.exponentialRampToValueAtTime(0.01, t + 0.35);
        osc.connect(oscGain);
        oscGain.connect(this.ctx.destination);
        osc.start(t);
        osc.stop(t + 0.35);

        // Explosión de ruido blanco filtrado
        const bufferSize = this.ctx.sampleRate * 0.35;
        const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }

        const noise = this.ctx.createBufferSource();
        noise.buffer = buffer;
        const filter = this.ctx.createBiquadFilter();
        filter.type = "lowpass";
        filter.frequency.setValueAtTime(1400, t);
        filter.frequency.exponentialRampToValueAtTime(200, t + 0.35);

        const noiseGain = this.ctx.createGain();
        noiseGain.gain.setValueAtTime(0.8, t);
        noiseGain.gain.exponentialRampToValueAtTime(0.01, t + 0.35);

        noise.connect(filter);
        filter.connect(noiseGain);
        noiseGain.connect(this.ctx.destination);
        noise.start(t);
    }

    playHitmarker() {
        if (!this.initialized) return;
        this._ensureContext();
        const t = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(1800, t);
        osc.frequency.exponentialRampToValueAtTime(800, t + 0.06);
        gain.gain.setValueAtTime(0.6, t);
        gain.gain.exponentialRampToValueAtTime(0.01, t + 0.06);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(t);
        osc.stop(t + 0.06);
    }

    playLaser() {
        if (!this.initialized) return;
        this._ensureContext();
        const t = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(1100, t);
        osc.frequency.exponentialRampToValueAtTime(240, t + 0.16);
        gain.gain.setValueAtTime(0.4, t);
        gain.gain.exponentialRampToValueAtTime(0.01, t + 0.16);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(t);
        osc.stop(t + 0.16);
    }

    playExplosion() {
        if (!this.initialized) return;
        this._ensureContext();
        const t = this.ctx.currentTime;

        const bufferSize = this.ctx.sampleRate * 0.5;
        const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }

        const noise = this.ctx.createBufferSource();
        noise.buffer = buffer;
        const filter = this.ctx.createBiquadFilter();
        filter.type = "lowpass";
        filter.frequency.setValueAtTime(500, t);
        filter.frequency.exponentialRampToValueAtTime(60, t + 0.5);

        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(0.9, t);
        gain.gain.exponentialRampToValueAtTime(0.01, t + 0.5);

        noise.connect(filter);
        filter.connect(gain);
        gain.connect(this.ctx.destination);
        noise.start(t);
    }

    playHurt() {
        if (!this.initialized) return;
        this._ensureContext();
        const t = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = "square";
        osc.frequency.setValueAtTime(180, t);
        osc.frequency.exponentialRampToValueAtTime(70, t + 0.22);
        gain.gain.setValueAtTime(0.5, t);
        gain.gain.exponentialRampToValueAtTime(0.01, t + 0.22);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(t);
        osc.stop(t + 0.22);
    }

    playWaveFanfare() {
        if (!this.initialized) return;
        this._ensureContext();
        const t = this.ctx.currentTime;
        const freqs = [330, 440, 554, 660];
        freqs.forEach((f, idx) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            const startT = t + idx * 0.12;
            osc.type = "sine";
            osc.frequency.setValueAtTime(f, startT);
            gain.gain.setValueAtTime(0.4, startT);
            gain.gain.exponentialRampToValueAtTime(0.01, startT + 0.25);
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(startT);
            osc.stop(startT + 0.25);
        });
    }

    _startAmbientDrone() {
        if (!this.ctx) return;
        const osc = this.ctx.createOscillator();
        const filter = this.ctx.createBiquadFilter();
        this.ambientGain = this.ctx.createGain();

        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(55, this.ctx.currentTime); // Sub-grave 55Hz

        filter.type = "lowpass";
        filter.frequency.setValueAtTime(140, this.ctx.currentTime);

        this.ambientGain.gain.setValueAtTime(0.12, this.ctx.currentTime);

        osc.connect(filter);
        filter.connect(this.ambientGain);
        this.ambientGain.connect(this.ctx.destination);
        osc.start();
    }
}
