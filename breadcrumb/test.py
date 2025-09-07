import re
from playwright.sync_api import sync_playwright

def normalize_text(text):
    return re.sub(r'\s+', ' ', text.strip())

def get_breadcrumb_data(page, url):
    """Returns list of (text, href) breadcrumb tuples from a page."""
    page.goto(url, timeout=20000, wait_until="domcontentloaded")
    selectors = [""]
    breadcrumb = []

    for selector in selectors:
        try:
            element = page.wait_for_selector(selector, timeout=5000)
            if element:
                items = element.query_selector_all("a, span")
                for item in items:
                    text = normalize_text(item.inner_text())
                    href = item.get_attribute("href") or ""
                    if text:
                        breadcrumb.append((text, href))
                break
        except:
            continue

    return breadcrumb

def is_valid_url(page, url):
    """Checks whether a breadcrumb link leads to a valid page."""
    try:
        if not url.startswith("http"):
            return True  # ignore relative links or missing hrefs
        page.goto(url, timeout=10000, wait_until="domcontentloaded")
        content = page.content().lower()
        return not ("404" in content or "page not found" in content or "error" in content)
    except:
        return False

def compare_breadcrumbs(live_url, aem_url):
    """Compare breadcrumbs between live_url and aem_url and return results as text."""
    output = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 🚀 switched to headless for server use
        context = browser.new_context()
        page_live = context.new_page()
        page_aem = context.new_page()
        check_page = context.new_page()

        live_breadcrumb = get_breadcrumb_data(page_live, live_url)
        aem_breadcrumb = get_breadcrumb_data(page_aem, aem_url)

        live_dict = dict(live_breadcrumb)
        aem_dict = dict(aem_breadcrumb)

        live_texts = set(live_dict.keys())
        aem_texts = set(aem_dict.keys())

        if live_texts == aem_texts:
            output.append("Breadcrumbs match exactly.")
        else:
            extra_live = live_texts - aem_texts
            extra_aem = aem_texts - live_texts

            output.append("Breadcrumbs do not match. Checking extra links...")

            invalids = []
            for text in extra_live:
                url = live_dict.get(text)
                if url and not is_valid_url(check_page, url):
                    invalids.append((text, url))

            for text in extra_aem:
                url = aem_dict.get(text)
                if url and not is_valid_url(check_page, url):
                    invalids.append((text, url))

            if invalids:
                output.append("Mismatch: Found invalid breadcrumb links:")
                for text, link in invalids:
                    output.append(f" - '{text}' → {link}")
            else:
                output.append("Breadcrumbs differ, but all extra links are valid. Not a mismatch.")

        browser.close()

    return "\n".join(output)
