
import tkinter as tk
from tkinter import ttk

class LazyLoadingTreeview(ttk.Treeview):
    def __init__(self, parent, total_items, load_size=100, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Parameters
        self.total_items = total_items
        self.load_size = load_size
        self.loaded_items = 0
        
        # Setup vertical scrollbar
        vsb = ttk.Scrollbar(parent, orient="vertical", command=self._on_scroll)
        self.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        
        # Bind the vertical scroll event
        self.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<Configure>", self._on_configure)
        
        # Load initial data
        self.load_data()

        # Initialize the scrollbar to reflect the full dataset
        self.update_scrollbar()

    def load_data(self):
        """Load a chunk of data into the treeview."""
        if self.loaded_items >= self.total_items:
            return
        
        end_item = min(self.loaded_items + self.load_size, self.total_items)
        
        for i in range(self.loaded_items, end_item):
            self.insert("", "end", text=f"Item {i}", values=(f"Value {i}",))
        
        self.loaded_items = end_item

    def _on_scroll(self, *args):
        """Handle the scrollbar movement."""
        self.yview(*args)
        
        # Check if more data needs to be loaded when scrolling down
        if args[0] == 'moveto' and float(args[1]) > 0.95:  # Close to the bottom
            self._check_load_more()

    def _on_mousewheel(self, event):
        """Handle the mouse wheel scrolling."""
        if event.delta < 0:  # Scroll down
            self._check_load_more()
        self.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _on_configure(self, event):
        """Check if more data needs to be loaded when the treeview is resized."""
        self._check_load_more()

    def _check_load_more(self):
        """Check if more data needs to be loaded."""
        # Get the total number of visible rows
        total_rows_visible = int(self.winfo_height() / self.master.winfo_fpixels('1i'))
        
        # If we're close to the end and more items can be loaded, load more data
        if self.loaded_items < self.total_items:
            self.load_data()
            self.update_scrollbar()

    def update_scrollbar(self):
        """Update the scrollbar to reflect the full dataset, even though not all items are loaded."""
        fraction_of_items_loaded = self.loaded_items / self.total_items
        self.yview_moveto(fraction_of_items_loaded)

# Main application
def main():
    root = tk.Tk()
    root.geometry("400x300")

    # Create a LazyLoadingTreeview
    total_items = 200000
    treeview = LazyLoadingTreeview(root, total_items, columns=("Value"))
    treeview.heading("#0", text="Item")
    treeview.heading("Value", text="Value")
    treeview.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
