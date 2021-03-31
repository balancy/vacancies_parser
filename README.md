# Vacancies parser

Application allows parsing statistics of developer vacancies from job searching sites. 
App contains two scripts, one parses from HH, another from SuperJob.
Firstly, scripts extract the most popular programming languages at the moment.
Then performs gathering statistics concerning how many offers found and what is the average 
salary for every programming language on these sites.
Then statistics is displayed in table form, easy to understand. 

## How to install
Python3 and Git should be already installed. 

1. Clone the repository by command:
```console
git clone https://github.com/balancy/vacancies_parser
```
2. Inside cloned repository create virtual environment by command:
```console
python -m venv env
```
3. Activate virtual environment. For linux-based OS:
```console
source env/bin/activate
```
&nbsp;&nbsp;&nbsp;&nbsp;For Windows:
```console
env\scripts\activate
```
4. Install dependencies:
```
pip install -r requirements.txt
```
5. Rename file `.env.example` to `.env` and initialize your propre SuperJob API key:
```console
SECRET_KEY = "v3.r.111111111.1111111111111111111111111111.111111111111111111111111111111"
```
6. Run HH and SuperJob parsing scripts by commands:
```console
python hh_parse.py
```
```console
python superjob_parse.py
```
## Project Goals
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
