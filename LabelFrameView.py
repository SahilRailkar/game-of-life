import tkinter as tk
import BooleanModel
from PIL import Image
from PIL import ImageTk


class LabelFrameView(tk.LabelFrame):
    """LabelFrameView is a class which extends the LabelFrame widget from tkinter to simplify the construction of
    the view in LifeGUI."""

    def __init__(self, master, cell_size=50):
        """Constructs a LabelFrameView object.

        MODEL is the BooleanModel which holds the raw data behind the cells in LifeGUI.
        CELLS is a two-dimensional tkinter Label widget list and the view of LifeGUI.
        TILE_SIZE is the integer value of the length and width of each of the cells in LifeGUI.
        ALIVE_COLOR is the string variable which represents the color of a cell when it is alive.
        DEAD_COLOR is the string variable which represents the color of a cell when it is dead.
        """
        tk.LabelFrame.__init__(self, master, bd=1, relief="solid")
        self.model = None
        self.cells = None
        self.cell_size = cell_size
        self.alive_color = "red"
        self.dead_color = "white"

    def winfo_children(self) -> list:
        """Returns a list of the child widgets of the LabelFrameView object."""
        return super(LabelFrameView, self).winfo_children()

    def set_model(self, model: BooleanModel):
        """Sets the model of the LabelFrameView object and resets the view of LifeGUI to match it.

        MODEL is the BooleanModel which holds the raw data behind the cells in LifeGUI.
        """
        self.model = model
        self.reset_cells()

    def reset_cells(self):
        """Resets the view of LifeGUI to match with its corresponding model."""
        img = Image.new('RGB', (1, 1), (255, 255, 255))
        ph = ImageTk.PhotoImage(img)
        for child in LabelFrameView.winfo_children(self):
            child.destroy()
        self.cells = list()
        for row in range(len(self.model.grid)):
            self.cells.append(list())
            for col in range(len(self.model.grid[row])):
                if self.model.grid[row][col] is self.model.alive:
                    cell = tk.Label(master=self, image=ph, width=self.cell_size, height=self.cell_size, bg=self.
                                    alive_color, bd=1, relief="solid")
                    cell.bind("<Button-1>", left_click)
                    cell.bind("<Button-2>", right_click)
                    cell.bind("<B1-Motion>", left_click)
                    cell.bind("<B2-Motion>", right_click)
                    self.cells.append(cell)
                    cell.grid(row=row, column=col)
                else:
                    cell = tk.Label(master=self, image=ph, width=self.cell_size, height=self.cell_size, bg=self.
                                    dead_color, bd=1, relief="solid")
                    cell.bind("<Button-1>", left_click)
                    cell.bind("<Button-2>", right_click)
                    cell.bind("<B1-Motion>", left_click)
                    cell.bind("<B2-Motion>", right_click)
                    self.cells.append(cell)
                    cell.grid(row=row, column=col)


def right_click(event):
    """Handles the event of a right click on a cell."""
    caller_info = event.widget.grid_info()
    event.widget.master.model.grid[int(caller_info["row"])][int(caller_info["column"])] = event.widget.master.model.dead
    event.widget.master.reset_cells()


def left_click(event):
    """Handles the event of a left click on a cell."""
    caller_info = event.widget.grid_info()
    event.widget.master.model.grid[int(caller_info["row"])][int(caller_info["column"])] = event.widget.master.model.\
        alive
    event.widget.master.reset_cells()
