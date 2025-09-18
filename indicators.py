import pandas as pd

class TechnicalIndicators:
    def __init__(self, ohlcv_json: dict):
        self.ohlcv_json = ohlcv_json

    def calculate_sonic_r(self, limit: int = 300):
        # Chuyển JSON sang DataFrame
        df = pd.DataFrame.from_dict(self.ohlcv_json, orient="index")
        df.index = pd.to_datetime(df.index)  # convert key -> datetime
        df = df.sort_index()  # sắp xếp theo thời gian

        # Đảm bảo dữ liệu là số
        df = df.astype(float)

        # Edit tên key dữ liệu
        df["open"] = df["1. open"]
        df["high"] = df["2. high"]
        df["low"] = df["3. low"]
        df["close"] = df["4. close"]
        df["volume"] = df["5. volume"]

        # EMA34 cho high/low
        df["pac_high"] = df["high"].ewm(span=34, adjust=False).mean()
        df["pac_low"] = df["low"].ewm(span=34, adjust=False).mean()

        # EMA89 và EMA200 cho trend filter
        df["ema89"] = df["close"].ewm(span=89, adjust=False).mean()
        df["ema200"] = df["close"].ewm(span=200, adjust=False).mean()

        # Logic tín hiệu đơn giản:
        # - Buy khi giá > dragon_high và close > ema89 & ema200, volume tăng
        # - Sell khi giá < dragon_low và close < ema89 & ema200, volume tăng
        signals = []
        for i in range(len(df)):
            if i < 1:
                signals.append("none")
                continue

            vol_up = df["volume"].iloc[i] > df["volume"].iloc[i - 1]

            if (df["close"].iloc[i] > df["pac_high"].iloc[i] and
                    df["close"].iloc[i] > df["ema89"].iloc[i] and
                    df["close"].iloc[i] > df["ema200"].iloc[i] and vol_up):
                signals.append("buy")
            elif (df["close"].iloc[i] < df["pac_low"].iloc[i] and
                  df["close"].iloc[i] < df["ema89"].iloc[i] and
                  df["close"].iloc[i] < df["ema200"].iloc[i] and vol_up):
                signals.append("sell")
            else:
                signals.append("none")

        df["sonic_signal"] = signals

        fields = [
            "open", "high", "low", "close", "volume",
            "pac_high", "pac_low", "ema89", "ema200", "sonic_signal"
        ]
        df_filtered = df[fields].dropna()
        # Lấy 300 ngày cuối
        df_limited = df_filtered.tail(limit)
        json_out = df_limited.to_dict(orient="index")
        json_out = {date.strftime("%Y-%m-%d"): values for date, values in json_out.items()}

        return json_out
