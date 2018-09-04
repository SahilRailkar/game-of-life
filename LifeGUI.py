import tkinter as tk
import LabelFrameView as lfv
import BooleanModel as bm
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename


"""Functions for the widgets in generate_frame and grid_frame"""


def open_file():
    """Opens the user-given *.txt file and sets the model and resets the view based on the data from the file."""
    file_name = askopenfilename(initialdir="/", title="Select file", filetypes=(("Text File", "*.txt"),))

    with open(file_name, 'r') as file:
        rc = file.readline().split(" ")

        new_grid = list()

        for row_num in range(int(rc[0])):
            cells = file.readline().split(" ")
            new_grid.append(list())
            for cell in cells:
                if cell == "X":
                    new_grid[row_num].append(model.alive)
                elif cell == "O":
                    new_grid[row_num].append(model.dead)

    model.grid = new_grid
    view.reset_cells()


def save_file():
    """Saves the current model and view to a *.txt file so they may be accessed again using the Open command."""
    file_name = asksaveasfilename(initialdir="/", title="Select file", filetypes=(("Text File", "*.txt"),))

    with open(file_name, 'w') as file1:
        print(str(len(model.grid)) + " " + str(len(model.grid[0])), file=file1)
        for row in range(len(model.grid)):
            for col in range(len(model.grid[0])):
                if model.grid[row][col] is model.alive:
                    print("X ", end='', file=file1)
                else:
                    print("O ", end='', file=file1)
            print(file=file1)


def generate_view():
    """Generates a model and a view corresponding to the user input in the tkinter Entry widgets at the top of
    LifeGUI."""
    try:
        num_of_rows = int(rows_input.get())
        num_of_cols = int(columns_input.get())

        if num_of_rows <= 0 or num_of_cols <= 0:
            popup_window(2)
        else:
            new_grid = list()
            for row in range(num_of_rows):
                new_grid.append(list())
                for col in range(num_of_cols):
                    new_grid[row].append(False)
            model.grid = new_grid
            model.generation = 0
            generation.configure(text="Generation " + str(model.generation))
            view.reset_cells()
    except ValueError:
        popup_window(1)


def popup_window(error_num):
    """Raises a pop-up window which displays an error message corresponding with the error made by the user."""
    pw = tk.Toplevel()
    pw.title("ERROR")

    error_frame = tk.Frame(pw)
    ok_frame = tk.Frame(pw, bg="#D3D3D3")

    if error_num == 1:
        error = tk.Label(error_frame, text="Invalid Input: Enter a valid number")
    else:
        error = tk.Label(error_frame, text="Invalid Input: Enter a number greater than or equal to 1")
    error.pack(padx=20, pady=10)
    ok = tk.Button(ok_frame, text="OK", highlightthickness=0, highlightbackground="#D3D3D3", command=pw.destroy)
    ok.pack(padx=10, pady=5, side=tk.RIGHT)

    error_frame.pack(fill=tk.BOTH, expand=True)
    ok_frame.pack(fill=tk.BOTH, expand=True)



"""Initializes the tkinter window."""
root = tk.Tk()
root.title("Conway's Game of Life GUI")


"""Creates a tkinter Menu widget with various commands."""
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)


"""Creates a tkinter Frame widget with two Entry widgets and a Button widget to generate various views in LifeGUI."""
generate_frame = tk.Frame(root, bg="#D3D3D3", padx=20, pady=20)
rows = tk.Label(generate_frame, text="# of Rows:", bg="#D3D3D3")
columns = tk.Label(generate_frame, text="# of Columns:", bg="#D3D3D3")
rows_input = tk.Entry(generate_frame, highlightthickness=0, highlightbackground="#D3D3D3")
columns_input = tk.Entry(generate_frame, highlightthickness=0, highlightbackground="#D3D3D3")
generate = tk.Button(generate_frame, text="Generate", highlightthickness=0, highlightbackground="#D3D3D3",
                     command=generate_view)
rows.pack(side=tk.LEFT, padx=(12, 0))
rows_input.pack(side=tk.LEFT, padx=(0, 25))
columns.pack(side=tk.LEFT)
columns_input.pack(side=tk.LEFT)
generate.pack(side=tk.LEFT, padx=(37, 0))


"""Creates a tkinter Frame widget which contains the LifeGUI's grid."""
grid_frame = tk.Frame(root, width=800, height=450, pady=100)
grid = [[False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, False, False]]
model = bm.BooleanModel(grid)
view = lfv.LabelFrameView(grid_frame)
view.set_model(model)
view.pack()





"""Functions for widgets in bottom_frame"""


def reset():
    """Resets the model and clears the view of LifeGUI."""
    model.set_false_color()
    model.generation = 0
    generation.configure(text="Generation " + str(model.generation))
    view.reset_cells()


def next_gen():
    """Updates the model and the view of LifeGUI to the next generation."""
    model.next_generation()
    view.reset_cells()
    generation.configure(text="Generation " + str(model.generation))


def change_size(size):
    """Changes the size of the cells to match the value displayed on the Cell Size Scale."""
    view.cell_size = int(size)
    view.reset_cells()



"""Creates a tkinter Frame widget which contains options which modify and update the LifeGUI grid."""
bottom_frame = tk.Frame(root, width=800, height=150, bg="#D3D3D3", padx=75, pady=15)

clear = tk.Button(bottom_frame, text="Clear", highlightthickness=0, highlightbackground="#D3D3D3", command=reset)
clear.configure(bg="red")
next_generation = tk.Button(bottom_frame, text="Next Generation", bg="#D3D3D3", highlightthickness=0,
                            highlightbackground="#D3D3D3", command=next_gen)

generation = tk.Label(bottom_frame, text="Generation " + str(model.generation), bg="#D3D3D3")

clear.grid(row=0, column=3, padx=(5, 10))
next_generation.grid(row=0, column=2, padx=(25, 5))

generation.grid(row=0, column=1, padx=(110, 25))

scale_frame = tk.Frame(bottom_frame, bg="#D3D3D3")
cell_size = tk.Scale(scale_frame, from_=0, to_=100, orient=tk.HORIZONTAL, bg="#D3D3D3", command=change_size)
cell_size.set(50)
cell_size_label = tk.Label(scale_frame, text="Cell Size", bg="#D3D3D3")
cell_size.grid(row=0, column=0, padx=(25, 0))
cell_size_label.grid(row=1, column=0, padx=(25, 0))
scale_frame.grid(row=0, column=0, padx=10)

generate_frame.pack(fill=tk.BOTH, expand=True)
grid_frame.pack()
bottom_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()


# def run_generations():
#     root.after(1, run_generations)
#     model.next_generation()
#     view.reset_cells()

# def toggle():
#     if run['text'] == "Run":
#         run.configure(text="Stop")
#         root.after(0.5, )
#
#         while run['text'] == "Stop":
#             print("meow")
#             model.next_generation()
#             view.reset_cells()
#
#     else:
#         run.configure(text="Run")

# run = tk.Button(bottom_frame, text="Run", bg="#D3D3D3", highlightthickness=0, highlightbackground="#D3D3D3",
# command=run_generations)

# run.grid(row=0, column=2, padx=10)