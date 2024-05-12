import tkinter as tk
import random
import math


class DiceRollerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("D&D Dice Roller")

        self.dice_options = ["d4", "d6", "d8", "d10", "d12", "d20"]
        self.dice_shapes = {"d4": 3, "d6": 4, "d8": 4, "d10": 10, "d12": 10, "d20": 6}

        self.label = tk.Label(master, text="Choose a dice to roll:")
        self.label.pack()

        self.dice_var = tk.StringVar()
        self.dice_var.set(self.dice_options[0])

        self.dice_menu = tk.OptionMenu(master, self.dice_var, *self.dice_options)
        self.dice_menu.pack()

        self.num_dice_label = tk.Label(master, text="Number of dice:")
        self.num_dice_label.pack()

        self.num_dice_entry = tk.Entry(master, width=5)
        self.num_dice_entry.insert(0, "1")
        self.num_dice_entry.pack()

        self.roll_button = tk.Button(master, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack()

        self.canvas = tk.Canvas(master, width=200, height=200)
        self.canvas.pack()

        self.result_label = tk.Label(self.canvas, text="", font=("Helvetica", 16))
        self.result_label.place(relx=0.5, rely=0.5, anchor="center")

        self.log_text = tk.Text(master, width=40, height=10)
        self.log_text.pack(side="left")
        self.log_scrollbar = tk.Scrollbar(master, orient="vertical", command=self.log_text.yview)
        self.log_scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=self.log_scrollbar.set)

    def roll_dice(self):
        selected_dice = self.dice_var.get()
        sides = int(selected_dice[1:])
        num_dice = int(self.num_dice_entry.get())

        dice_shape = self.dice_shapes[selected_dice]

        dice_rolls = [self.roll_dice_result(sides) for _ in range(num_dice)]
        result = sum(dice_rolls)
        self.animate_dice_roll(dice_shape, result)

        self.log_result(selected_dice, num_dice, dice_rolls, result)

    def roll_dice_result(self, sides):
        return random.randint(1, sides)

    def animate_dice_roll(self, sides, result):
        self.draw_dice(sides, result)
        

    def draw_dice(self, sides, result):
        self.canvas.delete("dice")

        if result:
            self.result_label.config(text="", background="white")

        x_center, y_center = 100, 100
        radius = 50
        angle = (360 / sides) * math.pi / 180
        starting_angle = math.pi / 2

        points = []
        for i in range(sides):
            x = x_center + radius * math.cos(starting_angle + i * angle)
            y = y_center + radius * math.sin(starting_angle + i * angle)
            points.extend([x, y])

        self.canvas.create_polygon(
            points, fill="white", outline="black", width=2, tags="dice"
        )

        self.rotate_dice(sides, 20)

        if result:
            self.result_label.config(text=str(result))

    def rotate_dice(self, sides, iterations):
        angle_offset = 0
        x_center, y_center = 100, 100
        radius = 50
        angle = (360 / sides) * math.pi / 180
        starting_angle = math.pi / 2

        for _ in range(iterations):
            self.canvas.delete("dice")

            points = []
            for i in range(sides):
                x = x_center + radius * math.cos(
                    starting_angle + i * angle + angle_offset
                )
                y = y_center + radius * math.sin(
                    starting_angle + i * angle + angle_offset
                )
                points.extend([x, y])

            self.canvas.create_polygon(
                points, fill="white", outline="black", width=2, tags="dice"
            )
            angle_offset += 0.2
            self.master.update_idletasks()  # update the GUI
            self.master.after(50)  # wait 50ms before next iteration

    def log_result(self, selected_dice, num_dice, dice_rolls, result):
        results = "+".join(map(str, dice_rolls))
        self.log_text.insert("end", f"Rolled {str(num_dice)}{selected_dice}: {results} = {result}\n")
        self.log_text.see("end")  # scroll to the end


def main():
    root = tk.Tk()
    app = DiceRollerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()