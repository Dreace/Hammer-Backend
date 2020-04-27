from flask_jwt import jwt_required, current_identity

from plugins.user import api
from utils.check_authority import permission_required


@api.route('/currentUser')
@jwt_required()
@permission_required(['admin'])
def user_current_user():
    return {
        'code': 0,
        'data': {
            'name': current_identity.username,
            'authority': current_identity.authority,
            'avatar': 'https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png',
        }
    }
