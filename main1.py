import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from bs4 import BeautifulSoup
import pandas as pd

st.title("Live Job Scraper with LangChain")

companies = {
    "Google": "https://careers.google.com/jobs/results/",
    "Microsoft": "https://jobs.careers.microsoft.com/global/en",
    "Amazon": "https://www.amazon.jobs/en/",
    "Deloitte": "https://apply.deloitte.com/",
    "SAP": "https://jobs.sap.com/"
}

def scrape_jobs(url, company):
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        content = docs[0].page_content

        soup = BeautifulSoup(content, "html.parser")
        jobs = []

        if company == "Google":
            for job in soup.find_all("a", class_="gc-card"):
                title = job.find("div", class_="gc-card__title")
                if title:
                    jobs.append({
                        "Company": company,
                        "Title": title.text.strip(),
                        "Link": "https://careers.google.com" + job["href"]
                    })

        elif company == "Microsoft":
            for job in soup.find_all("a", class_="job-title"):
                jobs.append({
                    "Company": company,
                    "Title": job.text.strip(),
                    "Link": "https://jobs.careers.microsoft.com" + job["href"]
                })

        else:
            # Placeholder for heavy JS sites
            jobs.append({"Company": company, "Title": "Dynamic page (use Playwright/Selenium)", "Link": url})

        return jobs

    except Exception as e:
        return [{"Company": company, "Title": f"Error: {str(e)}", "Link": url}]

if st.button("Show Jobs"):
    all_jobs = []
    for company, url in companies.items():
        st.write(f"🔍 Scraping {company}...")
        all_jobs.extend(scrape_jobs(url, company))

    if all_jobs:
        df = pd.DataFrame(all_jobs)
        st.dataframe(df)
    else:
        st.warning("No jobs found.")
