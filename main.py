import requests
from bs4 import BeautifulSoup
import json

data = []
moscow_vacancies_count = 0

for i in range(1,2):
    print(f'Parsing {i} page')
    url = f'https://career.habr.com/vacancies?page={i}&type=all&with_salary=true' ''
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    cards = soup.find_all("div",class_='vacancy-card__inner')

    for card in cards:
        card_url = card.a['href']
        url = f'https://career.habr.com{card_url}' 
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text,'lxml')
        company = soup.find("div", 'company_name')
        print(company.text)   
        job_title = soup.find("h1", 'page-title__title')
        print(job_title.text)      
        skills = soup.find("span", 'inline-list')
        print(skills.text) 
        city = soup.find(lambda tag: tag.name == 'a' and 'vacancies?city_id=' in tag.get('href', '')).text.strip()
        print(city) 
        
        if city == 'Москва':
            moscow_vacancies_count += 1
            vacancy_data = {
                'company': company.text.strip(),
                'city': city.strip(),
                'job_title': job_title.text.strip(),
                'skills': skills.text.strip() 
            }

            data.append(vacancy_data)

with open('./vacancies_2.json', 'w', encoding='utf-8') as fp:
    json.dump(data, fp, indent=2, ensure_ascii=False)

print(f'Total Moscow vacancies: {moscow_vacancies_count}')