import tkinter as tk
from tkinter import Menu, Frame
from PIL import Image, ImageDraw
from data_handler import save_training_image, load_training_data
from model_handler import train_model, predict_digit


class DigitRecognizerApp:
    def __init__(self, root):
        self.root = root
        self.training_data_folder = "training_data"
        self.model = None
        self.last_prediction = None
        self.mode = "Train"

        self.root.title("Digit Recognizer")
        self.root.geometry("600x400")
        self.root.config(bg="#2e3b4e")

        self.setup_menu()
        self.setup_gui()

    def setup_menu(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        mode_menu = Menu(menu_bar, tearoff=0)
        mode_menu.add_command(label="Train", command=self.switch_to_train_mode)
        mode_menu.add_command(label="Test", command=self.switch_to_test_mode)
        menu_bar.add_cascade(label="Mode", menu=mode_menu)

    def setup_gui(self):
        main_frame = Frame(self.root, bg="#2e3b4e")
        main_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)

        self.canvas = tk.Canvas(main_frame, width=280, height=280, bg="black", cursor="cross", highlightthickness=2, highlightbackground="white")
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        self.image = Image.new("L", (280, 280), color=0)
        self.draw_obj = ImageDraw.Draw(self.image)

        control_frame = Frame(main_frame, bg="#2e3b4e")
        control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.output_label = tk.Label(control_frame, text="Prediction:", font=("Comic Sans MS", 18), fg="white", bg="#2e3b4e")
        self.output_label.pack(pady=5)

        self.predicted_digit_label = tk.Label(control_frame, text="", font=("Comic Sans MS", 36, "bold"), fg="#ffa726", bg="#2e3b4e")
        self.predicted_digit_label.pack(pady=5)

        self.label = tk.Label(control_frame, text="Enter the digit you drew:", font=("Comic Sans MS", 12), fg="white", bg="#2e3b4e")
        self.label.pack(pady=10)

        self.digit_entry = tk.Entry(control_frame, font=("Comic Sans MS", 16), justify="center", bd=3, relief="ridge")
        self.digit_entry.pack(pady=5)

        self.submit_button = tk.Button(control_frame, text="Submit", command=self.submit_canvas, font=("Comic Sans MS", 14), bg="#00bcd4", fg="white", relief="flat", padx=10, pady=5)
        self.submit_button.pack(pady=10)

        self.correct_button = tk.Button(control_frame, text="Correct", command=self.save_correct_prediction, font=("Comic Sans MS", 14), bg="#4caf50", fg="white", relief="flat", padx=10, pady=5)
        self.correct_button.pack(pady=10)
        self.correct_button.pack_forget()

        self.clear_button = tk.Button(main_frame, text="Clear", command=self.clear_canvas, font=("Comic Sans MS", 14), bg="#f44336", fg="white", relief="flat", padx=10, pady=5)
        self.clear_button.grid(row=1, column=0, pady=10)

        self.canvas.bind("<B1-Motion>", self.draw)

    def draw(self, event):
        x, y = event.x, event.y
        radius = 3
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="white", outline="white")
        self.draw_obj.ellipse([x - radius, y - radius, x + radius, y + radius], fill=255)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw_obj.rectangle([0, 0, 280, 280], fill=0)
        self.predicted_digit_label.config(text="")

    def submit_canvas(self):
        if self.mode == "Train":
            digit = self.digit_entry.get().strip()
            if digit.isdigit() and int(digit) in range(10):
                save_training_image(self.image, digit, self.training_data_folder)
            self.clear_canvas()
            self.digit_entry.delete(0, tk.END)
        elif self.mode == "Test":
            if not self.model:
                return
            resized_image = self.image.resize((28, 28))
            self.last_prediction = predict_digit(resized_image, self.model)
            self.predicted_digit_label.config(text=str(self.last_prediction))

    def save_correct_prediction(self):
        if self.last_prediction is not None:
            save_training_image(self.image, str(self.last_prediction), self.training_data_folder)
            self.clear_canvas()

    def switch_to_train_mode(self):
        self.mode = "Train"
        self.label.pack()
        self.digit_entry.pack(pady=5)
        self.submit_button.config(text="Submit")
        self.correct_button.pack_forget()

    def switch_to_test_mode(self):
        self.model = train_model(self.training_data_folder)
        self.mode = "Test"
        self.label.pack_forget()
        self.digit_entry.pack_forget()
        self.submit_button.config(text="Predict")
        self.correct_button.pack()


