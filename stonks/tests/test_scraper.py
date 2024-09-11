from io import StringIO
import pytest
import pandas as pd
from unittest.mock import patch

from stonks.scraper import Stonks


class TestScraper:

    def test_given_empty_dataframe_is_returned_when_passing_dataframe_then_exception_is_being_thrown(self):
        # given
        asset = 'INVALID_ASSET'
        # when
        with patch('stonks.scraper.Stonks.download_historical_data', return_value=pd.DataFrame()):
            # then
            with pytest.raises(ValueError):
                Stonks(asset)

    def test_given_incorrect_asset_name_when_downloading_historical_data_then_empty_dataframe_is_returned(self):
        # given
        asset = 'NOT_STONKS'
        # when
        df = Stonks.download_historical_data(asset)
        # then
        assert df.empty, "Expected empty dataframe for invalid asset"

    def test_given_correct_asset_name_when_downloading_historical_data_then_non_empty_dataframe_is_returned(self):
        # given
        asset = 'EURUSD=X'
        # when
        df = Stonks.download_historical_data(asset)

        #then
        assert not df.empty, "Expected non empty dataframe for valid asset"
        expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        assert all(column in df.columns for column in expected_columns), "Expected columns missing from DataFrame"

    def test_given_ohlc_historical_dataframe_when_calculating_indicators_then_is_dataframe_with_correct_data_returned(self):
        # given
        data = {
            'Close': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 29, 28, 27, 26]
        }
        df = pd.DataFrame(data)

        # when
        df_with_indicators = Stonks.calculate_indicators(df.copy())

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
            29,19.5,5.916,31.332,7.668
            30,20.5,5.916,32.332,8.668
            29,21.4,5.762,32.924,9.876
            28,22.2,5.493,33.186,11.214
            27,22.9,5.139,33.178,12.622
            26,23.5,4.730,32.960,14.040
            """
        )
        expected_df = pd.read_csv(expected_csv)

        pd.testing.assert_frame_equal(df_with_indicators.reset_index(drop=True), expected_df.reset_index(drop=True))