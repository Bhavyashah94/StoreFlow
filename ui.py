import tkinter as tk
from cart import CartPanel

class StoreFlowUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("StoreFlow")    
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda event: self.root.destroy())
        self.build_ui()

    def build_ui(self):
        # Top Bar
        self.top_bar = tk.Frame(self.root, height=70, bg='#2B2D42')
        self.top_bar.pack(side=tk.TOP, fill=tk.X)
        self.top_bar.pack_propagate(False)

        # Main Content
        self.main_area = tk.Frame(self.root, bg='white')
        self.main_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Sidebar (Initially Hidden)
        self.sidebar_width = 200   
        self.sidebar = tk.Frame(self.root, width=self.sidebar_width, bg='#8D99AE')

        # Sidebar buttons hover functions
        def on_enter(e):
            e.widget.config(bg='#D90429',fg='white')
        def on_leave(e):
            e.widget.config(bg='#8D99AE',fg='White')

        # Sidebar Buttons
        button_texts = ['Cart', 'Inventory', 'Sales', 'Settings']
        self.buttons = {}
        for text in button_texts:
            button = tk.Button(self.sidebar, text=text, relief=tk.FLAT, bg='#8D99AE',
                                fg='white', height=2, width=15, activebackground='#e78798',
                                borderwidth=0, highlightthickness=0)
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
            button.pack(side=tk.TOP, fill=tk.X, pady=0)
            self.buttons[text] = button
            
        # Toggle Button
        self.toggle_button = tk.Button(self.top_bar, text='☰', command=self.toggle_sidebar,
                                       relief=tk.FLAT, bg='#2B2D42', fg='#EDF2F4', activebackground='#8D99AE',
                                       height=2,width=6, borderwidth=0, highlightthickness=0, activeforeground='#EDF2F4')
        self.toggle_button.pack(side=tk.LEFT,pady=0)

        # Main Content (Placed inside main_area)
        self.main_content = tk.Frame(self.main_area, bg='white')
        self.main_content.pack(fill=tk.BOTH, expand=True)

        # Cart Panel
        self.cart_panel = CartPanel(self.main_content)
        self.cart_panel.pack(fill=tk.BOTH, expand=True)

    def toggle_sidebar(self):
        if self.sidebar.winfo_ismapped():
            self.sidebar.place_forget()  # Hide sidebar
            self.toggle_button.config(text='☰')
        else:
            self.sidebar.place(x=0, y=70, relheight=1, width=self.sidebar_width)  # Show sidebar on top
            self.toggle_button.config(text='✖')

    def run(self):
        self.root.mainloop()
