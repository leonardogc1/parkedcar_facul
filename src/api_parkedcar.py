from flask import Blueprint
from flask_restx import Api

from controllers.Funcionario import funcionario_
from controllers.Veiculo import veiculo_

blueprint = Blueprint('api_parkedcar', __name__, url_prefix='/parked-car/v1.0')
api = Api(blueprint, title = 'Parked Car API', version = '1.0', description = 'Parked Car features', contact = 'leonardogalvaoc@gmail.com', catch_all_404s = True, ordered = True)

api.add_namespace(funcionario_)
api.add_namespace(veiculo_)
