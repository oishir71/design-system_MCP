import logging
import asyncio
from playwright.async_api import async_playwright
import html2text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("storybook_async_fetcher")


async def markdown_format_text(url: str, locator_id: str = "storybook-docs") -> str:
    markdown = ""
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(
                headless=False,
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
                storybook_docs_div = await iframe.locator(f"#{locator_id}").inner_html()
                markdown += html2text.html2text(storybook_docs_div)
        except Exception as e:
            logger.error(f'Error "{str(e)}" was occurred during fetching text')
        finally:
            await browser.close()

    return markdown


if __name__ == "__main__":
    from storybook_resources import uri_2_resource

    asyncio.run(
        markdown_format_text(
            url=uri_2_resource[
                "markdown://softreef/design-system/component/Slider"
            ].url,
            save_image=True,
        )
    )
