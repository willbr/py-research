
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
        self.vsb = ttk.Scrollbar(parent, orient="vertical", command=self._on_scroll)
        #self.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        
        # Bind the vertical scroll event
        self.bind("<MouseWheel>", self._on_mousewheel)
        #self.bind("<Configure>", self._on_configure)
        
        # Load initial data
        self.load_data()

        # Initialize the scrollbar to reflect the full dataset
        row_height = self.master.winfo_fpixels('1i')
        total_rows_visible = int(self.winfo_height() / row_height)
        self.vsb_page_size = total_rows_visible / self.total_items
        self.vsb.set(0, self.vsb_page_size)


    def load_data(self):
        #print('load_data')
        """Load a chunk of data into the treeview."""
        if self.loaded_items >= self.total_items:
            return
        
        end_item = min(self.loaded_items + self.load_size, self.total_items)
        
        for i in range(self.loaded_items, end_item):
            self.insert("", "end", text=f"Item {i}", values=(f"Value {i}",))
        
        self.loaded_items = end_item
        #print(end_item)

    def _on_scroll(self, *args):
        #print(f'on_scroll {args=}')
        """Handle the scrollbar movement."""

        assert args[0] == 'moveto'
        
        loaded_pc = self.loaded_items / self.total_items
        target_pc = float(args[1])

        if target_pc > loaded_pc:
            self._check_load_more(target_pc)

        target_of_loaded_pc = (target_pc * self.total_items) / self.loaded_items
        self.yview_moveto(target_of_loaded_pc)

        self.vsb.set(target_pc, target_pc + self.vsb_page_size)

    def _on_mousewheel(self, event):
        """Handle the mouse wheel scrolling."""
        if event.delta < 0:  # Scroll down
            self._check_load_more(0.01)

        unit_delta = int(-5*(event.delta/120))
        self.yview_scroll(unit_delta, what='units')
        delta_pc = unit_delta / self.total_items

        current_pc, _ = self.vsb.get()
        target_pc = current_pc + delta_pc 

        self._check_load_more(target_pc)

        self.vsb.set(target_pc, target_pc + self.vsb_page_size)

    def _check_load_more(self, target_pc):
        """Check if more data needs to be loaded."""

        while True:
            if self.loaded_items == self.total_items:
                break

            loaded_pc = self.loaded_items / self.total_items
            if target_pc < loaded_pc:
                break
        
            self.load_data()


# Main application
def main():
    root = tk.Tk()
    root.geometry("800x600")

    # Create a LazyLoadingTreeview
    total_items = 20000
    treeview = LazyLoadingTreeview(root, total_items, columns=("Value"))
    treeview.heading("#0", text="Item")
    treeview.heading("Value", text="Value")
    treeview.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()

