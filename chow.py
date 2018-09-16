#!/usr/bin/env python
'''
AndelaEats Chow CLI Tool
* Usage: python chow.py
*
* Command Line Arguments
* 	make:model name eg. python chow.py make:model user [--with_repo [_controller] ]
*	make:repo name eg. python chow.py make:repo user
*	make:blueprint name eg. python chow.py make:blueprint vendors [--url_prefix=vendors]
*	make:controller name eg. python chow.py make:controller user
*	make:test name eg python chow.py make:test test_meal_repo - This command will parse paths and write to the valid paths provided
*	make:factory name eg python chow.py make:factory role
*
*
* NOTE: Please use the singular form of the words. The Chow will auto generate the plural forms where needed.
'''

import sys, os
import inflect

inflect_engine = inflect.engine()

def to_pascal_case(word, sep='_'):
	return ''.join(list(map(lambda x: x.capitalize(), word.split(sep))))

def create_model(name):
	name_clean = to_pascal_case(name)
	model_stub = '''from .base_model import BaseModel, db

class {model_name}(BaseModel):
	__tablename__ = '{table_name}'
	'''.format(model_name=name_clean, table_name=inflect_engine.plural(name))
	
	model_file_path = 'app/models/{}.py'.format(name)
	write_file(model_file_path, model_stub)
	return name_clean, model_file_path

def create_repo(name):
	name_clean = to_pascal_case(name) 		#''.join(list(map(lambda x: x.capitalize(), name.split('_'))))
	repo_stub = '''from app.repositories.base_repo import BaseRepo
from app.models.{name} import {name_clean}

class {name_clean}Repo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, {name_clean})'''.format(name=name, name_clean=name_clean)
	repo_file_path = 'app/repositories/{}_repo.py'.format(name)
	write_file(repo_file_path, repo_stub)
	return name_clean, repo_file_path

def create_blueprint(name, url_prefix=None):
	uprefix = '' if url_prefix is None else inflect_engine.plural(url_prefix)
	blueprint_stub = '''from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth

url_prefix = '{{}}/{url_prefix}'.format(BaseBlueprint.base_url_prefix)
{name}_blueprint = Blueprint('{name}', __name__, url_prefix=url_prefix)
	'''.format(name=name, url_prefix=uprefix)
	blueprint_file_path = 'app/blueprints/{}_blueprint.py'.format(name)
	write_file(blueprint_file_path, blueprint_stub)
	return name, blueprint_file_path

def create_controller(name):
	name_clean = to_pascal_case(name)
	controller_stub = '''from app.controllers.base_controller import BaseController

class {name}Controller(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
	'''.format(name=name_clean)
	
	controller_file_path = 'app/controllers/{}_controller.py'.format(name)
	write_file(controller_file_path, controller_stub)
	return name_clean, controller_file_path

def create_test(name, test_path=None):
	name_clean = to_pascal_case(name)
	test_file_path = 'tests'
	
	if test_path:
		os.makedirs(os.path.join(test_file_path, test_path), mode=0o777, exist_ok=True)
		test_file_path = os.path.join(test_file_path, test_path)
	
	test_stub = '''from tests.base_test_case import BaseTestCase

class {name}(BaseTestCase):

	def setUp(self):
		self.BaseSetUp()
		'''.format(name=name_clean)
	test_file_path = '{}/{}.py'.format(test_file_path, name)
	write_file(test_file_path, test_stub)
	return name_clean, test_file_path

def create_factory(name):
	name_clean = to_pascal_case(name)
	test_stub = '''import factory
from faker import Faker
from app.utils import db
from app.models.{name} import {name_clean}

fake = Faker()
# Please define model field values outside of the factory class. A problem with how factory-boy serializes keys.
# example
# fake_name = fake.name()
# fake_address = fake.address()

class {name_clean}Factory(factory.alchemy.SQLAlchemyModelFactory):

	class Meta:
		model = {name_clean}
		sqlalchemy_session = db.session
	
	id = factory.Sequence(lambda n: n)
	# name = fake_name
	# address = fake_address
		
			'''.format(name_clean=name_clean, name=name)
	factory_file_path = 'factories/{}_factory.py'.format(name)
	write_file(factory_file_path, test_stub)
	return name_clean, factory_file_path
	
	pass

def write_file(file_path, file_content):
	with open(file_path, 'w', encoding='utf-8') as file_handle:
		file_handle.write(file_content)

if __name__ == '__main__':
	
	args = sys.argv
	command = args[1]
	
	if command == 'make:model' or command == 'make:models':
		name = args[2]
		
		extras = list()
		if len(args) > 3:
			extras = args[3].split('--with_')[1].split('_')
		m = create_model(name)
		print('Model: {} Location: {}'.format(m[0], m[1]))
		
		if 'controller' in extras:
			c = create_controller(name=name)
			print('Controller: {}Controller Location: {}'.format(c[0], c[1]))
			
		if 'repo' in extras:
			r = create_repo(name=name)
			print('Repository: {}Repo Location: {}'.format(r[0], r[1]))
		
	
	if command == 'make:repo' or command == 'make:repos':
		name = args[2]
		r = create_repo(name=name)
		print('Repository: {}Repo Location: {}'.format(r[0], r[1]))
	
	
	if command == 'make:blueprint' or command == 'make:blueprints':
		name = args[2]
		url_prefix = None
		
		if len(args) > 3:
			url_prefix = args[3].split('--url_prefix=')[1]
			
		b = create_blueprint(name, url_prefix)
		print('Blueprint: {} Location: {}'.format(b[0], b[1]))
	
	
	if command == 'make:controller' or command == 'make:controllers':
		name = args[2]
		c = create_controller(name=name)
		print('Controller: {}Controller Location: {}'.format(c[0], c[1]))
		
	
	if command == 'make:test' or command == 'make:tests':
		name = args[2]
		test_path = None
		# check if test contains path separator.
		if name.find('/') > -1:
			arr = os.path.split(name)
			test_path = arr[0]
			name = arr[1]
		
		t = create_test(name=name, test_path=test_path)
		print('Test: {} Created Location: {}'.format(t[0], t[1]))
	
	
	if command == 'make:factory' or command == 'make:factories':
		name = args[2]
		
		f = create_factory(name)
		print('Factory: {}Factory Location: {}'.format(f[0], f[1]))
		
	