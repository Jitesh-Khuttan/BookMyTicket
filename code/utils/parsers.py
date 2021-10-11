from flask_restful import reqparse


def get_user_credential_parser():	
	_user_parser = reqparse.RequestParser()
	_user_parser.add_argument('username', type=str, required=True, help="Please provide the username")
	_user_parser.add_argument('password', type=str, required=True, help="Please provide the password.")

	return _user_parser


def get_city_parser():	
	_city_parser = reqparse.RequestParser()
	_city_parser.add_argument('city_name', type=str, required=True, help="Please provide the city name.")
	_city_parser.add_argument('pincode', type=int, required=True, help="Please provide city pincode,")

	return _city_parser

def get_parentchild_request_parser():	
	_pc_parser = reqparse.RequestParser()
	_pc_parser.add_argument('parent_id', type=str, required=True, help="Please provide the parent_id.")
	_pc_parser.add_argument('child_id', type=str, required=True, help="Please provide the child id.")

	return _pc_parser


def get_sibling_request_parser():	
	_sibling_parser = reqparse.RequestParser()
	_sibling_parser.add_argument('sibling_id1', type=str, required=True, help="Please provide the sibling 1's id.")
	_sibling_parser.add_argument('sibling_id2', type=str, required=True, help="Please provide the sibling 2's id.")

	return _sibling_parser


def get_member_request_parser():
	_member_parser = reqparse.RequestParser()
	_member_parser.add_argument('family_id', type=str, required=True, help="Please provide the family id.")
	_member_parser.add_argument('first_name', type=str, required=True, help="Please provide the first name.")
	_member_parser.add_argument('last_name', type=str, required=True, help="Please provide the last name.")
	_member_parser.add_argument('address', type=str, required=False, help="Please provide the address.")
	_member_parser.add_argument('email', type=str, required=False, help="Please provide the email id.")
	_member_parser.add_argument('phone_number', type=str, required=False, help="Please provide the phone number.")
	_member_parser.add_argument('birth_date', type=str, required=True, help="Please provide the birth date.")

	return _member_parser

def get_member_post_later_data_request_parser():
	_member_parser = reqparse.RequestParser()
	_member_parser.add_argument('member_id', type=str, required=True, help="Please provide the member_id.")
	_member_parser.add_argument('address', type=str, required=False, help="Please provide the address.")
	_member_parser.add_argument('email', type=str, required=False, help="Please provide the email id.")
	_member_parser.add_argument('phone_number', type=str, required=False, help="Please provide the phone number.")

	return _member_parser

def get_member_update_data_request_parser():
	_member_parser = reqparse.RequestParser()
	_member_parser.add_argument('member_id', type=str, required=True, help="Please provide the member_id.")
	_member_parser.add_argument('current_address', type=str, required=False, help="Please provide the current address.")
	_member_parser.add_argument('new_address', type=str, required=False, help="Please provide the new address.")
	_member_parser.add_argument('current_email', type=str, required=False, help="Please provide the current email id.")
	_member_parser.add_argument('new_email', type=str, required=False, help="Please provide the new email id.")
	_member_parser.add_argument('current_phone_number', type=str, required=False, help="Please provide the current phone number.")
	_member_parser.add_argument('new_phone_number', type=str, required=False, help="Please provide the new phone number.")

	return _member_parser

def get_member_delete_parser():
	_member_parser = reqparse.RequestParser()
	_member_parser.add_argument('member_id', type=str, required=True, help="Please provide the member_id.")

	return _member_parser