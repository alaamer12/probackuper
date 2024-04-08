import threading

class Invoker:
    __lock = threading.Lock()
    __instance = None

    def __new__(cls, *args, **kwargs):
        with cls.__lock:
            if cls.__instance is None:
                cls.__instance = super().__new__(cls, *args, **kwargs)
            return cls.__instance

    def __init__(self):
        self._commands = []

    def add_command(self, command):
        self._commands.append(command)

    def execute_commands(self):
        for command in self._commands:
            command.execute()