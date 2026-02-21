
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyttsx3
import threading

class TextToAudioApp:
    def __init__(self, root):
        """
        Initialize the main application.
        Sets up the window, title, dimensions, and starts the audio engine.
        """
        self.root = root
        self.root.title("Advanced Text to Audio Converter")
        self.root.geometry("600x550")
        self.root.resizable(False, False)

        # Initialize pyttsx3 engine
        try:
            self.engine = pyttsx3.init()
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Unable to initialize audio engine: {e}")
            self.root.destroy()
            return

        self.create_widgets()
        self.load_voices()

    def create_widgets(self):
        """
        Create and place all GUI elements:
        - Title
        - Text input area
        - Settings (Voices, Rate, Volume)
        - Action buttons (Listen, Save)
        - Status bar
        """
        # Title
        title_label = ttk.Label(self.root, text="Text to Audio Converter", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Text Input Area
        input_frame = ttk.LabelFrame(self.root, text="Text to Convert")
        input_frame.pack(pady=5, padx=10, fill="both", expand=True)

        self.text_area = tk.Text(input_frame, height=10, font=("Arial", 11), wrap="word")
        self.text_area.pack(pady=5, padx=5, fill="both", expand=True)

        # Settings Frame
        settings_frame = ttk.LabelFrame(self.root, text="Audio Settings")
        settings_frame.pack(pady=5, padx=10, fill="x")

        # Voice Selection
        ttk.Label(settings_frame, text="Voice:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.voice_combo = ttk.Combobox(settings_frame, state="readonly", width=40)
        self.voice_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.voice_combo.bind("<<ComboboxSelected>>", self.change_voice)

        # Speed (Rate)
        ttk.Label(settings_frame, text="Rate:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.rate_scale = ttk.Scale(settings_frame, from_=50, to=300, orient="horizontal", command=self.update_rate_label)
        self.rate_scale.set(150)  # Default value
        self.rate_scale.grid(row=1, column=1, padx=5, pady=5, sticky="we")
        
        self.rate_label = ttk.Label(settings_frame, text="150")
        self.rate_label.grid(row=1, column=2, padx=5, pady=5)

        # Volume
        ttk.Label(settings_frame, text="Volume:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.volume_scale = ttk.Scale(settings_frame, from_=0, to=1, orient="horizontal", command=self.update_volume_label)
        self.volume_scale.set(1.0) # Default value
        self.volume_scale.grid(row=2, column=1, padx=5, pady=5, sticky="we")

        self.volume_label = ttk.Label(settings_frame, text="100%")
        self.volume_label.grid(row=2, column=2, padx=5, pady=5)

        settings_frame.columnconfigure(1, weight=1)

        # Actions Frame
        actions_frame = ttk.Frame(self.root)
        actions_frame.pack(pady=10, padx=10, fill="x")

        # Filename Entry
        ttk.Label(actions_frame, text="Filename (no extension):").pack(side="left", padx=5)
        self.filename_entry = ttk.Entry(actions_frame, width=20)
        self.filename_entry.insert(0, "output")
        self.filename_entry.pack(side="left", padx=5)

        # Buttons
        self.listen_btn = ttk.Button(actions_frame, text="Listen Preview", command=self.listen_text)
        self.listen_btn.pack(side="right", padx=5)

        save_btn = ttk.Button(actions_frame, text="Save (.mp3)", command=self.save_audio)
        save_btn.pack(side="right", padx=5)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x")

    def load_voices(self):
        """
        Retrieves voices installed on the operating system (e.g., Windows/macOS)
        and loads them into the dropdown (Combobox) for the user to choose.
        """
        try:
            self.voices = self.engine.getProperty('voices')
            voice_names = [f"{v.name}" for v in self.voices]
            self.voice_map = {f"{v.name}": v.id for v in self.voices}
            self.voice_combo['values'] = voice_names
            if voice_names:
                self.voice_combo.current(0)
        except Exception as e:
             messagebox.showwarning("Warning", f"Unable to load voices: {e}")

    def update_rate_label(self, value):
        """
        Update the number shown next to the rate slider
        when the user moves it.
        """
        val = int(float(value))
        self.rate_label.config(text=str(val))

    def update_volume_label(self, value):
        """
        Update the percentage shown next to the volume slider
        when the user moves it.
        """
        val = int(float(value) * 100)
        self.volume_label.config(text=f"{val}%")

    def change_voice(self, event=None):
        """
        Called when the user selects a new voice from the dropdown.
        Immediately applies the selected voice to the engine.
        """
        selected_name = self.voice_combo.get()
        if selected_name in self.voice_map:
            self.engine.setProperty('voice', self.voice_map[selected_name])

    def get_engine_properties(self):
        """
        Reads current values from sliders (Rate, Volume) and the menu (Voice)
        and applies them to the pyttsx3 engine.
        Ensures audio uses the latest settings before speaking or saving.
        """
        # Update Rate
        rate = int(self.rate_scale.get())
        self.engine.setProperty('rate', rate)
        
        # Update Volume
        volume = float(self.volume_scale.get())
        self.engine.setProperty('volume', volume)

        # Update Voice - ensure it's set
        selected_name = self.voice_combo.get()
        if selected_name in self.voice_map:
            self.engine.setProperty('voice', self.voice_map[selected_name])

    def listen_text(self):
        """
        Action for the 'Listen Preview' button.
        Takes the text and starts reading it in a separate thread
        to prevent the UI from freezing during audio playback.
        """
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showinfo("Info", "Enter some text before listening.")
            return

        self.status_var.set("Playback in progress...")
        self.listen_btn.config(state="disabled")
        
        # Run in a separate thread to keep UI responsive
        threading.Thread(target=self._run_speak_thread, args=(text,), daemon=True).start()

    def _run_speak_thread(self, text):
        """
        This function runs in the background (thread).
        It actually commands the engine to speak.
        """
        try:
            self.get_engine_properties()
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            # Schedule the error message on the main thread
            self.root.after(0, lambda: messagebox.showerror("Audio Error", f"Error during playback: {e}"))
        finally:
            self.root.after(0, lambda: self.status_var.set("Ready"))
            self.root.after(0, lambda: self.listen_btn.config(state="normal"))

    def save_audio(self):
        """
        Action for the 'Save (.mp3)' button.
        Takes the text, sets the properties, and saves the output to an audio file
        instead of playing it through speakers.
        """
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showinfo("Info", "Enter text to save.")
            return

        filename = self.filename_entry.get().strip()
        if not filename:
            messagebox.showinfo("Info", "Enter a filename.")
            return
        
        if not filename.endswith(".mp3"):
            filename += ".mp3"

        # Optional: Let user choose directory via dialog if they want, 
        # but for now we follow the "dynamic filename" requirement simply.
        # Could enhance by opening a file dialog.
        
        self.status_var.set(f"Saving {filename}...")
        
        try:
            self.get_engine_properties()
            self.engine.save_to_file(text, filename)
            self.engine.runAndWait()
            messagebox.showinfo("Success", f"File saved successfully:\n{filename}")
            self.status_var.set("Save completed")
        except Exception as e:
            messagebox.showerror("Save Error", f"Unable to save file: {e}")
            self.status_var.set("Error during save")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToAudioApp(root)
    root.mainloop()