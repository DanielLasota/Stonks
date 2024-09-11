from unittest.mock import MagicMock
from stonks.stonks import ChartRenderer
import pandas as pd


class TestChartRenderer:

    def test_change_plot_type_updates_plot(self):
        # given
        asset = 'EURUSD=X'
        df = pd.DataFrame({
            'Close': [10, 20, 30],
            'SMA': [15, 25, 35],
            'Upper_Bollinger_Band': [20, 30, 40],
            'Lower_Bollinger_Band': [10, 20, 30]
        })
        chart_renderer = ChartRenderer(asset, df)
        chart_renderer.update_plot = MagicMock()

        # when
        chart_renderer.change_plot_type('line')

        # then
        chart_renderer.update_plot.assert_called_once()
        assert chart_renderer.current_plot_type == 'line'

    def test_change_period_triggers_update_asset_data(self):
        # given
        asset = 'EURUSD=X'
        df = pd.DataFrame({
            'Close': [10, 20, 30],
            'SMA': [15, 25, 35],
            'Upper_Bollinger_Band': [20, 30, 40],
            'Lower_Bollinger_Band': [10, 20, 30]
        })
        chart_renderer = ChartRenderer(asset, df)
        chart_renderer.update_asset_data = MagicMock()

        # when
        chart_renderer.change_period('3mo')

        # then
        chart_renderer.update_asset_data.assert_called_once()
        assert chart_renderer.current_period == '3mo'

    def test_change_interval_triggers_update_asset_data(self):
        # given
        asset = 'EURUSD=X'
        df = pd.DataFrame({
            'Close': [10, 20, 30],
            'SMA': [15, 25, 35],
            'Upper_Bollinger_Band': [20, 30, 40],
            'Lower_Bollinger_Band': [10, 20, 30]
        })
        chart_renderer = ChartRenderer(asset, df)
        chart_renderer.update_asset_data = MagicMock()

        # when
        chart_renderer.change_interval('1d')

        # then
        chart_renderer.update_asset_data.assert_called_once()
        assert chart_renderer.current_interval == '1d'

    def test_submit_text_triggers_update_asset_data(self):
        # given
        asset = 'AAPL'
        df = pd.DataFrame({
            'Close': [10, 20, 30],
            'SMA': [15, 25, 35],
            'Upper_Bollinger_Band': [20, 30, 40],
            'Lower_Bollinger_Band': [10, 20, 30]
        })
        chart_renderer = ChartRenderer(asset, df)
        chart_renderer.update_asset_data = MagicMock()

        # when
        chart_renderer.submit_text('GOOGL')

        # then
        chart_renderer.update_asset_data.assert_called_once()
        assert chart_renderer.asset == 'GOOGL'