from app import app
from flask import render_template, redirect, url_for, request, jsonify
from report_of_monaco_2018_racing_bydujiy import main as rr
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger, swag_from
from dict2xml import dict2xml


api = Api(app)
swag = Swagger(app)


drive_data, start_data, end_data = rr.read_logs('app/static/data_files')
drivers_list = rr.get_drivers(drive_data)
race_report = rr.get_report(drive_data, start_data, end_data)


@app.route('/report/', methods=["GET"])
def report_result():
    order = request.args.get('order')
    report = rr.sort_result(race_report, order)
    return render_template('report/report.html', report=report)


@app.route('/report/drivers/', methods=["GET", "POST"])
def drivers_info():
    order = request.args.get('order')
    drivers = rr.sort_result(drivers_list, order)
    return render_template('report/drivers.html', drivers=drivers)


@app.route('/driver_result')
def driver_result():
    driver_id = request.args.get('driver_id')
    return redirect(url_for('driver', driver_id=driver_id))


@app.route('/report/drivers/<string:driver_id>')
def driver(driver_id):
    driver_report = rr.search_by_abbr(race_report, driver_id)
    return render_template('report/driver.html', driver_report=driver_report)


class Report(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('format', type=str,
                                 choices=['json', 'xml'], default='json')
        self.parser.add_argument('order', type=str, choices=['asc', 'desc'],
                                 default='asc')

    @swag_from('docs/report.yml')
    def get(self):
        args = self.parser.parse_args()
        response_format = args['format']
        order = args['order']
        report = rr.sort_result(race_report, order)
        dict_report = [
            {
                'abbr': item[0],
                'name': item[1],
                'team': item[2],
                'time': item[3]
            } for item in report
        ]
        if response_format == 'xml':
            return dict2xml(dict_report, wrap='racers', indent=' ')
        else:
            return jsonify(dict_report)


api.add_resource(Report, '/api/v1/racer-report')
