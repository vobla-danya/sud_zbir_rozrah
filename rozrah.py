import sys
import os
import customtkinter as ctk
from tkinter import messagebox
import tomllib

#Отримуємо шлях до директорії шрифтів
def get_fonts_dir() -> str:
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), 'fonts')
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')

#Завантажуємо шрифт
def load_uaf_fonts():
    try:
        import pyglet
        fonts_dir = get_fonts_dir()
        for fname in os.listdir(fonts_dir):
            if fname.lower().endswith('.ttf'):
                pyglet.font.add_file(os.path.join(fonts_dir, fname))
    except Exception:
        pass  

load_uaf_fonts()

#Отримуємо шлях до конфігу
def get_config_path() -> str:
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base, 'config.toml')

def load_config() -> dict:
    path = get_config_path()
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        return DEFAULT_CONFIG
    except tomllib.TOMLDecodeError:
        messagebox.showerror("Помилка", "Файл config.toml пошкоджений.")
        return DEFAULT_CONFIG


DEFAULT_CONFIG = {
    "PROZHITKOVY_MINIMUM": {
        "2024": 1211.20,
        "2025": 1211.20,
        "2026": 1331.20
    },
    "INSTANTSIA_KOEF": {
        "1": 1.0,
        "2": 1.5,
        "3": 2.0
    },
    "ELEKTRONNUI_SUD_KOEF": 0.8
}

#Завантаження значень з config.toml
config = load_config()

PROZHITKOVY_MINIMUM = {
    int(k): v
    for k, v in config["PROZHITKOVYI_MINIMUM"].items()
}

INSTANTSIA_KOEF = {
    int(k): v
    for k, v in config["INSTANTSIA_KOEF"].items()
}

ELEKTRONNUI_SUD_KOEF = config["ELEKTRONNUI_SUD_KOEF"]

INSTANTSIA_LABELS = {
    1: "І інстанція",
    2: "ІІ інстанція (апеляція)",
    3: "ІІІ інстанція (касація)"
}

STEP        = "#6A653A"
STEP_DARK   = "#4A4730"
STEP_LIGHT  = "#9A956A"
CREAM       = "#F0EFE7"
CREAM_DARK  = "#E2E1D8"
INK         = "#1A1A1A"
INK_SOFT    = "#4A4A4A"
SUCCESS     = "#4A7C59"

FONT_REGULAR   = "UAF Sans"
FONT_FALLBACK  = "Segoe UI"   # якщо UAF Sans не завантажився

#Завантаження шрифту для customtkinter
def uaf(size: int, weight: str = "normal") -> ctk.CTkFont:
    return ctk.CTkFont(family=FONT_REGULAR, size=size, weight=weight)

#Функція розрахунку
def rozrahunok(rik: int, vymogy: int, inst: int, use_el_sud: bool = True) -> float:
    if rik not in PROZHITKOVY_MINIMUM:
        raise ValueError(f"Прожитковий мінімум для {rik} не задано.")
    if inst not in INSTANTSIA_KOEF:
        raise ValueError("Некоректна інстанція.")

    prozhitk   = PROZHITKOVY_MINIMUM[rik]
    instantzia = INSTANTSIA_KOEF[inst]
    el_sud     = ELEKTRONNUI_SUD_KOEF if use_el_sud else 1.0
    return prozhitk * instantzia * vymogy * el_sud

#Клас для GUI
class CourtFeeCalcApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        self.title("Розрахунок судового збору — в/ч А3913")
        self.geometry("580x680")
        self.resizable(False, False)
        self.configure(fg_color=CREAM)

        self._build_ui()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color=STEP, corner_radius=0, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="РОЗРАХУНОК СУДОВОГО ЗБОРУ",
            font=uaf(16, "bold"),
            text_color=CREAM,
        ).place(relx=0.5, rely=0.42, anchor="center")

        ctk.CTkLabel(
            header,
            text="в/ч А3913 · 12-а ОБАА",
            font=uaf(10),
            text_color=STEP_LIGHT,
        ).place(relx=0.5, rely=0.75, anchor="center")

        body = ctk.CTkFrame(self, fg_color=CREAM, corner_radius=0)
        body.pack(fill="both", expand=True, padx=30, pady=24)

        self._section_label(body, "РІК ПОЗОВНОГО ПРОВАДЖЕННЯ", 0)
        self.rik_var = ctk.StringVar(value="2025")
        ctk.CTkComboBox(
            body,
            variable=self.rik_var,
            values=[str(y) for y in PROZHITKOVY_MINIMUM.keys()],
            state="readonly",
            width=300, height=38,
            font=uaf(13),
            fg_color=CREAM_DARK,
            border_color=STEP, border_width=1,
            button_color=STEP, button_hover_color=STEP_DARK,
            dropdown_fg_color=CREAM, dropdown_hover_color=CREAM_DARK,
            text_color=INK,
        ).grid(row=1, column=0, sticky="w", pady=(2, 16))

        self._section_label(body, "КІЛЬКІСТЬ ЗОБОВ'ЯЗАЛЬНИХ ВИМОГ", 2)
        self.vymog_var = ctk.StringVar(value="1")
        ctk.CTkEntry(
            body,
            textvariable=self.vymog_var,
            width=300, height=38,
            font=uaf(13),
            fg_color=CREAM_DARK,
            border_color=STEP, border_width=1,
            text_color=INK,
        ).grid(row=3, column=0, sticky="w", pady=(2, 16))

        self._section_label(body, "СУДОВА ІНСТАНЦІЯ", 4)
        self.insta_var = ctk.StringVar(value="І інстанція")
        ctk.CTkComboBox(
            body,
            variable=self.insta_var,
            values=list(INSTANTSIA_LABELS.values()),
            state="readonly",
            width=300, height=38,
            font=uaf(13),
            fg_color=CREAM_DARK,
            border_color=STEP, border_width=1,
            button_color=STEP, button_hover_color=STEP_DARK,
            dropdown_fg_color=CREAM, dropdown_hover_color=CREAM_DARK,
            text_color=INK,
        ).grid(row=5, column=0, sticky="w", pady=(2, 16))

        badge = ctk.CTkFrame(body, fg_color=CREAM_DARK, corner_radius=6, height=32)
        badge.grid(row=6, column=0, sticky="w", pady=(0, 20))
        ctk.CTkLabel(
            badge,
            text="  ⚖  Коефіцієнт «Електронний суд»: 0.8  ",
            font=uaf(11),
            text_color=STEP_DARK,
        ).pack(padx=8, pady=4)

        ctk.CTkButton(
            body,
            text="РОЗРАХУВАТИ",
            command=self._calculate,
            width=300, height=44,
            font=uaf(14, "bold"),
            fg_color=STEP, hover_color=STEP_DARK,
            text_color=CREAM,
            corner_radius=4,
        ).grid(row=7, column=0, sticky="w", pady=(0, 20))
        
        self.result_card = ctk.CTkFrame(
            body,
            fg_color=CREAM_DARK,
            corner_radius=8,
            border_width=1,
            border_color=STEP_LIGHT,
        )
        self.result_card.grid(row=8, column=0, sticky="ew", pady=(0, 8))

        self.result_label = ctk.CTkLabel(
            self.result_card,
            text="",
            font=uaf(12),
            text_color=INK_SOFT,
            justify="left",
            wraplength=480,
        )
        self.result_label.pack(padx=20, pady=16, anchor="w")

        ctk.CTkButton(
            body,
            text="Очистити",
            command=self._clear,
            width=120, height=32,
            font=uaf(11),
            fg_color=CREAM_DARK, hover_color=STEP_LIGHT,
            text_color=INK_SOFT,
            border_width=1, border_color=STEP_LIGHT,
            corner_radius=4,
        ).grid(row=9, column=0, sticky="w")

    def _section_label(self, parent, text: str, row: int):
        ctk.CTkLabel(
            parent,
            text=text,
            font=uaf(10, "bold"),
            text_color=STEP,
        ).grid(row=row, column=0, sticky="w", pady=(0, 2))

    def _get_inst_key(self) -> int:
        label = self.insta_var.get()
        for k, v in INSTANTSIA_LABELS.items():
            if v == label:
                return k
        raise ValueError("Некоректна інстанція")

    def _calculate(self):
        try:
            rik    = int(self.rik_var.get())
            vymogy = int(self.vymog_var.get())
            if vymogy < 1:
                messagebox.showerror("Помилка", "Кількість вимог має бути більше 0.")
                return
            inst = self._get_inst_key()

            zbir       = rozrahunok(rik, vymogy, inst, True)
            prozhitk   = PROZHITKOVY_MINIMUM[rik]
            inst_koef  = INSTANTSIA_KOEF[inst]
            inst_label = INSTANTSIA_LABELS[inst]

            lines = (
                f"Рік:                  {rik}\n"
                f"Прожитковий мінімум:  {prozhitk:.2f} грн\n"
                f"Інстанція:            {inst_label}  (×{inst_koef})\n"
                f"Кількість вимог:      {vymogy}\n"
                f"Коеф. електр. суду:   {ELEKTRONNUI_SUD_KOEF}\n"
                f"{'─' * 38}\n"
                f"СУДОВИЙ ЗБІР:         {zbir:.2f} грн"
            )

            self.result_label.configure(
                text=lines,
                text_color=SUCCESS,
                font=uaf(12, "bold"),
            )
        except ValueError as e:
            messagebox.showerror("Помилка введення", str(e))
        except Exception as e:
            messagebox.showerror("Помилка", f"Несподівана помилка: {e}")

    def _clear(self):
        self.result_label.configure(text="", text_color=INK_SOFT, font=uaf(12))
        self.rik_var.set("2025")
        self.vymog_var.set("1")
        self.insta_var.set("І інстанція")


if __name__ == "__main__":
    app = CourtFeeCalcApp()
    app.mainloop()
