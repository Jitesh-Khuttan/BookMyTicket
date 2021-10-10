from flask_restful import Api
from code.resources.user import UserRegister, User, UserLogin
from code.resources.family import RegisterFamily, Family
from code.resources.member import Member, MemberDetails
from code.resources.parent_child import ParentChild, RetrieveParent, RetrieveChildren
from code.resources.sibling import Sibling, RetrieveSibling
from code.resources.grandparent import RetrieveGrandParent
from code.resources.cousin import RetrieveCousin

def initialize_urls(app):
	api = Api(app)

	#User APIs
	api.add_resource(UserRegister, '/user/register')
	api.add_resource(UserLogin, '/login')
	api.add_resource(User, '/user/<string:name>')

	#Family APIs
	api.add_resource(RegisterFamily, '/family/register')
	api.add_resource(Family, '/family/<int:family_id>')

	#Member APIs
	api.add_resource(Member, '/member')
	api.add_resource(MemberDetails, '/member/additional-details')

	#Relationships
	api.add_resource(ParentChild, '/parent')
	api.add_resource(RetrieveParent, '/parent/<int:member_id>')
	api.add_resource(RetrieveChildren, '/children/<int:member_id>')
	api.add_resource(Sibling, '/sibling')
	api.add_resource(RetrieveSibling, '/sibling/<int:member_id>')
	api.add_resource(RetrieveGrandParent, '/grandparent/<int:member_id>')
	api.add_resource(RetrieveCousin, '/cousin/<int:member_id>')

	return app