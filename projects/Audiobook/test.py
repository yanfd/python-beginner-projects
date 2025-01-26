import pyttsx3
from PyPDF2 import PdfReader
import threading
import queue
import keyboard

class AudioBookReader:
    def __init__(self, pdf_file):
        self.pdf = PdfReader(pdf_file)
        self.speaker = pyttsx3.init()
        self.speaker_lock = threading.Lock()
        self.task_queue = queue.Queue()
        self.stop_event = threading.Event()

    def play(self):
        for page_num in range(len(self.pdf.pages)):
            if self.stop_event.is_set():
                break
            text = self.pdf.pages[page_num].extract_text()
            self.task_queue.put(text)
            # Wait until this page's text has been fully spoken
            while not self.task_queue.empty():
                self.stop_event.wait(0.1)

    def speak_worker(self):
        while not self.stop_event.is_set():
            try:
                text = self.task_queue.get(timeout=1)
                with self.speaker_lock:  # Ensure thread-safe speech
                    self.speaker.say(text)
                    self.speaker.runAndWait()
            except queue.Empty:
                continue
        self.speaker.stop()

    def run(self):
        play_thread = threading.Thread(target=self.play)
        speak_thread = threading.Thread(target=self.speak_worker)

        play_thread.start()
        speak_thread.start()

        keyboard.add_hotkey('q', self.stop_playback)
        keyboard.wait('q')

        play_thread.join()
        speak_thread.join()

def main():
    while True:
        try:
            file = input("Enter your PDF file name: ")
            reader = AudioBookReader(file)
            reader.run()
            break
        except FileNotFoundError:
            print("File not found. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()