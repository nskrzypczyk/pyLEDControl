from control.effects.wave import Wave
from control.effects.game_of_life import GameOfLife
from control.effects.random_dot import RandomDot
from control.effects.rainbow_wave import RainbowWave
from control.effects.digi_clock import DigiClock
from control.effects.spotify import Spotify
from control.effects.weather import Weather
from control.effects.shuffle import Shuffle
from control.effects.off import OFF
import sys

effects = "control.effects"
__import__(effects)
effect_list = sys.modules[effects]
effect_dict = {
    name: obj for name, obj in effect_list.__dict__.items() if isinstance(obj, type)
}
