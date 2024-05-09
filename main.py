#Code by Jabulani Lubisi.

from tkinter import *
import customtkinter #for building modern web interfaces

# Theme settings
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class BMIIndex(customtkinter.CTk):#Window

    def __init__(self):
        super().__init__()

        self.height_inches = None
        self.weight_pounds = None
        self.height_meters = None
        self.weight_kilos = None
        self.bmi = None

        # Title
        self.title("BMI Calculator App")
        self.geometry('640x410')
        self.resizable(False, False)
        self.grid()

        # Create multiple frame
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # App frames
        frame_left = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        frame_left.grid(row=0, column=0, sticky="nswe")

        frame_right = customtkinter.CTkFrame(master=self)
        frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        # Labels for app
        label_left = customtkinter.CTkLabel(master=frame_left, text="BMI Calculator App",
                                            font=customtkinter.CTkFont(weight="bold", size=18),
                                            justify=customtkinter.LEFT)
        label_left.place(relx=0.5, rely=0.15, anchor="center")

        label_right_01 = customtkinter.CTkLabel(master=frame_right, text="Enter your height in Ms: ",
                                                font=customtkinter.CTkFont(size=12),
                                                justify=customtkinter.LEFT)
        label_right_01.place(relx=0.5, rely=0.07, anchor="center")

        label_right_02 = customtkinter.CTkLabel(master=frame_right, text="Enter your weight in Kgs: ",
                                                font=customtkinter.CTkFont(size=12),
                                                justify=customtkinter.LEFT)
        label_right_02.place(relx=0.5, rely=0.35, anchor="center")

        label_right_03 = customtkinter.CTkLabel(master=frame_right, text="Your Body Mass Index is: ",
                                                font=customtkinter.CTkFont(size=12),
                                                justify=customtkinter.LEFT)
        label_right_03.place(relx=0.5, rely=0.63, anchor="center")

        label_right_04 = customtkinter.CTkLabel(master=frame_right, text="According to the BMI, You are ",
                                                font=customtkinter.CTkFont(size=12),
                                                justify=customtkinter.LEFT)
        label_right_04.place(relx=0.5, rely=0.8, anchor="center")

        self.label_right_05 = customtkinter.CTkLabel(master=frame_right, text="",
                                                     font=customtkinter.CTkFont(size=12),
                                                     justify=customtkinter.LEFT)
        self.label_right_05.place(relx=0.75, rely=0.8, anchor="center")

        # Buttons
        button_right = customtkinter.CTkButton(master=frame_right, text="Calculate", command=self.display_bmi)
        button_right.place(relx=0.5, rely=0.9, anchor="center")

        # Text inside the textbox
        self.entry_right_01 = customtkinter.CTkEntry(master=frame_right, width=180, height=30,
                                                     placeholder_text="Your height in Ms",
                                                     font=customtkinter.CTkFont(size=12))
        self.entry_right_01.pack(pady=40, padx=10)

        self.entry_right_02 = customtkinter.CTkEntry(master=frame_right, width=180, height=30,
                                                     placeholder_text="Your weight in Kgs",
                                                     font=customtkinter.CTkFont(size=12))
        self.entry_right_02.pack(pady=40, padx=10)

        self.entry_right_03 = customtkinter.CTkEntry(master=frame_right, width=180, height=30,
                                                     font=customtkinter.CTkFont(size=12))
        self.entry_right_03.pack(pady=40, padx=10)

        # Appearances
        self.appearance_mode_label = customtkinter.CTkLabel(master=frame_left, text="Theme:")
        self.appearance_mode_label.grid(row=1, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_label.place(relx=0.5, rely=0.27, anchor="center")
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(master=frame_left,
                                                                      values=["Light", "Dark", "System"],
                                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_optionmenu.grid(row=2, column=0, padx=10, pady=(10, 10))
        self.appearance_mode_optionmenu.place(relx=0.5, rely=0.35, anchor="center")

    # Using the user appearance as a method; not a function in the class
    @staticmethod
    def change_appearance_mode_event(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # Calculate the Body Mass Index with using Height & Weight math formula
    def bmi_calculate(self):
        try:
            self.height_meters = float(self.height_inches * 1)
            self.weight_kilos = float(self.weight_pounds * 1)
            self.bmi = self.weight_kilos / (self.height_meters ** 2)
        except ValueError:
            self.bmi = "Invalid input!"

    # Prints out the Body Mass Index results
    def display_bmi(self):
        try:
            self.height_inches = float(self.entry_right_01.get())
            self.weight_pounds = float(self.entry_right_02.get())
        except ValueError:
            self.entry_right_03.delete(0, END)
            self.entry_right_03.insert(END, "Invalid input!")
        self.bmi_calculate()
        self.entry_right_03.delete(0, END)
        self.entry_right_03.insert(END, self.bmi)
        result_status = self.get_status()
        self.label_right_05.configure(text=result_status)

    # Prints out the string results from the BMI results
    def get_status(self):
        if self.bmi is None:
            return " "

        elif self.bmi < 16:
            return "anorexic"

        elif self.bmi < 18.5:
            return "underweight"

        elif self.bmi < 25:
            return "healthy"

        elif self.bmi < 30:
            return "overweight"

        else:
            return "obese"

# This is run the script directly. Not when the script is imported from one module to another script.
if __name__ == "__main__":
    bmi_index = BMIIndex()
    bmi_index.mainloop()

    
