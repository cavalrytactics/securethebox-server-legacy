from flask_restplus import Namespace, Resource, fields, reqparse
import requests
import time
airflow_parser = reqparse.RequestParser()
airflow_parser.add_argument('challenge', help='{error_msg}', type=dict, location='json')

api = Namespace('airflow', description='Airflow related operations')

@api.route('/challenges/<string:airflow_id>')
class airflowDeploy(Resource):
    @api.doc('deploy_challenge')
    def post(self, airflow_id):
        args = airflow_parser.parse_args()
        clusterName = args['challenge']['clusterName']
        userName = args['challenge']['userName']
        action = args['challenge']['action']
        try:

            headers = {
                'Cache-Control': 'no-cache',
                'Content-Type': 'application/json',
            }

            data = '{"conf":\"\
                        { \
                            \\"clusterName\\":\\"'+clusterName+'\\", \
                            \\"userName\\":\\"'+userName+'\\", \
                            \\"action\\":\\"'+action+'\\" \
                        } \
                    "}'

            requests.post('http://localhost:8080/api/experimental/dags/dag_main_challenge_service_traefik/dag_runs', headers=headers, data=data)

            return "success", 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
        except:
            return "error", 404