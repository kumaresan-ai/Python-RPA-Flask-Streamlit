import argparse
import re
import sys
import time
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout


def clean_text(text: str) -> str:
    # Normalize whitespace/newlines
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def first_existing_selector(page, selectors):
    """Return the first selector that exists on the page, else None."""
    for sel in selectors:
        try:
            if page.locator(sel).count() > 0:
                return sel
        except Exception:
            pass
    return None


def extract_page_text(page) -> str:
    """
    Try several common content containers for docs/blog/tutorials.
    Falls back to <body> if none match.
    """
    candidates = [
        "div[role='main']",
        "main",
        "article",
        "#content",
        "div#content",
        ".content",
    ]
    sel = first_existing_selector(page, candidates) or "body"
    try:
        text = page.locator(sel).inner_text()
    except Exception:
        text = page.inner_text("body")
    return clean_text(text)


def collect_tutorial_links(page, base_url: str, limit: int) -> list:
    """
    From the start page, collect likely tutorial links.
    - For docs.python.org, ToC links live under .toctree-wrapper
    - For other sites, we still try internal links under main/article
    """
    # Prefer Sphinx ToC links (docs.python.org)
    hrefs = page.eval_on_selector_all(
        "div[role='main'] .toctree-wrapper a[href$='.html'], "
        "main .toctree-wrapper a[href], "
        "article .toctree-wrapper a[href]",
        "els => els.map(a => a.getAttribute('href'))"
    )

    # If none found, grab internal links from main/article as a fallback
    if not hrefs:
        hrefs = page.eval_on_selector_all(
            "div[role='main'] a[href], main a[href], article a[href]",
            "els => els.map(a => a.getAttribute('href'))"
        )

    urls = []
    base = base_url
    for href in hrefs or []:
        if not href or href.startswith("#") or href.startswith("mailto:"):
            continue
        abs_url = urljoin(base, href)
        # Keep only same-domain links to avoid crawling the whole web
        if urlparse(abs_url).netloc == urlparse(base_url).netloc:
            urls.append(abs_url)

    # De-duplicate preserving order
    seen = set()
    unique = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique.append(u)

    # Heuristic: prefer pages that look like part of the tutorial
    # For docs.python.org this catches "/tutorial/"
    preferred = [u for u in unique if "/tutorial/" in u] or unique

    # Don’t include the base_url itself here (the caller adds it first)
    preferred = [u for u in preferred if u.rstrip("/") != base_url.rstrip("/")]

    return preferred[:max(0, limit)]


def scrape(start_url: str, out_path: str, max_pages: int, timeout_ms: int, delay_s: float):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (compatible; TutorialScraper/1.0; +https://example.com) "
                "Playwright-Educational"
            )
        )
        page = context.new_page()

        pages_to_fetch = []

        # Load start page
        try:
            page.goto(start_url, timeout=timeout_ms, wait_until="domcontentloaded")
        except PWTimeout:
            print(f"ERROR: Timed out opening {start_url}", file=sys.stderr)
            browser.close()
            sys.exit(1)

        # Build the crawl list
        pages_to_fetch.append(start_url)
        if max_pages > 1:
            more = collect_tutorial_links(page, start_url, max_pages - 1)
            pages_to_fetch.extend(more)

        all_chunks = []

        for i, url in enumerate(pages_to_fetch, start=1):
            try:
                page.goto(url, timeout=timeout_ms, wait_until="domcontentloaded")
                title = page.title() or "Untitled"
                body_text = extract_page_text(page)
                chunk = f"{'#' * 1} {title}\nURL: {url}\n\n{body_text}\n"
                all_chunks.append(chunk)
                if i < len(pages_to_fetch):
                    time.sleep(delay_s)  # be polite
            except PWTimeout:
                print(f"WARNING: Timed out on {url}", file=sys.stderr)
            except Exception as e:
                print(f"WARNING: Failed on {url} ({e})", file=sys.stderr)

        if not all_chunks:
            print("No content extracted.", file=sys.stderr)
            browser.close()
            sys.exit(2)

        # Separate pages clearly in the text file
        separator = "\n\n" + ("-" * 80) + "\n\n"
        output = separator.join(all_chunks)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(output)

        browser.close()
        print(f"Saved {len(all_chunks)} page(s) to {out_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Read a Python tutorial site with Playwright and save to a text file."
    )
    parser.add_argument(
        "--start-url",
        default="https://docs.python.org/3/tutorial/index.html",
        help="Start page (default: Python official tutorial index).",
    )
    parser.add_argument(
        "--out",
        default="python_tutorial.txt",
        help="Output text file path (default: python_tutorial.txt).",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=3,
        help="How many pages total to fetch including the start page (default: 3).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60000,
        help="Per-page timeout in milliseconds (default: 60000).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay (seconds) between page fetches to be polite (default: 1.0).",
    )

    args = parser.parse_args()
    scrape(
        start_url=args.start_url,
        out_path=args.out,
        max_pages=max(1, args.max_pages),
        timeout_ms=args.timeout,
        delay_s=max(0.0, args.delay),
    )


if __name__ == "__main__":
    main()
