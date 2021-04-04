import os

from dotenv import load_dotenv
import requests

from utils import (
    extract_popular_programming_languages,
    format_statistics,
    generate_pretty_statistics,
    predict_salary,
)

API_URL = "https://api.superjob.ru/2.33/vacancies/"


def get_response(api_key, keyword, page_number):
    """Get HTTP response from SuperJob API, using keyword.

    :param api_key: your API key
    :param keyword: job to search. Example: Python
    :param page_number: number of page
    :return: HTTP response
    """

    headers = {
        "X-Api-App-Id": api_key,
    }

    params = {
        "town": "Москва",
        "keyword": keyword,
        "page": page_number,
        "count": 100,
    }

    response = requests.get(API_URL, headers=headers, params=params)
    response.raise_for_status()

    return response.json()


def predict_rub_salary_sj(vacancy_description):
    """Predict salary in rubles given a vacancy description.

    :param vacancy_description: vacancy description
    :return: predicted salary
    """

    if vacancy_description.get("currency") != "rub":
        return None

    salary_from = vacancy_description.get("payment_from")
    salary_to = vacancy_description.get("payment_to")

    return predict_salary(salary_from, salary_to)


def calculate_predicted_salaries(parsed_response):
    """Calculate predicted salaries for all salaries found in parsed response.

    :param parsed_response: parsed HTTP response
    :return: predicted salaries
    """

    predicted_salaries = [predict_rub_salary_sj(vacancy) for vacancy
                          in parsed_response.get("objects")]

    return list(filter(None, predicted_salaries))


if __name__ == "__main__":
    load_dotenv()
    superjob_api_key = os.environ["SUPERJOB_API_TOKEN"]

    statistics = dict()
    languages = extract_popular_programming_languages()
    for language in languages[1:]:
        predicted_salaries = list()
        look_another_page = True
        page_number = 0

        while look_another_page:
            try:
                response = get_response(superjob_api_key, language, page_number)
            except requests.HTTPError:
                print("SuperJob API is unavailable. Try later.")
                break

            look_another_page = response.get("more")
            predicted_salaries += calculate_predicted_salaries(response)
            total = response.get("total")
            page_number += 1

        statistics[language] = format_statistics(total, predicted_salaries)

    table = generate_pretty_statistics(statistics, "SuperJob")
    print(table)
