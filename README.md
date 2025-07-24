# Stock Timeline Value Analysis

A Streamlit web application that visualizes stock price movements with color-coded analysis based on the 200-week moving average. Unlike traditional charts that show static zones, this app dynamically colors the price line based on each time point's position relative to its 200-week moving average.

## Features

- **Timeline-based Color Analysis**: Stock prices are colored in real-time based on their position relative to the 200-week moving average at each point in time
- **Value Zone Classification**:
  - 🔵 **Very Cheap (Blue)**: Price < 200W Moving Average
  - 🟢 **Cheap (Green)**: 200W MA ≤ Price < 1.5 × 200W MA
  - 🟡 **Fair Value (Yellow)**: 1.5 × 200W MA ≤ Price < 2.0 × 200W MA
  - 🟠 **Expensive (Orange)**: 2.0 × 200W MA ≤ Price < 2.5 × 200W MA
  - 🔴 **Very Expensive (Red)**: Price ≥ 2.5 × 200W MA
- **Logarithmic Scale**: Y-axis uses log scale for better visualization of long-term trends
- **Popular Tickers**: Quick selection from popular stocks, ETFs, and cryptocurrencies
- **Zone Statistics**: Shows percentage of time spent in each value zone
- **Interactive Interface**: Clean Streamlit interface with Korean font support

## Installation

1. Clone this repository:
```bash
git clone https://github.com/jhyuk1214/stock_vis_timeline.git
cd stock_vis_timeline
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run main.py
```

2. Open your browser and navigate to the displayed local URL (typically `http://localhost:8501`)

3. Enter a stock ticker symbol or select from the popular options

4. View the timeline chart with color-coded price analysis

## Supported Assets

The app supports any ticker symbol available on Yahoo Finance, including:
- US Stocks (AAPL, MSFT, GOOGL, etc.)
- ETFs (SPY, QQQ, GLD, etc.)
- Cryptocurrencies (BTC-USD, ETH-USD, etc.)
- International stocks and indices

## Technical Details

- **Data Source**: Yahoo Finance via `yfinance` library
- **Moving Average**: 200-week (approximately 4-year) simple moving average
- **Chart Library**: Matplotlib with custom color segmentation
- **Time Period**: Default 10-year historical data

## Files Structure

- `main.py`: Streamlit web interface
- `stock_analyzer.py`: Core analysis logic and data processing
- `chart_visualizer.py`: Chart creation and visualization
- `requirements.txt`: Python dependencies
- `.gitignore`: Git ignore patterns

## Requirements

- Python 3.7+
- streamlit
- yfinance
- matplotlib
- pandas
- numpy

## License

This project is open source and available under the MIT License.