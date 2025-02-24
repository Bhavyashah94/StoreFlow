import tkinter as tk

class StoreFlowUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("StoreFlow")    
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda event: self.root.destroy())
        self.build_ui()

    def build_ui(self):

        # Top Bar
        self.top_bar = tk.Frame(self.root, height=50, bg='lightgrey')
        self.top_bar.pack(side=tk.TOP, fill=tk.X)

        # Main Content
        self.main_content = tk.Frame(self.root, bg='white')
        self.main_content.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Sidebar
        self.sidebar_width = 200   
        self.sidebar = tk.Frame(self.main_content, width=self.sidebar_width, bg='lightgrey')
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Sidebar Buttons size
        Sbutton_height = 20
        Sbutton_width = 50
        # Sidebar Buttons 
        button_texts = ['Cart', 'Inventory', 'Sales', 'Settings']
        self.buttons = {}
        for text in button_texts:
            button = tk.Button(self.sidebar, text=text, relief=tk.FLAT, bg='lightgrey', activebackground='lightgrey', height=2, width=15)
            button.pack(side=tk.TOP, fill=tk.X, pady=5)
            self.buttons[text] = button


        # Toggle Button
        self.toggle_button = tk.Button(self.top_bar, text='✖', command=self.toggle_sidebar,
                                       relief=tk.FLAT, bg='lightgrey', activebackground='lightgrey',
                                       padx=10, pady=10,borderwidth=0,highlightthickness=0)
        self.toggle_button.pack(side=tk.LEFT)

    def toggle_sidebar(self):
        if self.sidebar.winfo_viewable():
            self.sidebar.pack_forget()
            self.toggle_button.config(text='☰')
        else:
            self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
            self.toggle_button.config(text='✖')


    def run(self):
        self.root.mainloop()