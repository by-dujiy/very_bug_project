"""
Modify previous flask application to REST API using Flask API package and add
swagger using flasgger. The application has to have a version and format(json,
xml) parameters

E.g.

http://localhost:5000/api/v1/report/?format=json

Write tests using Unittest module or py.test.
Resources:

    Flask REST API: https://flask-restful.readthedocs.io/en/latest/

    JSON module https://docs.python.org/3/library/json.html

    XML module https://docs.python.org/3/library/xml.html

    Web API Design (recommended) https://pages.apigee.com/rs/apigee/images/api-
    design-ebook-2012-03.pdf

    Web API Design (short translation onto Russian) https://habr.com/ru/post/
    181988/
"""
from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
