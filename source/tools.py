import os
from abc import abstractmethod
import pygame as pg

# import pyaudio
# import wave
# import numpy as np
# tmp = []
# TODO: 分贝控制

keybinding = {
    'action': pg.K_s,
    'jump': pg.K_a,
    'left': pg.K_LEFT,
    'right': pg.K_RIGHT,
    'down': pg.K_DOWN
}


class State():
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.next = None
        self.persist = {}

    @abstractmethod
    def startup(self, current_time, persist):
        '''abstract method'''

    def cleanup(self):
        self.done = False
        return self.persist

    @abstractmethod
    def update(sefl, surface, keys, current_time):
        '''abstract method'''


class Control():
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = 60
        self.current_time = 0.0
        self.keys = pg.key.get_pressed()
        self.state_dict = {}
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def update(self):
        self.current_time = pg.time.get_ticks()
        if self.state.done:
            self.flip_state()
        self.state.update(self.screen, self.keys, self.current_time)

    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, persist)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()

    def main(self):
        # CHUNK = 512
        # FORMAT = pyaudio.paInt16
        # CHANNELS = 1
        # RATE = 48000
        # RECORD_SECONDS = 5
        # WAVE_OUTPUT_FILENAME = "cache.wav"
        # p = pyaudio.PyAudio()
        # stream = p.open(format=FORMAT,
        #                 channels=CHANNELS,
        #                 rate=RATE,
        #                 input=True,
        #                 frames_per_buffer=CHUNK)
        # print("开始缓存录音")
        # frames = []
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)

        #     for i in range(2):
        #         data = stream.read(CHUNK)
        #         frames.append(data)
        #     audio_data = np.fromstring(data, dtype=np.short)
        #     temp = np.max(audio_data)
        #     tmp.append(temp)
        #     print('监听麦克风音量：',tmp[-1])
        # stream.stop_stream()
        # stream.close()
        # p.terminate()
        # wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        # wf.setnchannels(CHANNELS)
        # wf.setsampwidth(p.get_sample_size(FORMAT))
        # wf.setframerate(RATE)
        # wf.writeframes(b''.join(frames))
        # wf.close()


def get_image(sheet, x, y, width, height, colorkey, scale):
    image = pg.Surface([width, height])
    rect = image.get_rect()

    image.blit(sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(colorkey)
    image = pg.transform.scale(image,
                               (int(rect.width * scale),
                                int(rect.height * scale)))
    return image

def load_all_gfx(directory, colorkey=(0, 0, 0), accept=('.png', '.jpg', '.bmp', '.gif')):
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name] = img
    return graphics

def load_all_sfx(directory, accept=('.wav', '.mpe', '.ogg', '.mdi', '.mp3')):
    effects = {}
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pg.mixer.Sound(os.path.join(directory, fx))
    return effects