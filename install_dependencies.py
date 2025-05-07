import subprocess
import sys
import os

def install_dependencies():
    """Install all dependencies for the Inventory Management System including demand forecasting."""
    print("Installing dependencies for Inventory Management System...")
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("Error: requirements.txt not found.")
        return False
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        
        # Install dependencies from requirements.txt
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        
        print("All dependencies installed successfully!")
        print("\nDemand forecasting dependencies installed:")
        print("- pandas: Data manipulation and analysis library")
        print("- statsmodels: Statistical models and time series analysis")
        print("- scikit-learn: Machine learning library")
        print("\nYou can now run the application with demand forecasting functionality.")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

if __name__ == "__main__":
    install_dependencies() 