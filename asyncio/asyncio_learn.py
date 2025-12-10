import aiohttp
import asyncio


async def url_one(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            return html[:500]
async def main():
    url = "https://httpbin.org/html"
    result = await url_one(url)
    print(result)

asyncio.run(main())