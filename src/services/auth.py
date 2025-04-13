from config import settings
from src.services.api_client import APIClient


async def user_login(telegram_user_id: str, phone: str, telegram_username: str = None) -> None:
    client = APIClient(settings.API_BASE_URL)
    response = await client.post_data(
        'api/v1/accounts/login',
        {'telegram_username': telegram_username, 'telegram_user_id': telegram_user_id, 'phone': phone},
    )
    return response
