from datetime import datetime
import pytz


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
    
    @staticmethod 
    def get_current_time() -> str:
        jakarta_tz = pytz.timezone("Asia/Jakarta")
        now = datetime.now(jakarta_tz)

        return now.strftime("%Y-%m-%d %H:%M")