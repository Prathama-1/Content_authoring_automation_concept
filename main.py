
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import sys

from breadcrumb.test import compare_breadcrumbs
from pagelinks.validate_links import check_links_for_page_suffix

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

# Mount frontend directory for static files
app.mount("/frontend", StaticFiles(directory=BASE_DIR / "frontend"), name="frontend")

# @app.get("/", response_class=HTMLResponse)
# def read_root():
#     html_path = BASE_DIR / "frontend" / "index.html"
#     return html_path.read_text(encoding="utf-8")
@app.get("/", response_class=HTMLResponse)
def read_root():
    html_path = BASE_DIR / "frontend" / "index.html"
    if html_path.exists():
        return html_path.read_text(encoding="utf-8")
    return HTMLResponse("<h1>Frontend not found</h1>", status_code=404)

@app.get("/run-breadcrumb")
def run_breadcrumb():
    live_url = ""
    aem_url = ""
    try:
        output = compare_breadcrumbs(live_url, aem_url)  # ✅ returns string
        return {
            "stdout": output,
            "stderr": "",
            "returncode": 0
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "returncode": 1
        }
    

@app.get("/validate_links")
def validate_links():
    url = "https://pt--ups-dev-pt--aemsites.aem.live/ua/en/support/shipping-support/shipping-dimensions-weight"
    result = check_links_for_page_suffix(url)  # ✅ call function directly
    return result