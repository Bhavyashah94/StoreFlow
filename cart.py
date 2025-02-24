import tkinter as tk


class CartPanel(tk.Frame):  
    def __init__(self, parent):
        super().__init__(parent)
        
        # Set background color for visualization (optional)
        self.config(bg="blue")  # Cart panel overall

        # Cart List 
        self.cart_list = tk.Frame(self, bg="white")  
        self.cart_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Cart Summary 
        self.cart_summary = tk.Frame(self, bg="#EDF2F4", width=600)
        self.cart_summary.pack(side=tk.RIGHT, fill=tk.Y)

        # cart_list_bottom bar
        self.cart_list_bottom = tk.Frame(self.cart_list, bg="#EDF2F4", height=100)
        self.cart_list_bottom.pack(side=tk.BOTTOM, fill=tk.X)
        self.cart_list_bottom.pack_propagate(False)

        # cart_list_bottom buttons
        self.clearcart_button = tk.Button(self.cart_list_bottom, text="Clear Cart", bg="#D90429", fg="white",
                                           relief=tk.FLAT, font=("Roboto", 12, "bold"), padx=10, pady=10, borderwidth=0)
        self.clearcart_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.holdcart_button = tk.Button(self.cart_list_bottom, text="Hold Cart", bg="#8D99AE", fg="white", 
                                         relief=tk.FLAT, font=("Roboto", 12), padx=10, pady=10, borderwidth=0)
        self.holdcart_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Add hover effects
        self.clearcart_button.bind("<Enter>", lambda e: self.clearcart_button.config(bg="#B22222"))
        self.clearcart_button.bind("<Leave>", lambda e: self.clearcart_button.config(bg="#D90429"))

        self.holdcart_button.bind("<Enter>", lambda e: self.holdcart_button.config(bg="#6C757D"))
        self.holdcart_button.bind("<Leave>", lambda e: self.holdcart_button.config(bg="#8D99AE"))