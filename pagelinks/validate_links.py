# pagelinks/validate_links.py
from playwright.sync_api import sync_playwright

def check_links_for_page_suffix(url):
    """Check links in AEM page for invalid or missing `.page` based on conditions."""
    results = {
        "checked_url": url,
        "total_links": 0,
        "issues": [],
        "status": "ok"
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # headless=True for API usage
        context = browser.new_context(
            user_agent=(
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            )
        )
        page = context.new_page()

        try:
            page.goto(url, timeout=30000, wait_until="networkidle")
            page.wait_for_selector("a[href]", timeout=10000)

            links = page.eval_on_selector_all("a[href]", "els => els.map(e => e.href)")
            results["total_links"] = len(links)

            for link in links:
                if "supplychain" in link.lower():
                    if ".page" not in link:
                        results["issues"].append(
                            {"type": "missing_page", "link": link}
                        )
                else:
                    if ".page" in link:
                        results["issues"].append(
                            {"type": "invalid_page", "link": link}
                        )

            if not results["issues"]:
                results["status"] = "all_good"

        except Exception as e:
            results["status"] = "error"
            results["error_message"] = str(e)

        finally:
            browser.close()

    return results
