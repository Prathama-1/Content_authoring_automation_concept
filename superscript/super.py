from playwright.sync_api import sync_playwright
import re

def check_space_before_superscript(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        page = context.new_page()

        page.route("**/*", lambda route, request:
            route.abort() if request.resource_type in ["image", "font", "stylesheet"] else route.continue_()
        )

        try:
            print(f"\n🔍 Checking superscript spacing on: {url}")
            page.goto(url, timeout=20000, wait_until="domcontentloaded")

            # Get all elements with <sup> inside
            elements_with_sup = page.query_selector_all(":has(sup)")
            issues_found = False

            for element in elements_with_sup:
                html = element.inner_html()
                
                # Check for space before <sup>
                if re.search(r'\s<sup>', html):
                    print(f"❌ Space before superscript found in:\n  {html.strip()}\n")
                    issues_found = True

            if not issues_found:
                print("✅ No spacing issues found before <sup> tags.")

        except Exception as e:
            print(f"❌ Error during superscript check: {e}")
        finally:
            browser.close()

# 🔗 Example AEM URL
aem_url = ""

# 🟢 Run check
check_space_before_superscript(aem_url)
