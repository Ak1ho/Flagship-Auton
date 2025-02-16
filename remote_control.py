class RemoteControl:
    def __init__(self):
        self.override_active=False
        self.last_command=None
    def update_command(self):
        pass
    def get_command(self):
        return self.last_command
    def is_override_active(self):
        return self.override_active
