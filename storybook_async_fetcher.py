import asyncio
from playwright.async_api import async_playwright
import html2text

async def main(url: str, locator_id: str="storybook-docs") -> str:
    markdown = ""
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        )

        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_load_state("networkidle")

        iframes = page.frames
        storybook_iframes = [iframe for iframe in iframes if iframe.name.startswith('storybook')]

        for iframe in storybook_iframes:
            storybook_docs_div = await iframe.locator(f"#{locator_id}").inner_html()
            markdown += html2text.html2text(storybook_docs_div)

        await browser.close()

    print(markdown)
    return markdown

if __name__ == "__main__":
    from softreef.storybook_resources import uri_2_resource
    asyncio.run(main(url=uri_2_resource["markdown://softreef/design-system/overview"].url))