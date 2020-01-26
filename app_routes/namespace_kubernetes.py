from flask_restplus import Namespace, Resource, fields, reqparse

from app_controllers.infrastructure.kubernetes import (
    kubernetesGetPodId
)
from app_controllers.infrastructure.docker import (
    dockerGetContainerId
)
from app_controllers.challenges.challenges import (
    challengesManageChallenge1
)

kubernetes_parser = reqparse.RequestParser()
kubernetes_parser.add_argument('challenge', help='{error_msg}', type=dict, location='json')
# kubernetes_parser.add_argument('action', choices=('apply','delete'), help='{error_msg}', type=dict, location='json')
# kubernetes_parser.add_argument('userName', help='{error_msg}', type=dict, location='json')
# kubernetes_parser.add_argument('clusterName', choices=('us-west1-a'), help='{error_msg}',  type=dict, location='json')
# kubernetes_parser.add_argument('serviceName', help='{error_msg}', type=dict, location='json')

api = Namespace('kubernetes', description='Academy related operations')

@api.route('/challenges/<string:challenge_id>')
class KubernetesDeploy(Resource):
    @api.doc('deploy_challenge')
    def post(self, challenge_id):
        args = kubernetes_parser.parse_args()
        try:
            print("post...")
            print(args)
            challengesManageChallenge1(args['challenge']['clusterName'],args['challenge']['userName'],args['challenge']['action'],args['challenge']['emailAddress'])
            return "success", 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
        except:
            return "error", 404
