import logging
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import html2text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("storybook_async_fetcher")


async def markdown_format_text(
    url: str, locator_id: str = "storybook-docs", anchor_class_name: str = "sb-anchor"
) -> str:
    markdown = ""
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(
                headless=True,
                executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            )

            page = await browser.new_page()
            await page.goto(url)
            await page.wait_for_load_state("networkidle")

            iframes = page.frames
            storybook_iframes = [
                iframe for iframe in iframes if iframe.name.startswith("storybook")
            ]

            for iframe in storybook_iframes:
                html = await iframe.locator(f"#{locator_id}").inner_html()
                soup = BeautifulSoup(html, "html.parser")

                for el in soup.select(f".{anchor_class_name}"):
                    el.decompose()

                markdown += html2text.html2text(str(soup))
        except Exception as e:
            logger.error(f'Error "{str(e)}" was occurred during fetching text')
        finally:
            await browser.close()

    return markdown


if __name__ == "__main__":
    from storybook_resources import uri_2_resource

    component = "Notification"
    asyncio.run(
        markdown_format_text(
            url=uri_2_resource[
                f"markdown://softreef/design-system/component/{component}"
            ].url
        )
    )
