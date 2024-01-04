from tech_news.database import find_news
from datetime import datetime


# Requisito 7
def search_by_title(title):
    title = title.lower()
    results = []

    for news in find_news():
        if title in news["title"].lower():
            results.append((news["title"], news["url"]))

    return results


# Requisito 8
def search_by_date(date):
    results = []

    try:
        date = datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')

        for news in find_news():
            if date in news["timestamp"]:
                results.append((news["title"], news["url"]))

        return results

    except ValueError:
        raise ValueError("Data inválida")


# Requisito 9
def search_by_category(category):
    category = category.lower
    results = []

    for news in find_news():
        if category() in news["category"].lower():
            results.append((news["title"], news["url"]))

    return results
