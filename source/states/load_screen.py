import pygame as pg
from .. import constants as c
from .. import setup, tools
from ..components import info

class LoadScreen(tools.State):
    def __init__(self):
        tools.State.__init__(self)
        self.screen1 = setup.GFX['load_screen1']
        self.screen2 = setup.GFX['load_screen2']
        self.time_list = [16000 * 1, 16000 * 2, 16000 * 2 + 2000, 16000 * 2 + 2000 + 100, 16000 * 2 + 2000 + 200]

    def startup(self, current_time, persist):
        self.start_time = current_time
        self.persist = persist
        self.game_info = self.persist
        self.next = self.set_next_state()

        info_state = self.set_info_state()
        self.overhead_info = info.Info(self.game_info, info_state)
        self.sound()

    def set_next_state(self):
        return c.LEVEL

    def set_info_state(self):
        return c.LOAD_SCREEN

    def update(self, surface, keys, current_time):
        # 如果按下enter键：
        if keys[pg.K_SPACE]:
            self.close_sound()
            self.done = True
        else:
            if (current_time - self.start_time) < self.time_list[0]:
                surface.blit(self.screen1, (0, 0))
            elif (current_time - self.start_time) < self.time_list[1]:
                surface.blit(self.screen2, (0, 0))
            elif (current_time - self.start_time) < self.time_list[2]:
                surface.fill(c.BLACK)
                self.overhead_info.update(self.game_info)
                self.overhead_info.draw(surface)
            elif (current_time - self.start_time) < self.time_list[3]:
                surface.fill(c.BLACK)
            elif (current_time - self.start_time) < self.time_list[4]:
                surface.fill((106, 150, 252))
            else:
                self.close_sound()
                self.done = True

    def sound(self):
        self.sfx_dict = setup.SFX
        self.sfx_dict['加载《晴天》'].play()

    def close_sound(self):
        self.sfx_dict['加载《晴天》'].stop()


class GameOver(LoadScreen):
    def __init__(self):
        LoadScreen.__init__(self)
        self.time_list = [3000, 3200, 3235]

    def set_next_state(self):
        return c.MAIN_MENU

    def set_info_state(self):
        return c.GAME_OVER


class TimeOut(LoadScreen):
    def __init__(self):
        LoadScreen.__init__(self)
        self.time_list = [2400, 2600, 2635]

    def set_next_state(self):
        if self.persist[c.LIVES] == 0:
            return c.GAME_OVER
        else:
            return c.LOAD_SCREEN

    def set_info_state(self):
        return c.TIME_OUT
