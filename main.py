import time
import json
import logging
import requests
from telegram import Bot
from bs4 import BeautifulSoup
from openai import OpenAI
from fuzzywuzzy import fuzz

# Загрузка конфигурации
with open("config.json", "r") as f:
    config = json.load(f)

bot = Bot(token=config["telegram_token"])
openai = OpenAI()

def fetch_seek_vacancies():
    # Псевдо-функция. Реальную реализацию вставим позже.
    return [{
        "title": "Project Administrator",
        "company": "UNHCR Australia",
        "location": "Melbourne",
        "link": "https://seek.com.au/job/sample",
        "description": "Supporting government funded humanitarian projects with planning and coordination."
    }]

def match_score(resume_text, job_description):
    response = openai.embeddings.create(input=[resume_text, job_description], model="text-embedding-ada-002")
    vec1, vec2 = response.data[0].embedding, response.data[1].embedding
    cosine = sum(x*y for x, y in zip(vec1, vec2)) / (
        sum(x**2 for x in vec1)**0.5 * sum(y**2 for y in vec2)**0.5
    )
    return cosine

def send_telegram_message(text):
    bot.send_message(chat_id="@jobalerbot", text=text, parse_mode="HTML")

def main():
    resume_text = "Experienced Program and Project Administrator with UN, NGO and government background."
    while True:
        for job in fetch_seek_vacancies():
            score = match_score(resume_text, job["description"])
            if score >= config["min_relevance_score"]:
                msg = f"📢 <b>{job['title']}</b> at <i>{job['company']}</i>\n📍 {job['location']}\n🔗 <a href='{job['link']}'>Apply Here</a>\n🤖 Match: {round(score * 100)}%"
                send_telegram_message(msg)
        time.sleep(config["frequency"])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
