import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from datetime import datetime
import matplotlib.font_manager as fm

# 한글 폰트 설정 (크로스 플랫폼)
import platform
import os

if platform.system() == 'Windows':
    plt.rcParams['font.family'] = ['Malgun Gothic', 'sans-serif']
else:
    # Linux/Mac용 (Streamlit Cloud)
    try:
        # 폰트 캐시 재빌드
        fm._rebuild()
        # 사용 가능한 폰트 확인
        font_list = [f.name for f in fm.fontManager.ttflist]
        korean_fonts = [f for f in font_list if 'Nanum' in f or 'Gothic' in f]
        
        if korean_fonts:
            plt.rcParams['font.family'] = korean_fonts[0]
        else:
            # fallback
            plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
    except:
        plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
    
plt.rcParams['axes.unicode_minus'] = False

class ChartVisualizer:
    def __init__(self):
        self.colors = {
            'very_cheap': 'blue',
            'cheap': 'green', 
            'fair_value': 'yellow',
            'expensive': 'orange',
            'very_expensive': 'red',
            'no_data': 'gray'
        }
        
    def create_chart(self, data, ma_200w, zones_timeline, colors_timeline, ticker):
        fig, ax = plt.subplots(figsize=(14, 8))
        
        dates = data.index
        prices = data['Close']
        
        # 가격 라인을 세그먼트별로 나누어 색상 적용
        self._plot_colored_price_line(ax, dates, prices, colors_timeline)
        
        # 200주 이동평균선
        ax.plot(dates, ma_200w, color='black', linewidth=3, label='200W Moving Average', linestyle='--')
        
        # 범례용 더미 라인들 (색상 구간별)
        self._add_color_legend(ax)
        
        ax.set_yscale('log')
        ax.set_title(f'{ticker} Stock Timeline Analysis Chart', 
                    fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price (Log Scale)', fontsize=12)
        
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
    
    def _plot_colored_price_line(self, ax, dates, prices, colors_timeline):
        """가격 라인을 색상별로 나누어 그리기"""
        current_color = None
        start_idx = 0
        
        for i, color in enumerate(colors_timeline):
            if color != current_color:
                # 이전 세그먼트 그리기
                if current_color is not None and start_idx < i:
                    ax.plot(dates[start_idx:i+1], prices[start_idx:i+1], 
                           color=current_color, linewidth=1.5)
                
                current_color = color
                start_idx = i
        
        # 마지막 세그먼트 그리기
        if start_idx < len(dates):
            ax.plot(dates[start_idx:], prices[start_idx:], 
                   color=current_color, linewidth=1.5)
    
    def _add_color_legend(self, ax):
        """색상 구간별 범례 추가"""
        legend_labels = {
            'blue': 'Very Cheap (< 200W MA)',
            'green': 'Cheap (200W MA ~ 1.5x)',
            'yellow': 'Fair Value (1.5x ~ 2.0x)',
            'orange': 'Expensive (2.0x ~ 2.5x)',
            'red': 'Very Expensive (> 2.5x)',
            'gray': 'No Data'
        }
        
        for color, label in legend_labels.items():
            ax.plot([], [], color=color, linewidth=3, label=label)
    
    def _get_zone_korean(self, zone_name):
        zone_names = {
            'very_cheap': '매우 저렴',
            'cheap': '저렴',
            'fair_value': '적정가치',
            'expensive': '비싼편',
            'very_expensive': '매우 비쌈',
            'no_data': '데이터 없음'
        }
        return zone_names.get(zone_name, zone_name)
    
    def _get_zone_english(self, zone_name):
        zone_names = {
            'very_cheap': 'Very Cheap',
            'cheap': 'Cheap',
            'fair_value': 'Fair Value',
            'expensive': 'Expensive',
            'very_expensive': 'Very Expensive',
            'no_data': 'No Data'
        }
        return zone_names.get(zone_name, zone_name)