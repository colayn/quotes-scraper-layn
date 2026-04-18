import json
from playwright.sync_api import sync_playwright
from aws.s3_upload import upload_to_s3

BASE_URL = "http://quotes.toscrape.com/search.aspx"
OUTPUT_FILE = "quotes_output.json"
BUCKET_NAME = "quotes-scraper-s3"


# -------------------
# GET AUTHORS
# -------------------
def authors_get(page):
    page.goto(BASE_URL)
    options = page.query_selector_all("select#author option")

    return [
        opt.get_attribute("value")
        for opt in options
        if opt.get_attribute("value")
    ]


# -------------------
# GET TAGS
# -------------------
def tags_get(page, author):
    page.goto(BASE_URL)
    page.wait_for_selector("select#author")

    page.select_option("select#author", author)

    page.wait_for_function(
        "document.querySelector('select#tag') && document.querySelector('select#tag').options.length > 1"
    )

    options = page.query_selector_all("select#tag option")

    return [
        opt.get_attribute("value")
        for opt in options
        if opt.get_attribute("value")
    ]


# -------------------
# PARSE QUOTE
# -------------------
def parse_quote(div, fallback_author):
    text = ""
    author_name = fallback_author

    for sel in ["span.text", ".text", "span"]:
        el = div.query_selector(sel)
        if el:
            text = el.inner_text().strip()
            if text:
                break

    for sel in [".author", "small.author"]:
        el = div.query_selector(sel)
        if el:
            author_name = el.inner_text().strip()

    tags = [
        t.inner_text().strip()
        for t in div.query_selector_all(".tag")
    ]

    return {
        "quote": text,
        "author": author_name,
        "tags": tags
    }


# -------------------
# SCRAPER
# -------------------
def scrape_all():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        results = []
        seen = set()

        authors = authors_get(page)
        print(f"Found {len(authors)} authors")

        for author in authors:
            print(f"Processing: {author}")

            tags = tags_get(page, author)

            for tag in tags:
                try:
                    page.goto(BASE_URL)
                    page.wait_for_selector("select#author")

                    page.select_option("select#author", author)

                    page.wait_for_function(
                        "document.querySelector('select#tag') && document.querySelector('select#tag').options.length > 1"
                    )

                    page.select_option("select#tag", tag)
                    page.click("input.btn[type='submit']")
                    page.wait_for_timeout(1500)

                    for div in page.query_selector_all("div.quote"):
                        q = parse_quote(div, author)

                        key = (q["quote"], q["author"])

                        if q["quote"] and key not in seen:
                            seen.add(key)
                            results.append(q)

                except Exception as e:
                    print(f"Error {author}/{tag}: {e}")

        browser.close()
        return results


# -------------------
# SAVE JSON
# -------------------
def save_json(data):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(data)} quotes locally")


# -------------------
# MAIN
# -------------------
def main():
    data = scrape_all()

    print("\n====================")
    print(f"TOTAL QUOTES: {len(data)}")
    print("====================\n")

    save_json(data)

    upload_to_s3(
        OUTPUT_FILE,
        BUCKET_NAME,
        OUTPUT_FILE
    )


if __name__ == "__main__":
    main()