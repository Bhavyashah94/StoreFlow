from ui import StoreFlowUI
import ctypes
# Set DPI awareness for Windows
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Start the application
if __name__ == "__main__":
    app = StoreFlowUI()
    app.run()
