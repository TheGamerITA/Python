import os
import threading
import customtkinter as ctk
import tkinter.messagebox as msgbox
from tkinter import filedialog

from services.export_service import generate_report
from services.history_service import load_history


class UltimateApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Research Station Premium")
        self.geometry("800x650")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.tabview = ctk.CTkTabview(self, width=780, height=600)
        self.tabview.pack(pady=10)
        self.tabview.add("Search")
        self.tabview.add("History")
        self.tabview.add("Settings")

        self.setup_search_tab()
        self.setup_history_tab()
        self.setup_settings_tab()

    def setup_search_tab(self):
        tab = self.tabview.tab("Search")

        ctk.CTkLabel(tab, text="Research Station", font=("Arial", 28, "bold"), text_color="#4B8BBE").pack(pady=15)

        self.entry = ctk.CTkEntry(tab, placeholder_text="Topic...", width=500, height=45, font=("Arial", 14))
        self.entry.pack(pady=10)

        frame = ctk.CTkFrame(tab, fg_color="transparent")
        frame.pack(pady=5)

        ctk.CTkLabel(frame, text="Language:").grid(row=0, column=0, padx=5)
        self.opt_lang = ctk.CTkOptionMenu(frame, values=["Italiano", "English", "Français", "Deutsch"])
        self.opt_lang.grid(row=0, column=1, padx=10)

        ctk.CTkLabel(frame, text="Depth:").grid(row=0, column=2, padx=5)
        self.seg_depth = ctk.CTkSegmentedButton(frame, values=["Fast", "Normal", "In-depth"])
        self.seg_depth.set("Normal")
        self.seg_depth.grid(row=0, column=3, padx=10)

        ctk.CTkLabel(frame, text="Format:").grid(row=1, column=0, padx=5, pady=10)
        self.opt_format = ctk.CTkOptionMenu(frame, values=["PDF", "Word (.docx)"])
        self.opt_format.grid(row=1, column=1, padx=10, pady=10)

        self.btn_go = ctk.CTkButton(tab, text="START SEARCH", width=250, height=50, font=("Arial", 16, "bold"), command=self.ask_save)
        self.btn_go.pack(pady=20)

        self.progress = ctk.CTkProgressBar(tab, width=500, mode="indeterminate")
        self.progress.pack_forget()
        self.status = ctk.CTkLabel(tab, text="Ready.", text_color="gray")
        self.status.pack(pady=5)

        self.btn_open = ctk.CTkButton(tab, text="OPEN FILE", fg_color="#E09F3E", state="disabled", command=self.open_current)
        self.btn_open.pack_forget()
        self.saved_path = None

    def setup_history_tab(self):
        tab = self.tabview.tab("History")
        self.history_frame = ctk.CTkScrollableFrame(tab, width=700, height=450)
        self.history_frame.pack(pady=10)
        self.refresh_history()

        ctk.CTkButton(tab, text="Refresh List", command=self.refresh_history).pack(pady=5)

    def refresh_history(self):
        for w in self.history_frame.winfo_children():
            w.destroy()
        history = load_history()
        if not history:
            ctk.CTkLabel(self.history_frame, text="No recent searches.").pack(pady=20)
            return

        for item in history:
            frame = ctk.CTkFrame(self.history_frame)
            frame.pack(fill="x", pady=2, padx=5)
            ctk.CTkLabel(frame, text=f"[{item['date']}] {item['topic']}", anchor="w", width=300).pack(side="left", padx=10)
            ctk.CTkButton(frame, text="Open", width=80, command=lambda p=item["path"]: self.safe_open(p)).pack(side="right", padx=10)

    def safe_open(self, path):
        if os.path.exists(path):
            os.startfile(path)
        else:
            msgbox.showerror("Error", "The file no longer exists.")

    def setup_settings_tab(self):
        tab = self.tabview.tab("Settings")
        ctk.CTkLabel(tab, text="App Theme", font=("Arial", 18)).pack(pady=20)
        self.seg_theme = ctk.CTkSegmentedButton(tab, values=["Blue", "Green", "Dark-Blue"], command=self.change_theme)
        self.seg_theme.set("Blue")
        self.seg_theme.pack(pady=10)
        ctk.CTkLabel(tab, text="(Requires restart to fully apply to all elements)", text_color="gray").pack()

    def change_theme(self, value):
        ctk.set_default_color_theme(value.lower())
        msgbox.showinfo("Theme", f"You selected {value}. Restart the app to see all changes.")

    def ask_save(self):
        topic = self.entry.get().strip()
        fmt = self.opt_format.get()
        ext = ".pdf" if "PDF" in fmt else ".docx"

        path = filedialog.asksaveasfilename(defaultextension=ext, title="Save Report", initialfile=f"{topic}{ext}")
        if not topic:
            msgbox.showwarning("Missing topic", "Please enter a topic before starting the search.")
            return

        if path:
            self.toggle_ui(False)
            self.progress.pack()
            self.progress.start()
            threading.Thread(
                target=self.worker,
                args=(topic, self.opt_lang.get(), self.seg_depth.get(), path, fmt),
                daemon=True,
            ).start()

    def worker(self, topic, lang, depth, path, fmt):
        try:
            generate_report(topic, lang, depth, path, fmt)
            self.saved_path = path
            self.on_success()
        except Exception as exc:
            print(exc)
            self.on_fail(str(exc))

    def on_success(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.status.configure(text="Completed!", text_color="green")
        self.btn_open.pack(pady=10)
        self.btn_open.configure(state="normal")
        self.toggle_ui(True)
        self.refresh_history()

    def on_fail(self, err):
        self.progress.stop()
        self.progress.pack_forget()
        self.status.configure(text=f"Error: {err}", text_color="red")
        self.toggle_ui(True)

    def toggle_ui(self, enable):
        state = "normal" if enable else "disabled"
        self.btn_go.configure(state=state)

    def open_current(self):
        if self.saved_path:
            os.startfile(self.saved_path)
