
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import streamlit as st
import pandas as pd

st.title("Website Link Checker")

base_url = st.text_input("Enter Base URL to Crawl:", "https://focusedusolutions.com")
target_domain = st.text_input("Enter Domain to Search Links For:", "focuseduvation.com")

if st.button("Start Crawling"):
    visited = set()
    to_visit = [base_url]
    results = []

    def is_same_domain(url):
        return urlparse(url).netloc.endswith(urlparse(base_url).netloc)

    progress = st.progress(0)
    count = 0

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                continue

            visited.add(url)
            soup = BeautifulSoup(response.text, "html.parser")

            for a in soup.find_all("a", href=True):
                link = urljoin(url, a["href"])
                if target_domain in link:
                    results.append([url, link])

                if is_same_domain(link) and link not in visited:
                    to_visit.append(link)

            count += 1
            progress.progress(min(count / 100, 1.0))  

        except Exception as e:
            st.write(f"Error crawling {url}: {e}")

    df = pd.DataFrame(results, columns=["Page URL", "Link Found"])
    st.success(f"✅ Done! Found {len(results)} links to {target_domain}")
    st.dataframe(df)

    if not df.empty:
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="focuseduvation_links.csv",
            mime="text/csv"
        )
