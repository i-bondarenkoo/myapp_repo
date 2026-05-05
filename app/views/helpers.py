import aiohttp


async def get_http_session():
    async with aiohttp.ClientSession() as session:
        yield session
