from io import StringIO
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from stonks.stonks import DataFetcher, DataManipulator, ChartRenderer


class TestDataFetcher:

    def test_given_empty_dataframe_is_returned_when_passing_dataframe_then_exception_is_being_thrown(self):
        # given
        asset = 'INVALID_ASSET'
        # when
        with patch('stonks.stonks.yf.download', return_value=pd.DataFrame()):
            # then
            with pytest.raises(ValueError):
                fetcher = DataFetcher(asset)
                fetcher.fetch_data()

    def test_given_incorrect_asset_name_when_downloading_historical_data_then_empty_dataframe_is_returned(self):
        # given
        asset = 'NOT_STONKS'
        # when
        with patch('stonks.stonks.DataFetcher.fetch_data', return_value=pd.DataFrame()):
            fetcher = DataFetcher(asset)
            df = fetcher.fetch_data()
        # then
        assert df.empty, "Expected empty dataframe for invalid asset"

    def test_given_correct_asset_name_when_downloading_historical_data_then_non_empty_dataframe_is_returned(self):
        # given
        asset = 'EURUSD=X'
        fetcher = DataFetcher(asset)
        # when
        df = fetcher.fetch_data()

        # then
        assert not df.empty, "Expected non-empty dataframe for valid asset"
        expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        assert all(column in df.columns for column in expected_columns), "Expected columns missing from DataFrame"


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


class TestDataManipulator:

    def test_given_ohlc_historical_dataframe_when_calculating_indicators_then_is_dataframe_with_correct_data_returned(self):
        # given
        data = {
            'Close': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 29, 28, 27, 26]
        }
        df = pd.DataFrame(data)
        manipulator = DataManipulator(df)

        # when
        df_with_indicators = manipulator.add_indicators()

        # then
        expected_csv = StringIO(
            """Close,SMA,STD,Upper_Bollinger_Band,Lower_Bollinger_Band
            10,,,,
            11,,,,
            12,,,,
            13,,,,
            14,,,,
            15,,,,
            16,,,,
            17,,,,
            18,,,,
            19,,,,
            20,,,,
            21,,,,
            22,,,,
            23,,,,
            24,,,,
            25,,,,
            26,,,,
            27,,,,
            28,,,,
            29,19.5,5.916079783099616,31.33215956619923,7.667840433800768
            30,20.5,5.916079783099616,32.33215956619923,8.667840433800768
            29,21.4,5.761944116355173,32.92388823271035,9.876111767289652
            28,22.2,5.492578725210189,33.18515745042038,11.214842549579622
            27,22.9,5.139117270095078,33.178234540190154,12.621765459809843
            26,23.5,4.729526514634588,32.95905302926918,14.040946970730824
            """
        )
        expected_df = pd.read_csv(expected_csv)

        pd.testing.assert_frame_equal(df_with_indicators.reset_index(drop=True), expected_df.reset_index(drop=True))

    def test_bollinger_bands_with_short_history(self):
        # given
        data = {'Close': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]}
        df = pd.DataFrame(data)
        manipulator = DataManipulator(df)

        # when
        df_with_bollinger = manipulator.add_indicators()

        # then
        assert 'SMA' in df_with_bollinger.columns
        assert 'Upper_Bollinger_Band' in df_with_bollinger.columns
        assert 'Lower_Bollinger_Band' in df_with_bollinger.columns

        assert df_with_bollinger['SMA'].isna().all(), "SMA should be NaN for less than 20 data points"
        assert df_with_bollinger['Upper_Bollinger_Band'].isna().all(), "Upper Bollinger Band should be NaN for less than 20 data points"
        assert df_with_bollinger['Lower_Bollinger_Band'].isna().all(), "Lower Bollinger Band should be NaN for less than 20 data points"
