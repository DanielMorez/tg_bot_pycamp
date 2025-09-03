def get_readable_expires(expires_at: int, current_time: int) -> str:
    remaining_time = expires_at - current_time
    minutes = remaining_time // 60
    seconds = remaining_time % 60

    readable_time = f"{seconds} сек"
    if minutes > 0:
        readable_time = f"{minutes} мин {readable_time}"

    return readable_time
