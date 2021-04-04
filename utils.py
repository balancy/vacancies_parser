from statistics import mean

from bs4 import BeautifulSoup
import requests
from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    """Predict salary given a fork from and to.

    :param salary_from: lower border of salary
    :param salary_to: upper border of salary
    :return: predicted salary
    """

    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_from:
        return salary_from * 1.2
    if salary_to:
        return salary_to * 0.8

    return None


def extract_popular_programming_languages(number=8):
    """Extract a list of popular programming languages.

    :param number: number of languages
    :return: list of languages
    """

    url = "https://www.codingame.com/work/blog/hr-news-trends/" \
          "top-10-in-demand-programming-languages/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "lxml")
    selector = "ol li strong"

    extracted_languages = soup.select(selector)
    number = number if 1 <= number < len(extracted_languages) \
        else len(extracted_languages)

    return [language.text for language in extracted_languages][:number]


def generate_pretty_statistics(statistics, site):
    """Generates statistics in pretty format.

    :param statistics: statistics dictionary
    :param site: site statistics comes from
    :return: generated pretty statistics
    """

    table_data = [["Язык программирования", "Вакансий найдено",
                   "Вакансий обработано", "Средняя зарплата"]]
    for language, vacancies_stats in statistics.items():
        table_data.append([
            language, vacancies_stats.get("vacancies_found"),
            vacancies_stats.get("vacancies_processed"),
            vacancies_stats.get("average_salary"),
        ])

    title = f"{site} Moscow"
    table = AsciiTable(table_data, title=title)

    return table.table


def format_statistics(jobs_found, salaries):
    """Represent some statistics in formatted form.

    :param jobs_found: number of found jobs
    :param salaries: list of salaries
    :return: statistics in formatted form
    """

    return {
        "vacancies_found": jobs_found,
        "vacancies_processed": len(salaries),
        "average_salary": int(mean(salaries)),
    }