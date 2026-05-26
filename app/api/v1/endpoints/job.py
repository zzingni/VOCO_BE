from fastapi import APIRouter
import requests
from bs4 import BeautifulSoup

router = APIRouter()


@router.get("/jobs")
def get_jobs(keyword: str = ""):

    url = f"https://www.saramin.co.kr/zf_user/search?searchword={keyword}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    job_list = []

    jobs = soup.select(".item_recruit")

    for job in jobs[:10]:

        # 제목
        title_tag = job.select_one(".job_tit a")
        title = title_tag.text.strip() if title_tag else ""

        # 링크
        link = (
            "https://www.saramin.co.kr"
            + title_tag["href"]
            if title_tag and title_tag.get("href")
            else ""
        )

        # 회사명
        company_tag = job.select_one(".corp_name a")
        company = company_tag.text.strip() if company_tag else ""

        # 지역 / 경력
        condition_tags = job.select(".job_condition span")

        location = condition_tags[0].text.strip() if len(condition_tags) > 0 else ""
        career = condition_tags[1].text.strip() if len(condition_tags) > 1 else ""

        # 스택 태그
        stack_tags = job.select(".job_meta span")

        stacks = []

        for tag in stack_tags:
            text = tag.text.strip()

            if text:
                stacks.append(text)

        job_list.append({
            "title": title,
            "company": company,
            "location": location,
            "career": career,
            "stacks": stacks,
            "link": link
        })

    return {
        "jobs": job_list
    }