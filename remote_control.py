"""
remote_control.py
Module for handling remote/manual override commands (e.g. from RC, controller, or network).
"""

class RemoteControl:
    def __init__(self):
        """
        Initialize any necessary communication or parser for remote commands.
        """
        self.override_active = False
        self.last_command = None  # could store something like ('FORWARD', 0.5) for speed

    def update_command(self):
        """
        Check for new commands from the remote system.
        This might read from an RC receiver, a socket, etc.
        """
        # Example pseudo-code to read from some input
        # data = read_remote_data()
        # parse it into commands
        pass

    def get_command(self):
        """
        Return the latest command (direction/speed or stop).
        """
        return self.last_command

    def is_override_active(self):
        """
        Return True if remote override is engaged.
        """
        return self.override_active
