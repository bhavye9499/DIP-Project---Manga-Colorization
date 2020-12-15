import tkinter as tk

from src.globals import globals
from src.gui.windows.home import HomeWindow
from src.gui.windows.input_image import InputImageWindow
from src.gui.windows.output_image import OutputImageWindow

if __name__ == '__main__':
    root = tk.Tk()

    globals.home_window = HomeWindow(root)
    globals.input_image_window = InputImageWindow(root)
    globals.output_image_window = OutputImageWindow(root)

    globals.home_window.open_window()
