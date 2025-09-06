class Helper:
    @staticmethod
    def parse_user_command(user_command: str) -> str:
        parts = user_command.split(" ")
        command = parts[0]
        return command.lower()

    @staticmethod
    def parse_user_args(user_command: str, splitter: str = " ") -> str:
        parts = user_command.split(splitter)
        args = parts[1:]
        return args