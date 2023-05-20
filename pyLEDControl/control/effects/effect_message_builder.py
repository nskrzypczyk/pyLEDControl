from typing import Union
from control.effects import effect_dict
from control.effect_message import EffectMessage


class EffectMessageBuilder:
    def __init__(self) -> None:
        self.msg = EffectMessage()

    def set_effect(self, effect: Union[type, str]) -> EffectMessage:
        if isinstance(effect, str):
            self.msg.effect = effect_dict[effect]
        else:
            self.msg.effect = effect
        return self.msg
