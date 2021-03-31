from statistics import mean
import time

from bs4 import BeautifulSoup
import requests

API_URL = "https://api.hh.ru/vacancies"


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


def fetch_hh_page(job_title, page_number):
    """Get parsed one HH page via API.

    :param job_title: title of the job to search
    :param page_number: number of page to parse
    :return: parsed page
    """

    params = {
        "text": f"NAME:{job_title}",
        "area": "1",
        "period": "30",
        "page": str(page_number),
        "per_page": "100",
    }

    response = requests.get(API_URL, params=params)
    response.raise_for_status()

    return response.json()


def predict_rub_salary(salary_fork):
    """Predict salary in rubles given a salary fork.

    :param salary_fork: salary fork
    :return: predicted salary
    """

    if not salary_fork.get("currency") != "RUB":
        return None

    salary_from = salary_fork.get("from")
    salary_to = salary_fork.get("to")

    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_from:
        return salary_from * 1.2
    if salary_to:
        return salary_to * 0.8

    return None


def calculate_predicted_salaries(response_items):
    """Calculate predicted salaries from parsed items.

    :param response_items: parsed items from API response
    :return: list of calculated predicted salaries
    """

    salaries_forks = [vacancy.get("salary") for vacancy in response_items]
    salaries = [predict_rub_salary(salary_fork)
                for salary_fork in salaries_forks if salary_fork]

    return salaries


def calculate_salaries_for_pages(job_title, number_of_pages=30):
    """Calculate predicted salaries for all given pages.

    :param job_title: job title
    :param number_of_pages: number of pages to parse
    :return: list of calculated salaries and total number of jobs found
    """

    salaries = list()
    results_found = 0
    for page_number in range(number_of_pages):
        try:
            parsed_response = fetch_hh_page(job_title, page_number)
        except requests.HTTPError:
            print("Unable to reach the server")
            break
        except requests.exceptions.ConnectionError:
            print("Failed to establish a new connection.")
            break

        if not results_found:
            results_found = parsed_response.get("found")

        response_items = parsed_response.get("items")
        if not response_items:
            break
        salaries += calculate_predicted_salaries(response_items)
        time.sleep(3)

    return salaries, results_found


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


if __name__ == "__main__":
    languages = extract_popular_programming_languages(2)
    output = dict()
    for language in languages:
        salaries, jobs_found = \
            calculate_salaries_for_pages(f"Программист {language}", 3)
        output[language] = format_statistics(jobs_found, salaries)

    print(output)
