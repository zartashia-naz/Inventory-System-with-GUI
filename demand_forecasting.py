import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import MongoDBConnection
from datetime import datetime, timedelta
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings("ignore")

class DemandForecasting:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1150x650+220+130")
        self.root.title("Inventory Management System | Demand Forecasting")
        self.root.config(bg="white")
        self.root.focus_force()
        
        # Colors
        self.bg_color = "#0f4d7d"  # Dark blue
        self.accent_color = "#84C639"  # Green
        self.text_color = "white"
        
        # Initialize database connection
        self.db = MongoDBConnection()
        
        # Variables
        self.var_product = StringVar()
        self.var_forecast_period = IntVar(value=30)  # Default 30 days forecast
        self.var_forecast_model = StringVar(value="Exponential Smoothing")
        self.product_list = []
        
        # Title
        title = Label(self.root, text="Demand Forecasting", 
                     font=("times new roman", 30, "bold"), bg=self.bg_color, fg="white", padx=20)
        title.pack(side=TOP, fill=X)
        
        # Main content area
        main_frame = Frame(self.root, bg="white")
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Two-column layout
        left_frame = Frame(main_frame, bg="white", width=300)
        left_frame.pack(side=LEFT, fill=Y, padx=(0, 10))
        
        right_frame = Frame(main_frame, bg="white")
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # Controls Panel
        controls_panel = LabelFrame(left_frame, text="Forecasting Controls", 
                                  font=("Arial", 15, "bold"), bg="white", fg=self.bg_color)
        controls_panel.pack(fill=BOTH, expand=True)
        
        # Product Selection
        lbl_product = Label(controls_panel, text="Select Product", 
                           font=("Arial", 12), bg="white", fg=self.bg_color)
        lbl_product.pack(anchor=W, padx=15, pady=(15, 5))
        
        self.product_combo = ttk.Combobox(controls_panel, textvariable=self.var_product, 
                                         values=self.product_list, state="readonly", 
                                         font=("Arial", 12))
        self.product_combo.pack(fill=X, padx=15, pady=(0, 15))
        
        # Forecast Period
        lbl_period = Label(controls_panel, text="Forecast Period", 
                          font=("Arial", 12), bg="white", fg=self.bg_color)
        lbl_period.pack(anchor=W, padx=15, pady=(0, 5))
        
        period_frame = Frame(controls_panel, bg="white")
        period_frame.pack(fill=X, padx=15, pady=(0, 15))
        
        for days, text in [(7, "1 Week"), (30, "1 Month"), (60, "2 Months"), (90, "3 Months")]:
            Radiobutton(period_frame, text=text, variable=self.var_forecast_period, 
                       value=days, font=("Arial", 11), bg="white", 
                       fg=self.bg_color).pack(anchor=W, pady=2)
        
        # Model Selection
        lbl_model = Label(controls_panel, text="Forecast Model", 
                         font=("Arial", 12), bg="white", fg=self.bg_color)
        lbl_model.pack(anchor=W, padx=15, pady=(0, 5))
        
        model_frame = Frame(controls_panel, bg="white")
        model_frame.pack(fill=X, padx=15, pady=(0, 15))
        
        models = ["Exponential Smoothing", "ARIMA", "Moving Average"]
        for model in models:
            Radiobutton(model_frame, text=model, variable=self.var_forecast_model, 
                       value=model, font=("Arial", 11), bg="white",
                       fg=self.bg_color).pack(anchor=W, pady=2)
        
        # Button Frame
        btn_frame = Frame(controls_panel, bg="white")
        btn_frame.pack(fill=X, padx=15, pady=15)
        
        # Refresh and Forecast Buttons
        btn_refresh = Button(btn_frame, text="Refresh Products", 
                            font=("Arial", 12), bg="white", fg=self.bg_color, 
                            cursor="hand2", bd=1, command=self.load_products)
        btn_refresh.pack(fill=X, pady=(0, 10))
        
        btn_forecast = Button(btn_frame, text="Generate Forecast", 
                             font=("Arial", 12, "bold"), bg=self.bg_color, fg=self.bg_color, 
                             cursor="hand2", command=self.generate_forecast)
        btn_forecast.pack(fill=X)
        
        # Result Frame
        self.result_frame = LabelFrame(right_frame, text="Forecast Results", 
                                     font=("Arial", 15, "bold"), bg="white", fg=self.bg_color)
        self.result_frame.pack(fill=BOTH, expand=True)
        
        # Initialize canvas for plots
        self.create_plot_placeholder()
        
        # Load products initially
        self.load_products()
    
    def create_plot_placeholder(self):
        # Clear previous content
        for widget in self.result_frame.winfo_children():
            widget.destroy()
            
        placeholder_label = Label(self.result_frame, 
                                 text="Select a product and click 'Generate Forecast' to view predictions", 
                                 font=("Arial", 12), bg="white", fg=self.bg_color)
        placeholder_label.pack(pady=200)
    
    def load_products(self):
        """Load active products from database"""
        # Clear existing items
        self.product_list = []
        
        try:
            # Get products from database
            products = self.db.products.find({"status": "Active"})
            for product in products:
                self.product_list.append(product["name"])
                
            # Update combobox
            self.product_combo.config(values=self.product_list)
            self.var_product.set("Select Product")
            
            messagebox.showinfo("Success", "Product list refreshed successfully", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products: {str(e)}", parent=self.root)
    
    def get_sales_data(self, product_name, days=90):
        """Retrieve sales data for a specific product for the given number of days"""
        # Calculate start date
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Query MongoDB for sales of this product
        sales_data = []
        
        try:
            # Get all sales in the date range
            sales = self.db.sales.find({
                "date": {"$gte": start_date, "$lte": end_date}
            }).sort("date", 1)  # Sort by date ascending
            
            # Process each sale to find the product
            for sale in sales:
                for item in sale.get("items", []):
                    if item.get("product_name") == product_name:
                        sales_data.append({
                            "date": sale["date"],
                            "quantity": item["quantity"]
                        })
            
            # Convert to pandas DataFrame for analysis
            if sales_data:
                df = pd.DataFrame(sales_data)
                df["date"] = pd.to_datetime(df["date"])
                df.set_index("date", inplace=True)
                
                # Resample to daily level and fill missing values with 0
                daily_sales = df.resample('D').sum().fillna(0)
                return daily_sales
            else:
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve sales data: {str(e)}", parent=self.root)
            return None
    
    def generate_forecast(self):
        """Generate forecast based on historical sales data"""
        product_name = self.var_product.get()
        forecast_days = self.var_forecast_period.get()
        forecast_model = self.var_forecast_model.get()
        
        if product_name == "Select Product":
            messagebox.showerror("Error", "Please select a product", parent=self.root)
            return
        
        # Get historical sales data
        sales_data = self.get_sales_data(product_name)
        
        if sales_data is None or sales_data.empty:
            messagebox.showerror("Error", "No sales data available for this product", parent=self.root)
            return
        
        try:
            # Create forecast based on selected model
            forecast_values = None
            
            if forecast_model == "Exponential Smoothing":
                forecast_values = self.exponential_smoothing_forecast(sales_data, forecast_days)
            elif forecast_model == "ARIMA":
                forecast_values = self.arima_forecast(sales_data, forecast_days)
            elif forecast_model == "Moving Average":
                forecast_values = self.moving_average_forecast(sales_data, forecast_days)
            
            # Display forecast
            self.display_forecast(sales_data, forecast_values, product_name, forecast_model)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate forecast: {str(e)}", parent=self.root)
    
    def exponential_smoothing_forecast(self, sales_data, forecast_days):
        """Generate forecast using exponential smoothing"""
        # Fit the model
        model = ExponentialSmoothing(
            sales_data['quantity'], 
            trend='add', 
            seasonal='add', 
            seasonal_periods=7  # Weekly seasonality
        )
        model_fit = model.fit()
        
        # Make forecast
        forecast = model_fit.forecast(forecast_days)
        
        # Ensure forecast values are non-negative
        forecast = forecast.clip(lower=0)
        
        return forecast
    
    def arima_forecast(self, sales_data, forecast_days):
        """Generate forecast using ARIMA model"""
        # Fit ARIMA model (p,d,q) = (5,1,0)
        model = ARIMA(sales_data['quantity'], order=(5, 1, 0))
        model_fit = model.fit()
        
        # Make forecast
        forecast = model_fit.forecast(steps=forecast_days)
        
        # Ensure forecast values are non-negative
        forecast = forecast.clip(lower=0)
        
        return forecast
    
    def moving_average_forecast(self, sales_data, forecast_days):
        """Generate forecast using moving average"""
        # Calculate the rolling mean with a 7-day window
        sales_data['rolling_mean'] = sales_data['quantity'].rolling(window=7, min_periods=1).mean()
        
        # Get the last 7 days average
        last_7_days_avg = sales_data['rolling_mean'].iloc[-7:].mean()
        
        # Create forecast series
        date_range = pd.date_range(start=sales_data.index[-1] + timedelta(days=1), periods=forecast_days)
        forecast = pd.Series(data=last_7_days_avg, index=date_range)
        
        return forecast
    
    def display_forecast(self, historical_data, forecast_data, product_name, model_name):
        """Display forecast results with charts"""
        # Clear previous content
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Create a Figure
        fig = plt.Figure(figsize=(12, 8), dpi=100)
        
        # Create subplots
        ax1 = fig.add_subplot(211)  # Historical + Forecast
        ax2 = fig.add_subplot(223)  # Historical monthly pattern
        ax3 = fig.add_subplot(224)  # Weekly pattern
        
        # Plot 1: Historical + Forecast
        ax1.plot(historical_data.index, historical_data['quantity'], label='Historical Sales', color='#0f4d7d')
        ax1.plot(forecast_data.index, forecast_data, label='Forecast', color='#ff6b6b', linestyle='--')
        ax1.set_title(f'Demand Forecast for {product_name} using {model_name}')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Quantity')
        ax1.legend()
        ax1.grid(True)
        
        # Plot 2: Monthly pattern
        monthly_data = historical_data.resample('M').sum()
        ax2.bar(monthly_data.index.strftime('%b'), monthly_data['quantity'], color='#84C639')
        ax2.set_title('Monthly Sales Pattern')
        ax2.set_xlabel('Month')
        ax2.set_ylabel('Quantity')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True)
        
        # Plot 3: Weekly pattern
        historical_data['day_of_week'] = historical_data.index.dayofweek
        weekly_data = historical_data.groupby('day_of_week')['quantity'].mean()
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        ax3.bar(days, weekly_data, color='#FFC107')
        ax3.set_title('Average Sales by Day of Week')
        ax3.set_xlabel('Day of Week')
        ax3.set_ylabel('Avg Quantity')
        ax3.grid(True)
        
        # Forecast summary statistics
        total_forecast = forecast_data.sum()
        avg_forecast = forecast_data.mean()
        max_forecast = forecast_data.max()
        
        # Add forecast summary text
        forecast_days = len(forecast_data)
        summary_text = (
            f"Forecast Summary ({forecast_days} days):\n"
            f"Total Expected Demand: {total_forecast:.0f} units\n"
            f"Average Daily Demand: {avg_forecast:.1f} units\n"
            f"Peak Daily Demand: {max_forecast:.0f} units"
        )
        
        fig.text(0.5, 0.02, summary_text, ha='center', fontsize=12, bbox=dict(facecolor='#e9ecef', alpha=0.8))
        
        # Adjust layout
        fig.tight_layout(rect=[0, 0.05, 1, 0.95])
        
        # Embed plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.result_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=5, pady=5)

if __name__ == "__main__":
    root = Tk()
    obj = DemandForecasting(root)
    root.mainloop() 