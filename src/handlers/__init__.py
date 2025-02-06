from .start import router as start_router

# Собираем все роутеры в один список
routers = [start_router]


def register_handlers(dp):
    for router in routers:
        dp.include_router(router)
