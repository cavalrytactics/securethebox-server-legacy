from flask_restplus import Namespace, Resource, fields, reqparse
from app_controllers.challenges.gitlab_manager import GitlabManager
import os

gitlab_parser = reqparse.RequestParser()
gitlab_parser.add_argument('challenge', help='{error_msg}', type=dict, location='json')

gm = GitlabManager()
api = Namespace('gitlab', description='Gitlab related operations')

@api.route('/securethebox/github')
class GitlabSetup(Resource):
    @api.doc('test')
    def post(self):
        args = gitlab_parser.parse_args()
        try:
            print("github")
            return "success", 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
        except:
            return "error", 404