import logging

class RemoteControl:
    def __init__(self):
        logging.info("RemoteControl initialized. Awaiting commands from keyboard input.")

    def get_command(self):
        """
        This is a simple blocking call to get a command from the keyboard.
        In a real system, this might listen on a socket or other interface.
        """
        try:
            cmd = input("Enter command (forward/backward/left/right/stop/exit): ").strip().lower()
            return cmd
        except Exception as e:
            logging.error("Error reading remote command: %s", e)
            return None
