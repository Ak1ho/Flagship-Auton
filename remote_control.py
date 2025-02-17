import threading
import sys
import time

class RemoteControl:
    def __init__(self):
        self.remote_override = False
        self.kill_switch = False
        self.last_command = None
        self._stop_thread = False
        self.input_thread = None

    def start(self):
        """
        Start the input thread that listens for manual override commands.
        """
        self._stop_thread = False
        self.input_thread = threading.Thread(target=self._listen_for_input, daemon=True)
        self.input_thread.start()

    def stop(self):
        """
        Signal the input thread to stop.
        """
        self._stop_thread = True
        if self.input_thread:
            self.input_thread.join()

    def _listen_for_input(self):
        print("Remote Control Thread Started. Type 'r' to toggle remote mode, 'k' for kill, 'q' to quit.")
        while not self._stop_thread:
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                user_input = sys.stdin.readline().strip().lower()
                if user_input == 'r':
                    self.remote_override = not self.remote_override
                    print(f"Remote override set to: {self.remote_override}")
                elif user_input == 'k':
                    self.kill_switch = True
                    print("KILL SWITCH ENGAGED!")
                elif user_input in ['w', 'a', 's', 'd']:
                    self.last_command = user_input
                elif user_input == 'q':
                    self.kill_switch = True
                    print("Quitting remote control...")
                    break
            time.sleep(0.05)

        self._stop_thread = True

try:
    import select
except ImportError:
    pass
