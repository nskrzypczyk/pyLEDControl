
import time


from bindings.stock_binding import StockBinding, StockData
from control.adapter.abstract_matrix import AbstractColor, AbstractMatrix
from control.effects.abstract_effect import AbstractEffect

from control.abstract_effect_options import AbstractEffectOptions

"""
    This effect uses newly added abstractions defined in AbstractEffect aiming to reduce effect boilerplate.
"""

PAGE_TIME_SEC = 4
FPS = 1


class Stocks(AbstractEffect):
    @staticmethod
    def run(matrix_cls: type, options: AbstractEffectOptions, conn, *args, **kwargs):
        matrix, canvas, font, field, rows, cols = AbstractEffect.create_context(
            matrix_cls)
        font.LoadFont("/usr/local/share/rgbfonts/4x6.bdf")
        binding = StockBinding(initialze=True)

        red = matrix.graphics.Color(255, 100, 100)
        green = matrix.graphics.Color(19, 249, 19)
        white = matrix.graphics.Color(255, 255, 255)

        def get_color_for_percentual_change(change: float) -> AbstractColor:
            if change > 0:
                return green
            elif round(change) == 0:
                return white
            return red

        def render_header(data: StockData):
            matrix.graphics.DrawText(canvas, font, 1, 7, white, data["symbol"])
            matrix.graphics_extended.DrawTextAligned(
                matrix, canvas, font, 7, white, f"{data['close_current']}{data['currency']}", align="right", x_offset=-1)
            matrix.graphics.DrawLine(canvas, 0, 9, cols, 9, white)

        def render_data(data: StockData):
            y_baseline = 17

            matrix.graphics.DrawText(canvas, font, 1, y_baseline, white, "1d:")
            matrix.graphics_extended.DrawTextAligned(matrix, canvas, font, y_baseline, get_color_for_percentual_change(
                data["change_1d_pct"]), str(data["change_1d_pct"]) + "%", align="right", x_offset=-1)

            matrix.graphics.DrawText(
                canvas, font, 1, y_baseline + 8, white, "1w:")
            matrix.graphics_extended.DrawTextAligned(matrix, canvas, font, y_baseline + 8, get_color_for_percentual_change(
                data["change_7d_pct"]), str(data["change_7d_pct"]) + "%", align="right", x_offset=-1)

            matrix.graphics.DrawText(
                canvas, font, 1, y_baseline + 16, white, "2w:")
            matrix.graphics_extended.DrawTextAligned(matrix, canvas, font, y_baseline + 16, get_color_for_percentual_change(
                data["change_14d_pct"]), str(data["change_14d_pct"]) + "%", align="right", x_offset=-1)

            matrix.graphics.DrawText(
                canvas, font, 1, y_baseline + 24, white, "1m:")
            matrix.graphics_extended.DrawTextAligned(matrix, canvas, font, y_baseline + 24, get_color_for_percentual_change(
                data["change_1m_pct"]), str(data["change_1m_pct"]) + "%", align="right", x_offset=-1)

            matrix.graphics.DrawText(
                canvas, font, 1, y_baseline + 32, white, "6m:")
            matrix.graphics_extended.DrawTextAligned(matrix, canvas, font, y_baseline + 32, get_color_for_percentual_change(
                data["change_6m_pct"]), str(data["change_6m_pct"]) + "%", align="right", x_offset=-1)

        def render_footer(data: StockData):
            y_baseline = 53
            matrix.graphics.DrawLine(
                canvas, 0, y_baseline, cols, y_baseline, white)

            matrix.graphics_extended.DrawTextAligned(
                matrix, canvas, font, y_baseline + 8, white, str(data["name"]), align="left", x_offset=1)

        counter = 0

        def action():
            nonlocal canvas, counter
            if counter == len(binding.symbols):
                counter = 0
            stock_data = binding.get_by_idx(counter)
            ##########################

            if stock_data is not None:
                canvas.Clear()
                render_header(stock_data)
                render_data(stock_data)
                render_footer(stock_data)

            ##########################
            matrix.brightness = options.brightness
            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(PAGE_TIME_SEC)
            counter += 1

        Stocks.loop(conn, action)
