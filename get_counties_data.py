import requests
from requests import RequestException
from requests.exceptions import RequestException, ConnectionError, HTTPError, Timeout
from tabulate import tabulate


class FindCountry:
    __URL = "https://restcountries.com/v3.1/all"


    @classmethod
    def get_response_from_url(cls):
        try:
            response = requests.get(cls.__URL)
            if response.status_code == 200:
                return response.json()
            response.raise_for_status()
        except (RequestException, ConnectionError, HTTPError, Timeout) as e:
            raise RequestException(f"Bad request: {e}")


    @classmethod
    def get_countries_data(cls):
        data = cls.get_response_from_url()
        all_countries = []
        for country in data:
            name = country.get("name").get("common")
            capital = country.get("capital", ["None"])[0]
            flag_url = country.get("flags").get("png")
            all_countries.append([name, capital, flag_url])
        return all_countries


    @classmethod
    def display_data(cls):
        countries = cls.get_countries_data()
        headers = ['Country Name', 'Capital', 'Flag URL']
        print(tabulate(countries, headers=headers, tablefmt='grid'))



if __name__ == "__main__":
    FindCountry.display_data()
