import os
from statistics import mean

from dotenv import load_dotenv
import requests

from utils import extract_popular_programming_languages, predict_salary


API_URL = "https://api.superjob.ru/2.33/vacancies/"


def get_response(api_key, keyword):

    headers = {
        "X-Api-App-Id": api_key,
    }

    params = {
        "town": "Москва",
        # "catalogues": 48,
        "keyword": keyword,
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


if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ["SECRET_KEY"]

    statistics = dict()
    languages = extract_popular_programming_languages(3)
    for language in languages:
        response = get_response(api_key, language)
        predicted_salaries = [predict_rub_salary_sj(vacancy) for vacancy in
                              response.get("objects")]
        not_none_salaries = [predicted_salary for predicted_salary in
                             predicted_salaries if
                             predicted_salary is not None]

        statistics[language] = {
            "vacancies_found": response.get("total"),
            "vacancies_processed": len(not_none_salaries),
            "average_salary": int(mean(not_none_salaries)),
        }

    print(statistics)
