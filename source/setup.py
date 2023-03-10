import os
import pygame as pg
from . import constants as c
from . import tools

pg.init()
pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
pg.display.set_caption(c.ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(c.SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

path0 = str(__file__).split('\\')[0] + '\\' + str(__file__).split('\\')[1] + '\\'+ str(__file__).split('\\')[2] + '\\resources'

GFX = tools.load_all_gfx(os.path.join(path0, "Graphics"))
MY_GFX = tools.load_all_gfx(os.path.join(path0, "QuestionProj"))
SFX = tools.load_all_sfx(os.path.join(path0, "Sound"))