import asyncio
from playwright.async_api import async_playwright

async def playWright_function():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        #navigation.
        await page.goto("https://www.google.com")

        await page.wait_for_timeout(10000)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(playWright_function())