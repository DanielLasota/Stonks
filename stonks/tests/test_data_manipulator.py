from io import StringIO

from stonks.stonks import DataManipulator
import pandas as pd


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