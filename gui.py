import tkinter as tk
from tkinter import scrolledtext
import threading
import datetime
import psutil
from core.brain import process_command

# ── Paleta ARES ──────────────────────────────────────────────
BG_DEEP    = "#080808"
BG_PANEL   = "#0d0d0d"
BG_INPUT   = "#0a0505"
RED_MAIN   = "#8B0000"
RED_BRIGHT = "#cc2200"
RED_HOT    = "#ff4411"
ORANGE_ACC = "#ff6600"
RED_DIM    = "#441100"
RED_MID    = "#661100"
BORDER     = "#2a0a0a"
BORDER_HI  = "#5a1500"
TEXT_DIM   = "#331100"
TEXT_MID   = "#884400"
TEXT_USER  = "#ff5533"
TEXT_ALHIA = "#cc4422"
WHITE_DIM  = "#553322"

FONT_MONO  = ("Courier New", 14)
FONT_MONO_S= ("Courier New", 12)
FONT_MONO_B= ("Courier New", 14, "bold")
FONT_TITLE = ("Courier New", 15, "bold")
FONT_SMALL = ("Courier New", 12)


class AlhiaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ALHIA · ARES PROTOCOL")
        self.root.configure(bg=BG_DEEP)
        self.root.geometry("780x620")
        self.root.minsize(600, 480)
        self.root.resizable(True, True)

        self._build_titlebar()
        self._build_statusbar()
        self._build_chat()
        self._build_inputbar()
        self._build_bottombar()

        self._update_status_loop()
        self._print_system("ALHIA v1.0 inicializada  ·  ARES PROTOCOL ENNABLED")
        self._print_system(f"Sesión iniciada: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # ── TITLEBAR ────────────────────────────────────────────────
    def _build_titlebar(self):
        bar = tk.Frame(self.root, bg="#111111", height=40)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        left = tk.Frame(bar, bg="#111111")
        left.pack(side="left", padx=12)

        tk.Label(left, text="▣", bg="#111111", fg=RED_MAIN,
                 font=("Courier New", 16)).pack(side="left", padx=(0, 8))

        info = tk.Frame(left, bg="#111111")
        info.pack(side="left")
        tk.Label(info, text="ALHIA", bg="#111111", fg=RED_BRIGHT,
                 font=FONT_TITLE).pack(anchor="w")
        tk.Label(info, text="ARES PROTOCOL · ACTIVE", bg="#111111", fg=RED_DIM,
                 font=FONT_SMALL).pack(anchor="w")

        right = tk.Frame(bar, bg="#111111")
        right.pack(side="right", padx=12)

        for color, cmd in [
            ("#8B0000", self.root.destroy),
            ("#3a1a00", self.root.iconify),
            ("#1a0a0a", lambda: None),
        ]:
            btn = tk.Canvas(right, width=12, height=12, bg="#111111",
                            highlightthickness=0, cursor="hand2")
            btn.create_oval(1, 1, 11, 11, fill=color, outline="")
            btn.pack(side="left", padx=3)
            btn.bind("<Button-1>", lambda e, c=cmd: c())

    # ── STATUSBAR ───────────────────────────────────────────────
    def _build_statusbar(self):
        self.status_bar = tk.Frame(self.root, bg="#0d0d0d", height=22)
        self.status_bar.pack(fill="x")
        self.status_bar.pack_propagate(False)

        tk.Frame(self.status_bar, width=4, bg=RED_MAIN).pack(side="left")

        self.lbl_online = self._stat_label("● ONLINE", RED_BRIGHT)
        self.lbl_cpu    = self._stat_label("CPU  0%", RED_MID)
        self.lbl_ram    = self._stat_label("RAM  0.0 GB", RED_MID)
        self.lbl_ares   = self._stat_label("ARES  GUARDANDO", RED_MID)
        self.lbl_hora   = self._stat_label("00:00:00", RED_DIM)

    def _stat_label(self, text, color):
        lbl = tk.Label(self.status_bar, text=text, bg="#0d0d0d", fg=color,
                       font=FONT_SMALL, padx=10)
        lbl.pack(side="left")
        return lbl

    def _update_status_loop(self):
        try:
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory().used / (1024 ** 3)
            now = datetime.datetime.now().strftime("%H:%M:%S")
            self.lbl_cpu.config(text=f"CPU  {cpu:.0f}%")
            self.lbl_ram.config(text=f"RAM  {ram:.1f} GB")
            self.lbl_hora.config(text=now)
        except Exception:
            pass
        self.root.after(2000, self._update_status_loop)

    # ── CHAT AREA ───────────────────────────────────────────────
    def _build_chat(self):
        container = tk.Frame(self.root, bg=BG_DEEP)
        container.pack(fill="both", expand=True, padx=6, pady=(4, 0))

        self.chat = scrolledtext.ScrolledText(
            container,
            bg=BG_DEEP,
            fg=TEXT_ALHIA,
            font=FONT_MONO,
            wrap=tk.WORD,
            state="disabled",
            relief="flat",
            bd=0,
            padx=12,
            pady=10,
            insertbackground=RED_BRIGHT,
            selectbackground=RED_MAIN,
        )
        self.chat.pack(fill="both", expand=True)

        # Scrollbar roja
        self.chat.vbar.config(bg=BG_PANEL,troughcolor=BG_DEEP,activebackground=RED_MAIN,)

        # Tags de color
        self.chat.tag_config("system",    foreground="#553322", font=FONT_MONO_S)
        self.chat.tag_config("label_you", foreground=RED_DIM,   font=FONT_SMALL)
        self.chat.tag_config("label_ai",  foreground=RED_DIM,   font=FONT_SMALL)
        self.chat.tag_config("user_msg",  foreground=TEXT_USER, font=FONT_MONO)
        self.chat.tag_config("ai_msg",    foreground=TEXT_ALHIA,font=FONT_MONO)
        self.chat.tag_config("accent",    foreground=ORANGE_ACC,font=FONT_MONO_B)
        self.chat.tag_config("error",     foreground="#ff2200", font=FONT_MONO)
        self.chat.tag_config("separator", foreground=RED_DIM,   font=FONT_SMALL)

    def _print_system(self, msg):
        self._append(f"  —  {msg}  —\n", "system")

    def _append(self, text, tag):
        self.chat.config(state="normal")
        self.chat.insert("end", text, tag)
        self.chat.config(state="disabled")
        self.chat.see("end")

    def _print_user(self, msg):
        self._append("\n  TU\n", "label_you")
        self._append(f"  {msg}\n", "user_msg")

    def _print_alhia(self, msg):
        self._append("\n  ALHIA\n", "label_ai")
        # Resaltar palabras clave con acento naranja
        parts = msg.split("→")
        if len(parts) > 1:
            for i, part in enumerate(parts):
                tag = "accent" if i % 2 == 1 else "ai_msg"
                self._append(f"  {part.strip()}", tag)
                if i < len(parts) - 1:
                    self._append(" → ", "accent")
            self._append("\n", "ai_msg")
        else:
            self._append(f"  {msg}\n", "ai_msg")

    def _print_thinking(self):
        self._append("\n  ALHIA\n", "label_ai")
        self._append("  procesando...\n", "separator")

    def _remove_last_thinking(self):
        self.chat.config(state="normal")
        content = self.chat.get("1.0", "end")
        idx = content.rfind("  procesando...")
        if idx != -1:
            line_start = content.rfind("\n", 0, idx) + 1
            # Calcular posición tkinter
            start_pos = f"1.0 + {line_start}c"
            end_pos   = f"1.0 + {idx + len('  procesando...\n')}c"
            self.chat.delete(start_pos, end_pos)
        self.chat.config(state="disabled")

    # ── INPUT BAR ───────────────────────────────────────────────
    def _build_inputbar(self):
        bar = tk.Frame(self.root, bg=BG_PANEL, pady=8)
        bar.pack(fill="x", padx=6)

        tk.Frame(bar, width=1, bg=RED_MAIN).pack(side="left", fill="y", padx=(6, 0))

        tk.Label(bar, text=">_", bg=BG_PANEL, fg=RED_MAIN,
                 font=("Courier New", 14, "bold")).pack(side="left", padx=(8, 6))

        self.entry = tk.Entry(
            bar,
            bg=BG_INPUT,
            fg=RED_HOT,
            insertbackground=RED_BRIGHT,
            relief="flat",
            font=FONT_MONO,
            bd=0,
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))
        self.entry.bind("<Return>", self._on_send)
        self.entry.focus_set()

        self.btn_send = tk.Button(
            bar,
            text="ENVIAR",
            bg=RED_MAIN,
            fg="#ffaa88",
            activebackground="#aa0000",
            activeforeground="#ffffff",
            relief="flat",
            font=("Courier New", 10, "bold"),
            cursor="hand2",
            padx=14,
            pady=6,
            command=self._on_send,
        )
        self.btn_send.pack(side="right", padx=(0, 6))

    # ── BOTTOM BAR ──────────────────────────────────────────────
    def _build_bottombar(self):
        bar = tk.Frame(self.root, bg="#0a0505", height=18)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        items = [
            ("GROQ", "llama-3.3-70b"),
            ("ARES", "MONITOR ACTIVO"),
            ("MEM",  "NO INICIADA"),
        ]
        for label, val in items:
            tk.Label(bar, text=f"{label} · {val}", bg="#0a0505", fg=RED_DIM,
                     font=FONT_SMALL, padx=14).pack(side="left")

    # ── LÓGICA DE ENVÍO ─────────────────────────────────────────
    def _on_send(self, event=None):
        texto = self.entry.get().strip()
        if not texto:
            return

        if texto.lower() in ("salir", "exit", "quit"):
            self.root.destroy()
            return

        self.entry.delete(0, "end")
        self._print_user(texto)
        self._print_thinking()
        self.btn_send.config(state="disabled", bg=RED_DIM)

        threading.Thread(target=self._process, args=(texto,), daemon=True).start()

    def _process(self, texto):
        try:
            respuesta = process_command(texto)
        except Exception as e:
            respuesta = f"Error: {e}"

        self.root.after(0, self._show_response, respuesta)

    def _show_response(self, respuesta):
        self._remove_last_thinking()
        if respuesta.startswith("Error"):
            self._print_alhia_error(respuesta)
        else:
            self._print_alhia(respuesta)
        self.btn_send.config(state="normal", bg=RED_MAIN)
        self.entry.focus_set()

    def _print_alhia_error(self, msg):
        self._append("\n  ALHIA\n", "label_ai")
        self._append(f"  {msg}\n", "error")


def main():
    root = tk.Tk()
    app = AlhiaGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()