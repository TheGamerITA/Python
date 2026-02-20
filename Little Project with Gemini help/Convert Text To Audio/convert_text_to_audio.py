
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyttsx3
import threading

class TextToAudioApp:
    def __init__(self, root):
        """
        Inizializza l'applicazione principale.
        Configura la finestra, il titolo, le dimensioni e avvia il motore audio.
        """
        self.root = root
        self.root.title("Advanced Text to Audio Converter")
        self.root.geometry("600x550")
        self.root.resizable(False, False)

        # Initialize pyttsx3 engine
        try:
            self.engine = pyttsx3.init()
        except Exception as e:
            messagebox.showerror("Errore Inizializzazione", f"Impossibile inizializzare il motore audio: {e}")
            self.root.destroy()
            return

        self.create_widgets()
        self.load_voices()

    def create_widgets(self):
        """
        Crea e posiziona tutti gli elementi dell'interfaccia grafica:
        - Titolo
        - Area di testo (input)
        - Impostazioni (Voci, Velocità, Volume)
        - Pulsanti di azione (Ascolta, Salva)
        - Barra di stato
        """
        # Title
        title_label = ttk.Label(self.root, text="Convertitore Testo in Audio", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Text Input Area
        input_frame = ttk.LabelFrame(self.root, text="Testo da Convertire")
        input_frame.pack(pady=5, padx=10, fill="both", expand=True)

        self.text_area = tk.Text(input_frame, height=10, font=("Arial", 11), wrap="word")
        self.text_area.pack(pady=5, padx=5, fill="both", expand=True)

        # Settings Frame
        settings_frame = ttk.LabelFrame(self.root, text="Impostazioni Audio")
        settings_frame.pack(pady=5, padx=10, fill="x")

        # Voice Selection
        ttk.Label(settings_frame, text="Voce:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.voice_combo = ttk.Combobox(settings_frame, state="readonly", width=40)
        self.voice_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.voice_combo.bind("<<ComboboxSelected>>", self.change_voice)

        # Speed (Rate)
        ttk.Label(settings_frame, text="Velocità:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
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
        ttk.Label(actions_frame, text="Nome file (senza estensione):").pack(side="left", padx=5)
        self.filename_entry = ttk.Entry(actions_frame, width=20)
        self.filename_entry.insert(0, "output")
        self.filename_entry.pack(side="left", padx=5)

        # Buttons
        self.listen_btn = ttk.Button(actions_frame, text="Ascolta Anteprima", command=self.listen_text)
        self.listen_btn.pack(side="right", padx=5)

        save_btn = ttk.Button(actions_frame, text="Salva (.mp3)", command=self.save_audio)
        save_btn.pack(side="right", padx=5)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x")

    def load_voices(self):
        """
        Recupera le voci installate nel sistema operativo (es. Windows/macOS)
        e le carica nel menu a tendina (Combobox) per farle scegliere all'utente.
        """
        try:
            self.voices = self.engine.getProperty('voices')
            voice_names = [f"{v.name}" for v in self.voices]
            self.voice_map = {f"{v.name}": v.id for v in self.voices}
            self.voice_combo['values'] = voice_names
            if voice_names:
                self.voice_combo.current(0)
        except Exception as e:
             messagebox.showwarning("Attenzione", f"Impossibile caricare le voci: {e}")

    def update_rate_label(self, value):
        """
        Aggiorna il numero visualizzato accanto allo slider della velocità
        quando l'utente lo sposta.
        """
        val = int(float(value))
        self.rate_label.config(text=str(val))

    def update_volume_label(self, value):
        """
        Aggiorna la percentuale visualizzata accanto allo slider del volume
        quando l'utente lo sposta.
        """
        val = int(float(value) * 100)
        self.volume_label.config(text=f"{val}%")

    def change_voice(self, event=None):
        """
        Funzione chiamata quando l'utente seleziona una nuova voce dal menu a tendina.
        Imposta immediatamente la voce selezionata nel motore audio.
        """
        selected_name = self.voice_combo.get()
        if selected_name in self.voice_map:
            self.engine.setProperty('voice', self.voice_map[selected_name])

    def get_engine_properties(self):
        """
        Legge i valori attuali dagli slider (Velocità, Volume) e dal menu (Voce)
        e li applica al motore pyttsx3.
        Serve a garantire che l'audio usi le impostazioni più recenti prima di parlare o salvare.
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
        Azione del pulsante 'Ascolta Anteprima'.
        Prende il testo e avvia la lettura in un thread separato
        per evitare che l'interfaccia si blocchi (non risponda) durante l'audio.
        """
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showinfo("Info", "Inserisci del testo prima di ascoltare.")
            return

        self.status_var.set("Riproduzione in corso...")
        self.listen_btn.config(state="disabled")
        
        # Run in a separate thread to keep UI responsive
        threading.Thread(target=self._run_speak_thread, args=(text,), daemon=True).start()

    def _run_speak_thread(self, text):
        """
        Questa funzione viene eseguita in background (thread).
        Si occupa effettivamente di far parlare il motore.
        """
        try:
            self.get_engine_properties()
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            # Schedule the error message on the main thread
            self.root.after(0, lambda: messagebox.showerror("Errore Audio", f"Errore durante la riproduzione: {e}"))
        finally:
            self.root.after(0, lambda: self.status_var.set("Pronto"))
            self.root.after(0, lambda: self.listen_btn.config(state="normal"))

    def save_audio(self):
        """
        Azione del pulsante 'Salva (.mp3)'.
        Prende il testo, imposta le proprietà e salva l'output in un file audio
        invece di riprodurlo dalle casse.
        """
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showinfo("Info", "Inserisci del testo da salvare.")
            return

        filename = self.filename_entry.get().strip()
        if not filename:
            messagebox.showinfo("Info", "Inserisci un nome per il file.")
            return
        
        if not filename.endswith(".mp3"):
            filename += ".mp3"

        # Optional: Let user choose directory via dialog if they want, 
        # but for now we follow the "dynamic filename" requirement simply.
        # Could enhance by opening a file dialog.
        
        self.status_var.set(f"Salvataggio di {filename}...")
        
        try:
            self.get_engine_properties()
            self.engine.save_to_file(text, filename)
            self.engine.runAndWait()
            messagebox.showinfo("Successo", f"File salvato correttamente:\n{filename}")
            self.status_var.set("Salvataggio completato")
        except Exception as e:
            messagebox.showerror("Errore Salvataggio", f"Non è stato possibile salvare il file: {e}")
            self.status_var.set("Errore durante il salvataggio")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToAudioApp(root)
    root.mainloop()