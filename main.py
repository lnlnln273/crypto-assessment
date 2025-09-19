from ohlcv import OHLSV
from indicators import TechnicalIndicators
from gemini_client import GeminiClient

ohlcv = OHLSV()
SYMBOL = input("Input coin/token symbol: ")
btc_ohlcv_data = ohlcv.get_data(SYMBOL.upper())

indicators = TechnicalIndicators(btc_ohlcv_data)
json_data = indicators.calculate_sonic_r(limit=30)

gemini_client = GeminiClient()
custom_prompt = ("Bạn là chuyên gia phân tích thị trường crypto, "
                 "bạn đang có nhiệm vụ là cập nhật nhanh tình hình thị trường crypto mỗi ngày cho cộng đồng."
            f"Dựa trên dữ liệu của {SYMBOL} cung cấp dưới định dạng json gồm có:"
            "open, high, low, close, volume, (pac_high, pac_low: gọi tắt là cụm Sonic R), ema89, ema200, sonic_signal"
            f"với timeframe tham chiếu là D1, hãy nhận định nhanh xu hướng của {SYMBOL} trong ngắn hạn. "
            "Phân tích ngắn gọn nhưng chi tiết, kèm cảnh báo rủi ro."
        )
r = gemini_client.analyze_market(json_data, custom_prompt)

print(r)
