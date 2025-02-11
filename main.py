import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec

# Constants
UPDATE_INTERVAL = 60000  # 1 minute in milliseconds
SYMBOL = 'BTC-USD'
DATE_FORMAT = '%Y-%m-%d'  # Date format for the application title

# Initialize global variables
all_prices = pd.Series(dtype=float)
countdown_seconds = UPDATE_INTERVAL // 1000  # Seconds countdown for update interval

def fetch_data(symbol=SYMBOL, period='1d', interval='1m'):
    """Fetches recent data for the specified symbol and handles errors."""
    print("Fetching new data...")
    status_var.set("Updating prices...")
    root.update_idletasks()  # Refresh window to show update status

    try:
        data = yf.download(tickers=symbol, period=period, interval=interval)
        print("Data fetched:", data.head())
        
        # Select 'Close' column, ensure datetime index
        close_prices = data['Close'].copy()
        close_prices.index = pd.to_datetime(close_prices.index, errors='coerce').tz_localize(None)
        close_prices.dropna(inplace=True)  # Remove any NaT entries

        return close_prices.squeeze()
    except Exception as e:
        print(f"Error fetching data: {e}")
        status_var.set("Data fetch failed.")
        return pd.Series(dtype=float)
    finally:
        status_var.set(f"Prices updated. {countdown_seconds} seconds until next update.")
        start_countdown()

def update_table(prices):
    """Updates sidebar table with recent price data, including color-coding."""
    num_prices = 40 if root.state() == "zoomed" else 30
    recent_prices = prices[-num_prices:]  # Last `num_prices` entries, in ascending order

    # Clear table frame
    for widget in table_frame.winfo_children():
        widget.destroy()

    # Add headers
    tk.Label(table_frame, text="Time", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky="ew")
    tk.Label(table_frame, text="Price (USD)", font=('Arial', 10, 'bold')).grid(row=0, column=1, sticky="ew")

    # Display prices with color-coding
    prices_to_display = list(recent_prices[::-1].items())
    for i, (timestamp, price) in enumerate(prices_to_display):
        color = 'black'
        if i < len(prices_to_display) - 1:
            next_price = prices_to_display[i + 1][1]
            color = 'green' if price > next_price else 'red' if price < next_price else 'black'

        time_label = timestamp.strftime('%H:%M') if isinstance(timestamp, pd.Timestamp) else "Invalid Time"
        tk.Label(table_frame, text=time_label).grid(row=i+1, column=0, sticky="ew")
        tk.Label(table_frame, text=f"{price:.2f}", fg=color).grid(row=i+1, column=1, sticky="ew")

    last_updated_label.config(text=f"Last Updated: {datetime.now().strftime('%H:%M:%S')}")

def update_plots(prices):
    """Updates main plot area with price and trend data."""
    fig.clear()
    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 2])

    try:
        # Configure 20-minute and 60-minute charts
        configure_axis(fig.add_subplot(gs[0, 0]), prices[-20:], 'Last 20 Minutes', interval=5)
        configure_axis(fig.add_subplot(gs[0, 1]), prices[-60:], 'Last 60 Minutes', interval=10, sma_periods=[5, 10])

        # Full Time Period chart
        ax_full = fig.add_subplot(gs[1, :])
        ax_full.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plot_full_period(ax_full, prices)
        
        fig.tight_layout()
        canvas.draw()
    except Exception as e:
        print(f"Error updating plots: {e}")
        status_var.set("Error updating plots.")

def configure_axis(ax, data, title, interval, sma_periods=[5]):
    """Configures a chart with specified data range, title, and intervals."""
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=interval))
    ax.plot(data, label='Price', color='blue')
    
    for period in sma_periods:
        ax.plot(data.rolling(window=period).mean(), label=f'SMA {period}', linestyle='--')

    ax.set_title(title)
    ax.legend()

def plot_full_period(ax, prices):
    """Plots full time period with multiple SMAs."""
    ax.plot(prices, label='Price', color='blue')
    ax.plot(prices.rolling(window=5).mean(), label='SMA 5', color='orange')
    ax.plot(prices.rolling(window=10).mean(), label='SMA 10', color='green')
    ax.plot(prices.rolling(window=30).mean(), label='SMA 30', color='purple')
    ax.set_title('Full Time Period')
    ax.legend()

def refresh_data():
    """Fetches new data, updates the table and plots, and schedules the next update."""
    global all_prices
    new_prices = fetch_data()

    if not new_prices.empty:
        if not all_prices.empty:
            # Check if new data is from a new day; if so, reset the data.
            last_date = all_prices.index[-1].date()
            new_date = new_prices.index[-1].date()
            if new_date > last_date:
                all_prices = new_prices
            else:
                # Append only new entries that are not already present.
                new_data = new_prices[~new_prices.index.isin(all_prices.index)]
                all_prices = pd.concat([all_prices, new_data])
        else:
            all_prices = new_prices

        # Ensure the data is sorted by timestamp and remove any duplicate timestamps.
        all_prices = all_prices.sort_index()
        all_prices = all_prices[~all_prices.index.duplicated(keep='last')]

    update_table(all_prices)
    update_plots(all_prices)
    root.after(UPDATE_INTERVAL, refresh_data)

def countdown():
    """Counts down seconds until the next update."""
    global countdown_seconds
    if countdown_seconds > 0:
        countdown_seconds -= 1
        status_var.set(f"Prices updated. {countdown_seconds} seconds until next update.")
        root.after(1000, countdown)
    else:
        countdown_seconds = UPDATE_INTERVAL // 1000

def start_countdown():
    """Starts countdown after updating prices."""
    global countdown_seconds
    countdown_seconds = UPDATE_INTERVAL // 1000
    countdown()

def quit_app():
    """Closes the application."""
    root.quit()
    root.destroy()

def setup_ui():
    """Sets up the main UI components for the application."""
    root.title(f"Bitcoin Daily Price Trend Tracker - {datetime.now().strftime(DATE_FORMAT)}")

    window_width, window_height = 1280, 720
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    position_right = int((screen_width - window_width) / 2)
    position_down = int((screen_height - window_height) / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
    root.resizable(True, True)

    # Setup menu
    menu = tk.Menu(root)
    root.config(menu=menu)
    file_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Quit", command=quit_app)

    # Layout frames
    main_frame.pack(fill=tk.BOTH, expand=True)
    table_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    last_updated_label.pack()

    # Configure canvas size
    fig.set_size_inches(10, 8)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Initialize Tkinter components
root = tk.Tk()
main_frame = tk.Frame(root)
table_frame = tk.Frame(main_frame)
chart_frame = tk.Frame(main_frame)

# Status and Last Updated Labels
status_var = tk.StringVar(value="Ready")
status_label = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor="w", padx=10, pady=5)
last_updated_label = tk.Label(root, text="Last Updated: -")

# Pack status bar at the bottom with padding
status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

# Set up matplotlib figure and canvas
fig = plt.Figure()
canvas = FigureCanvasTkAgg(fig, master=chart_frame)

# Setup and start application
setup_ui()
refresh_data()
status_label.pack(side=tk.BOTTOM, fill=tk.X)
root.mainloop()
