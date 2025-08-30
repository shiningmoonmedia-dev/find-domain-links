import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import streamlit as st
import pandas as pd

# ---------- Page Config ----------
st.set_page_config(
    page_title="Domain Link Finder",
    page_icon="🔗",
    layout="centered"
)

# ---------- Header ----------
st.title("🔍 Domain Link Finder")
st.markdown("Easily find all links to a specific domain within a website.")
st.divider()

# ---------- Input Section ----------
st.subheader("Enter Details")

col1, col2 = st.columns(2)
with col1:
    base_url = st.text_input("🌐 Website to Crawl", "https://focusedusolutions.com")
with col2:
    target_domain = st.text_input("🎯 Domain to Search", "focuseduvation.com")

start_button = st.button("🚀 Start Crawling")

# ---------- Crawler Logic ----------
if start_button:
    visited = set()
    to_visit = [base_url]
    results = []

    def is_same_domain(url):
        return urlparse(url).netloc.endswith(urlparse(base_url).netloc)

    progress = st.progress(0)
    count = 0

    with st.spinner("Crawling website... please wait ⏳"):
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
                st.write(f"⚠️ Error crawling {url}: {e}")

    df = pd.DataFrame(results, columns=["Page URL", "Link Found"])

    st.success(f"✅ Crawl Completed! Found **{len(results)}** links to `{target_domain}`")
    st.dataframe(df, use_container_width=True)

    if not df.empty:
        st.download_button(
            label="⬇️ Download Results (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="focuseduvation_links.csv",
            mime="text/csv"
        )

# ---------- Footer ----------
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Developed by <b>Indra Thapa</b> 🚀</p>",
    unsafe_allow_html=True
)
