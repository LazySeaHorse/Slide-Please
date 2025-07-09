import tkinter as tk
from tkinter import ttk, messagebox
import pvporcupine
import pyaudio
import struct
import threading
import pyautogui
import time
import os

# Configuration - Change these values as needed
PICOVOICE_ACCESS_KEY = "YOUR_API_KEY"
PPN_FILE_PATH = "next_slide_please.ppn"  # Place this file in same directory as script


class VoiceSlideController:
    def __init__(self, root):
        self.root = root
        self.root.title("Slide Please!")
        self.root.geometry("280x300")

        # Default key to simulate
        self.current_key = "right"

        # Threading control
        self.listening = False
        self.listen_thread = None

        # Detection indicator state
        self.detection_active = False

        # Initialize UI
        self.setup_ui()

        # Initialize Porcupine
        self.porcupine = None
        self.audio_stream = None

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(main_frame, text="Slide Please!",
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Status indicator frame
        self.indicator_frame = tk.Frame(main_frame, width=200, height=50,
                                        bg='gray', relief=tk.RAISED, bd=2)
        self.indicator_frame.grid(row=1, column=0, columnspan=2, pady=10)
        self.indicator_frame.grid_propagate(False)

        self.status_label = ttk.Label(self.indicator_frame, text="Not Listening",
                                      font=('Arial', 12), background='gray',
                                      foreground='white')
        self.status_label.place(relx=0.5, rely=0.5, anchor='center')

        # Key selection
        ttk.Label(main_frame, text="Key to Press:").grid(row=2, column=0,
                                                         sticky=tk.W, pady=10)

        # Common presentation keys
        self.key_options = [
            ("Right Arrow", "right"),
            ("Left Arrow", "left"),
            ("Space", "space"),
            ("Page Down", "pagedown"),
            ("Page Up", "pageup"),
            ("Enter", "enter"),
            ("Down Arrow", "down"),
            ("Up Arrow", "up"),
            ("F5", "f5"),
            ("Escape", "escape")
        ]

        self.key_var = tk.StringVar(value="right")
        self.key_dropdown = ttk.Combobox(main_frame, textvariable=self.key_var,
                                         state='readonly', width=15)
        self.key_dropdown['values'] = [opt[0] for opt in self.key_options]
        self.key_dropdown.set("Right Arrow")
        self.key_dropdown.grid(row=2, column=1, sticky=tk.W, pady=10)
        self.key_dropdown.bind('<<ComboboxSelected>>', self.on_key_change)

        # Start/Stop button
        self.toggle_button = ttk.Button(main_frame, text="Start Listening",
                                        command=self.toggle_listening, width=20)
        self.toggle_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Info label
        info_text = 'Say "next slide please" to advance slides'
        info_label = ttk.Label(main_frame, text=info_text, font=('Arial', 10, 'italic'))
        info_label.grid(row=4, column=0, columnspan=2, pady=(10, 0))

    def on_key_change(self, event=None):
        # Update the current key based on selection
        selected_text = self.key_var.get()
        for text, key in self.key_options:
            if text == selected_text:
                self.current_key = key
                break

    def toggle_listening(self):
        if not self.listening:
            self.start_listening()
        else:
            self.stop_listening()

    def start_listening(self):
        try:
            # Check if PPN file exists
            if not os.path.exists(PPN_FILE_PATH):
                messagebox.showerror("Error",
                                     f"Wake word file '{PPN_FILE_PATH}' not found!\n\n"
                                     "Please create it using Picovoice Console.")
                return

            # Initialize Porcupine
            self.porcupine = pvporcupine.create(
                access_key=PICOVOICE_ACCESS_KEY,
                keyword_paths=[PPN_FILE_PATH]
            )

            # Initialize PyAudio
            pa = pyaudio.PyAudio()
            self.audio_stream = pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )

            # Update UI
            self.listening = True
            self.toggle_button.config(text="Stop Listening")
            self.update_status("Listening...", "green")

            # Start listening thread
            self.listen_thread = threading.Thread(target=self.listen_loop, daemon=True)
            self.listen_thread.start()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to start listening:\n{str(e)}")
            self.stop_listening()

    def stop_listening(self):
        self.listening = False

        # Close audio stream
        if self.audio_stream is not None:
            self.audio_stream.close()
            self.audio_stream = None

        # Delete Porcupine instance
        if self.porcupine is not None:
            self.porcupine.delete()
            self.porcupine = None

        # Update UI
        self.toggle_button.config(text="Start Listening")
        self.update_status("Not Listening", "gray")

    def listen_loop(self):
        while self.listening:
            try:
                # Read audio frame
                pcm = self.audio_stream.read(self.porcupine.frame_length,
                                             exception_on_overflow=False)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

                # Process with Porcupine
                keyword_index = self.porcupine.process(pcm)

                if keyword_index >= 0:
                    # Wake word detected!
                    self.on_detection()

            except Exception as e:
                print(f"Error in listen loop: {e}")
                self.root.after(0, self.stop_listening)
                break

    def on_detection(self):
        # Simulate key press
        pyautogui.press(self.current_key)

        # Flash detection indicator
        self.root.after(0, lambda: self.flash_detection())

    def flash_detection(self):
        # Show detection
        self.update_status("DETECTED!", "orange")

        # Reset after 500ms
        self.root.after(500, lambda: self.update_status("Listening...", "green")
        if self.listening else None)

    def update_status(self, text, color):
        self.indicator_frame.config(bg=color)
        self.status_label.config(text=text, background=color)

        # Choose text color based on background
        text_color = 'white' if color in ['green', 'gray', 'red'] else 'black'
        self.status_label.config(foreground=text_color)

    def cleanup(self):
        self.stop_listening()


def main():
    root = tk.Tk()
    app = VoiceSlideController(root)

    # Ensure cleanup on exit
    root.protocol("WM_DELETE_WINDOW", lambda: [app.cleanup(), root.destroy()])

    root.mainloop()


if __name__ == "__main__":
    main()
