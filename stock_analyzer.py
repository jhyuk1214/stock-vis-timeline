import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class StockAnalyzer:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(self.ticker)
    
    def get_weekly_data(self, period="max"):
        try:
            hist = self.stock.history(period=period, interval="1wk", auto_adjust=True, prepost=True)
            if hist.empty:
                hist = self.stock.history(period="5y", interval="1wk")
            if hist.empty:
                raise ValueError(f"No data found for ticker {self.ticker}. Please check if the ticker is correct.")
            return hist
        except Exception as e:
            raise ValueError(f"Failed to fetch data for ticker {self.ticker}: {str(e)}")
    
    def calculate_200w_ma(self, data):
        return data['Close'].rolling(window=200, min_periods=200).mean()
    
    def calculate_price_zones_timeline(self, data, ma_200w):
        """각 시점에서 200주 이동평균선 대비 가격 구간을 계산하고 색상을 반환"""
        zones_timeline = []
        colors_timeline = []
        
        # 색상 매핑
        zone_colors = {
            'very_cheap': 'blue',
            'cheap': 'green', 
            'fair_value': 'yellow',
            'expensive': 'orange',
            'very_expensive': 'red'
        }
        
        for i in range(len(data)):
            current_price = data['Close'].iloc[i]
            current_ma = ma_200w.iloc[i]
            
            if pd.isna(current_ma):
                zones_timeline.append('no_data')
                colors_timeline.append('gray')
                continue
            
            # 각 시점에서의 구간 계산
            if current_price < current_ma:
                zone = 'very_cheap'
            elif current_price < current_ma * 1.5:
                zone = 'cheap'
            elif current_price < current_ma * 2.0:
                zone = 'fair_value'
            elif current_price < current_ma * 2.5:
                zone = 'expensive'
            else:
                zone = 'very_expensive'
            
            zones_timeline.append(zone)
            colors_timeline.append(zone_colors[zone])
        
        return zones_timeline, colors_timeline
    
    def calculate_price_zones(self, current_price, ma_200w):
        """현재 가격 기준 구간 계산 (기존 호환성 유지)"""
        latest_ma = ma_200w.iloc[-1]
        
        zones = {
            'very_cheap': (0, latest_ma),
            'cheap': (latest_ma, latest_ma * 1.5),
            'fair_value': (latest_ma * 1.5, latest_ma * 2.0),
            'expensive': (latest_ma * 2.0, latest_ma * 2.5),
            'very_expensive': (latest_ma * 2.5, float('inf'))
        }
        
        return zones, latest_ma
    
    def get_current_zone(self, current_price, zones):
        for zone_name, (lower, upper) in zones.items():
            if lower <= current_price < upper:
                return zone_name
        return 'very_expensive'