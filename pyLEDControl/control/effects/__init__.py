from control.effects.wave import Wave
from control.effects.random_dot import RandomDot
from control.effects.rainbow_wave import RainbowWave
from control.effects.digi_clock import DigiClock
from control.effects.spotify import Spotify
from control.effects.off import OFF
from control.effects.weather import Weather
import sys

effects = "control.effects"
__import__(effects)
effect_list = sys.modules[effects]
effect_dict = {
    name: obj for name, obj in effect_list.__dict__.items() if isinstance(obj, type)
}
