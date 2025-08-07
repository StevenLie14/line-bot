def parse_user_command(user_command: str) -> tuple[str, list[str]]:
    parts = user_command.split(" ")
    command = parts[0]
    args = parts[1:]
    return command, args