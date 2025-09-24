import aiohttp
from bs4 import BeautifulSoup
from typing import Optional

async def fetch_og_image(url: str, session: Optional[aiohttp.ClientSession] = None) -> Optional[str]:
    """
    Fetch the main image URL from a web page using the og:image meta tag.
    Returns the image URL if found, else None.
    """
    close_session = False
    if session is None:
        session = aiohttp.ClientSession()
        close_session = True
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            if response.status != 200:
                return None
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                return og_image['content']
    except Exception:
        return None
    finally:
        if close_session:
            await session.close()
    return None
