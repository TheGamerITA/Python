import requests
import wikipedia
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

from config import DEPTH_SETTINGS, LANG_MAP


def download_image(topic):
    try:
        page = wikipedia.page(topic)
        if page.images:
            for img_url in page.images[:5]:
                if img_url.lower().endswith((".jpg", ".png", ".jpeg")):
                    response = requests.get(img_url, stream=True, timeout=5)
                    if response.status_code == 200:
                        filename = f"temp_{topic.replace(' ', '')}.jpg"
                        with open(filename, "wb") as f:
                            f.write(response.content)
                        return filename
    except (wikipedia.exceptions.WikipediaException, requests.RequestException):
        pass
    return None


def smart_scrape(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=4)
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs[:3]])
        if len(text) > 400:
            text = text[:400] + "..."
        return text.strip() or "No textual content found."
    except requests.RequestException:
        return "Site access failed."


def collect_research(topic, lang, depth):
    code = LANG_MAP.get(lang, "it")
    depth_cfg = DEPTH_SETTINGS.get(depth, DEPTH_SETTINGS["Normal"])

    try:
        wikipedia.set_lang(code)
        wiki_summary = wikipedia.summary(topic, sentences=depth_cfg["sentences"])
        img_file = download_image(topic)
    except wikipedia.exceptions.WikipediaException:
        wiki_summary = "N/A"
        img_file = None

    web_results = []
    full_text = wiki_summary

    try:
        with DDGS() as ddgs:
            raw = list(ddgs.text(topic, max_results=depth_cfg["web_count"]))
            for result in raw:
                body = smart_scrape(result["href"]) if depth != "Fast" else result["body"]
                web_results.append(
                    {"title": result["title"], "body": body, "href": result["href"]}
                )
                full_text += " " + body
    except Exception:
        pass

    return wiki_summary, web_results, full_text, img_file
