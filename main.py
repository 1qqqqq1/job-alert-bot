
import time
import json
import logging
import requests
from telegram import Bot
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

# Загрузка конфигурации
with open("config.json", "r") as f:
    config = json.load(f)

bot = Bot(token=config["telegram_token"])

def fetch_seek_vacancies():
    # Псевдо-функция. Реальную реализацию можно заменить позже
    return [{
        "title": "Project Administrator",
        "company": "UNHCR Australia",
        "location": "Melbourne",
        "link": "https://seek.com.au/job/sample",
        "description": "Supporting government funded humanitarian projects with planning and coordination in cooperation with UN bodies."
    }]

def match_score(resume_text, job_description):
    keywords = [
        "project", "program", "administrator", "coordinator", "NGO",
        "migration", "UN", "refugee", "asylum", "planning", "humanitarian", "support"
    ]
    hits = sum(1 for kw in keywords if kw.lower() in job_description.lower())
    return hits / len(keywords)

def send_telegram_message(text):
    bot.send_message(chat_id=5624396746, text=text, parse_mode="HTML")

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
