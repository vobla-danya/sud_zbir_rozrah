# Шо для розрахунку треба:
# Спитати який рік, в залежності від цього застосувати константу
# Спитати кількість зобовʼязальних вимог, відносно цього множити
# Уточнити, чи це апеляція, чи касація і в залежності від цього застосувати коефіцієнт
# Помножити на 0.8 бо це через систему електронний суд
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

PROZHITKOVY_MINIMUM = {
    2024: 1211.20,
    2025: 1211.20,
    2026: 1331.20
}

INSTANTSIA_KOEF = {
    1: 1,
    2: 1.5,
    3: 2
}

ELEKTRONNUI_SUD_KOEF = 0.8

def rozrahunok(rik: int, vymogy: int, inst: int, use_el_sud: bool = True) -> Optional[float]:
    try:
        if rik < 100:
            rik = 2000 + rik

        if rik not in PROZHITKOVY_MINIMUM:
            raise ValueError(f"Прожитковий мінімум для {rik} не задано.")

        if inst not in INSTANTSIA_KOEF:
            raise ValueError("Некоректна інстанція")

        prozhitk = PROZHITKOVY_MINIMUM[rik]
        instantzia = INSTANTSIA_KOEF[inst]
        el_sud_koef = ELEKTRONNUI_SUD_KOEF if use_el_sud else 1.0

        result = prozhitk * instantzia * vymogy * el_sud_koef
        return result
    except Exception as e:
        raise e

class CourtFeeCalcApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Розрахунок судового збору")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.theme_use('clam')

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title_label = tk.Label(
            main_frame,
            text="Розрахунок судового збору",
            font=("Arial", 18, "bold"),
            fg="#ffffff",
            background="black"
        )
        title_label.grid(row = 0, column = 0, columnspan=2, pady=(0, 20))

        ttk.Label(main_frame, text="Оберіть рік позовного провадження: ", font=("Arial", 11)).grid(
            row=1, column=0, sticky=tk.W, pady=10
        )
        self.rik_var = tk.StringVar(value="2025")
        rik_combo = ttk.Combobox(
            main_frame,
            textvariable=self.rik_var,
            values=list(PROZHITKOVY_MINIMUM.keys()),
            state="readonly",
            width=25,
            font=("Arial", 10)
        )
        rik_combo.grid(row = 1, column = 1, sticky=tk.W, pady=10)

        ttk.Label(main_frame, text="Кількість зобовʼязальних вимог: ", font=("Arial", 11)).grid(
            row = 2, column = 0, sticky=tk.W, pady=10
        )
        self.vymog_var = tk.StringVar(value="1")
        vymog_spinbox = ttk.Spinbox(
            main_frame,
            from_= 1,
            to=100,
            textvariable=self.vymog_var,
            width=24,
            font=("Arial", 10)
        )
        vymog_spinbox.grid(row=2, column=1, sticky=tk.W, pady=10)

        ttk.Label(main_frame, text="Інстанція: ", font=("Arial", 11)).grid(
            row=3, column=0, sticky=tk.W, pady=10
        )
        self.insta_var = tk.StringVar(value="1")
        insta_combo = ttk.Combobox(
            main_frame,
            textvariable=self.insta_var,
            values=list(INSTANTSIA_KOEF.keys()),
            state="readonly",
            width=25,
            font=("Arial", 10)
        )
        insta_combo.grid(row=3, column=1, sticky=tk.W, pady=10)

        el_sud_label = tk.Label(
            main_frame,
            text="Коефіцієнт Електронного суду: 0.8",
            font=("Arial", 10, "italic"),
            fg="#27ae60"
        )
        el_sud_label.grid(row = 4, column=0, columnspan=2, pady=10)

        calc_button = tk.Button(
            main_frame,
            text="РОЗРАХУВАТИ",
            command=self.calculate,
            bg="#3498db",
            fg="black",
            font=("Arial", 12, "bold"),
            cursor = "hand2",
            relief = tk.FLAT,
            padx=20,
            pady=10
        )
        calc_button.grid(row=5, column=0, columnspan=2, pady=20)

        result_frame = tk.LabelFrame(
            main_frame,
            text="Деталі розрахунку",
            font = ("Arial", 11, "bold"),
            fg="#ffffff",
            padx=15,
            pady=15
        )
        result_frame.grid(row = 6, column = 0, columnspan = 2, sticky=(tk.W, tk.E), pady=10)

        self.result_text = tk.Text(
            result_frame,
            height = 10,
            width = 55,
            font=("Courier New", 10),
            bg="#194685",
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.result_text.pack()

        clear_button = tk.Button(
            main_frame,
            text="Очистити",
            command=self.clear_result,
            bg="#95a5a6",
            fg="black",
            font=("Arial", 10),
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            pady=5
        )
        clear_button.grid(row=7, column=0, columnspan=2, pady=5)

    def calculate(self):
        try:
            rik = int(self.rik_var.get())
            kilk_vymog = int(self.vymog_var.get())
            instanzia = int(self.insta_var.get())

            if kilk_vymog < 1:
                messagebox.showerror("Помилка", "Кількість вимог має бути більше 0")
                return

            zbir = rozrahunok(rik, kilk_vymog, instanzia, True)

            rik = PROZHITKOVY_MINIMUM[rik]
            instanzia = INSTANTSIA_KOEF[instanzia]

            result_text = f"""
{'=' *50}
    СУДОВИЙ ЗБІР: {zbir: .2f} грн
{'=' *50}
                    """

            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, result_text)
            self.result_text.config(state=tk.DISABLED)

        except ValueError as e:
            messagebox.showerror("Помилка", f"Помилка введення: {e}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Несподівана помилка: {e}")

    def clear_result(self):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = CourtFeeCalcApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

