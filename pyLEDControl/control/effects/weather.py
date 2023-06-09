import time
from control.effects.abstract_effect import AbstractEffect
from control.effect_message import EffectMessage
from control.adapter.abstract_matrix import AbstractMatrix
import settings
from bindings.weather_binding import WeatherBinding, is_weather_up_to_date

# icons are 6x8


class Weather(AbstractEffect):
    @staticmethod
    def run(matrix_class: type, msg: EffectMessage):
        matrix: AbstractMatrix = matrix_class(options=settings.rgb_options())
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()
        font = matrix.graphics.Font()
        font.LoadFont("../../rpi-rgb-led-matrix/fonts/4x6.bdf")
        refresh_rate = 5  # in seconds
        binding = WeatherBinding()
        forecast = binding.get()

        while 1:
            xoff = 0
            yoff = 6
            if not is_weather_up_to_date(forecast):
                forecast = binding.get()
            br = msg.get_brightness()
            color = 255 * br
            color_white = matrix.graphics.Color(
                color, color, color)

            # Build header row
            matrix.graphics.DrawText(
                canvas, font, xoff+2, yoff, color_white, "W")
            matrix.graphics.DrawText(
                canvas, font, xoff+11, yoff, color_white, "Tmax")
            matrix.graphics.DrawText(
                canvas, font, xoff+34, yoff, color_white, "Tmin")
            matrix.graphics.DrawText(
                canvas, font, xoff+54, yoff, color_white, "R%")

            for i in range(64):
                canvas.SetPixel(i, 8, color, color, color)

            yoff = 9
            for row in range(4):
                yoff += 12
                for col in range(4):
                    matrix.graphics.DrawText(
                        canvas, font, xoff+15, yoff, color_white, str(int(forecast["temperature_2m_max"][row])))
                    matrix.graphics.DrawText(
                        canvas, font, xoff+37, yoff, color_white, str(int(forecast["temperature_2m_min"][row])))
                    matrix.graphics.DrawText(
                        canvas, font, xoff+54, yoff, color_white, str(int(forecast["precipitation_probability"][row])))

            canvas = matrix.SwapOnVSync(canvas)

            # Additional loop because SetImage does not use canvas
            yoff = 9
            for row in range(4):
                yoff += 12
                for col in range(4):
                    matrix.SetImageFromFile(
                        forecast["icons"][row], xoff+2, yoff-6, br)
            time.sleep(refresh_rate)
