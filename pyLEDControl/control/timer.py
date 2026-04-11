from datetime import datetime
from functools import wraps

from misc.domain_data import TimerDataComponent


def use_timer(timer:TimerDataComponent) -> bool:
    if timer is None:
        return True
    
    if len(timer.days) == 0:
        return False
    
    # get current time
    now = datetime.now()

    if timer.days is not None:
        if now.weekday() not in timer.days:
            return False
        
    
    current_seconds = (
        now.hour * 3600 +
        now.minute * 60 +
        now.second
    )

    if timer.start is not None and timer.end is not None:
        if timer.start <= timer.end:
            valid = timer.start <= current_seconds <= timer.end
        else:
            # Overnight-window (e.g. 22:00–06:00)
            valid = (
                current_seconds >= timer.start or
                current_seconds <= timer.end
            )

        if not valid:
            return False
    return True
