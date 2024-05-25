import tkinter as tk
from tkinter.ttk import *

binds = '''
<Button-1>
<Button-2>
<Button-3>
<Button-4>
<Button-5>
<Double-Button-1>
<Motion>
<Enter>
<Leave>
<MouseWheel>
<Key>
'''.strip().split('\n')


root = tk.Tk()

for sequence in binds:
    root.bind(sequence, lambda e: print(e))

root.mainloop()

