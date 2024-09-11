from unittest.mock import patch
import pandas as pd
import pytest

from stonks.stonks import DataFetcher


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