
# Bitcoin Daily Price Trend App

A Python application that tracks the price and trend of Bitcoin (BTC) in GBP. This project leverages **Tkinter** for the graphical user interface and **yfinance**, **Pandas**, and **Matplotlib** for data handling and visualization.

## Features

- **Live Price Updates**: 
  - Displays the latest BTC-GBP price in the sidebar, updated every 60 seconds.
  - Prices are color-coded for quick reference:
    - **Green**: Price increased compared to the previous update.
    - **Red**: Price decreased compared to the previous update.

- **Interactive Charts**:
  1. **20-Minute Chart**:
     - Visualizes Bitcoin's price and trend over the last 20 minutes.
     - Includes a simple moving average (SMA) for better trend readability.
  2. **60-Minute Chart**:
     - Provides an overview of the past hour with SMAs (5 and 10) alongside the price.
  3. **Daily Chart**:
     - Displays Bitcoin's price and trend from midnight to the current time.
     - Uses SMAs (5, 10, and 30) to enhance trend visibility.

- **Status Bar Timer**:
  - Countdown to the next price update ensures you’re always aware of the refresh schedule.

## Installation

1. Clone this repository:
   ```
      git clone https://github.com/your-username/bitcoin-daily-price-trend-app.git
   ```
2. Navigate to the project directory:
   ```
   cd bitcoin-daily-price-trend-app
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python3 main.py
   ```
2. Explore the live Bitcoin price updates, interactive charts, and price trends.

## Learning Outcomes

This project was a valuable learning experience, covering:
- Building GUIs with **Tkinter**.
- Data analysis and manipulation with **Pandas**.
- Visualizing financial data using **Matplotlib**.
- Fetching live cryptocurrency data with **yfinance**.

## Technologies Used

- **Python**: Core programming language.
- **Tkinter**: For building the graphical user interface.
- **Pandas**: Data manipulation and analysis.
- **Matplotlib**: Charting and visualization.
- **yfinance**: Fetching live price data for Bitcoin.