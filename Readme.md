[![Build Status](https://travis-ci.org/tonymontaro/cross-solar-python.svg?branch=master)](https://travis-ci.org/tonymontaro/cross-solar-python)
[![codecov](https://codecov.io/gh/tonymontaro/cross-solar-python/branch/master/graph/badge.svg)](https://codecov.io/gh/tonymontaro/cross-solar-python)
[![Maintainability](https://api.codeclimate.com/v1/badges/21e39b1913cdd7e939a6/maintainability)](https://codeclimate.com/github/tonymontaro/cross-solar-python/maintainability)

# Cross-Solar
Cross-Solar is a backend web application by a startup company called “Green Energy Analytics” in Texas - USA. This application collects energy analytics data for solar panels every hour. 

Api documentation: [Generated with Postman](https://documenter.getpostman.com/view/646133/RzZ7o1Ba)

## Technologies Used
- [Python3.6](https://www.python.org/downloads/) - A programming language that lets you work more quickly.
- [Django](https://www.djangoproject.com/) - A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
- [Virtualenv](https://virtualenv.pypa.io/en/stable/) - A tool to create isolated virtual environments.


## Getting Started
Requirements
- Mac OS X, Windows or Linux
- Python 3.6
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)

### Installation
- Clone the repository and cd into the root folder:
```bash
git clone https://github.com/tonymontaro/cross-solar-python.git && cd cross-solar-python
```


- Create and activate a virtual environment in python3:

```bash
virtualenv -p python3 venv && source venv/bin/activate
```


- Install the dependencies:
```bash
pip install -r requirements.txt
```

- Migrations:
```bash
python manage.py migrate
```

- Finally, run the application
```bash
python manage.py runserver
```

## Tests

- Run the tests with:
``` bash
coverage run manage.py test && coverage report
```

## Tasks Performed

- refactored API URLs to be included in the cross_solar project
- added tests for HourAnalytics
- implemented the DayAnalytics views and added relevant tests
- fixed longitude/latitude bugs and updated tests
- made the "brand" optional on the Panel model since just the serial number, longitude and latitude are required.
- put a check to ensure that the serial number is unique
- refactored code to follow pep8 standards
- added continuous integration with TravisCI and included the test-build badge on the Readme.md file
- added coverage and maintainability badges to the Readme.md file
- generated API documentation with Postman; https://documenter.getpostman.com/view/646133/RzZ7o1Ba

Repository: https://github.com/tonymontaro/cross-solar-python
