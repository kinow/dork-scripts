#!/usr/bin/env python3

# requirements: javalang

import os, re, sys
from pprint import pprint as pp

import javalang

"""
Because there is no way :)
"""

# Patterns we do not want in an Entity
ENTITY_FILTER_PATTERNS = [
	'^import .*javax\.xml\.bind.*',
	'^@Xml.*'
]

# Patterns we do not want in a DTO
DTO_FILTER_PATTERNS = [
	'^import .*javax\.persistence.*',
	'^@Table.*',
	'^@Entity.*',
	'^@Id.*',
	'^@Column.*',
	'^@GeneratedValue.*',
	'^@Transient.*',
	'^@Temporal.*',
	'^@Inheritance.*',
	'^@DiscriminatorColumn.*'
]

# Patterns we do not want in a DTO

class ParseResult(object):

	def __init__(self):
		self.body = ''
		self.file_name = ''

class Parser(object):

	def __init__(self):
		self.class_name = 'SomeEntity'

	def filter_line(self, line, pattern_list):
		"""
		Parse a line, applying a blacklist list of patterns.
		"""
		for pattern in pattern_list:
			m = re.search(pattern, line)
			if m:
				return None

		# Try to find the class name
		if self.class_name == 'SomeEntity':
			m = re.search('.*class\s+([^\s]+)\s+.*', line)
			if m:
				self.class_name = m.group(1).strip()

		return line

	def parse(file):
		raise Exception('Not implemented!')

	def get_output_file_name(self):
		return self.class_name + '.java'

class EntityParser(Parser):

	def parse(self, class_file):
		parse_result = ParseResult()
		entity_contents = []
		for line in class_file:
			line = line.strip()
			result = self.filter_line(line, ENTITY_FILTER_PATTERNS)
			if result != None:
				entity_contents.append(result)

		content = '\n'.join(entity_contents)
		parse_result.body = content
		parse_result.file_name = self.get_output_file_name()
		return parse_result

class DtoParser(Parser):

	# From: https://stackoverflow.com/questions/12410242/python-capitalize-first-letter-only
	def _upperfirst(self, x):
		return x[0].upper() + x[1:]

	def _lowerfirst(self, x):
		return x[0].lower() + x[1:]

	def parse(self, class_file):
		parse_result = ParseResult()
		dto_contents = []
		for line in class_file:
			line = line.strip()
			result = self.filter_line(line, DTO_FILTER_PATTERNS)
			if result != None:
				dto_contents.append(result)

		initial_content = '\n'.join(dto_contents)

		tree = javalang.parse.parse(initial_content)
		lines = []

		# package...
		lines.append('package ' + tree.package.name + ';')
		lines.append('')

		# imports...
		for imp in tree.imports:
			lines.append('import ' + imp.path + ';')

		lines.append('')

		# annotations...
		class_decl = tree.types[0]
		for ann in class_decl.annotations:
			annotation = '@'+ann.name+'('
			elems_values = []
			if ann.element != None:
				if type(ann.element) is javalang.tree.MemberReference:
					elems_values.append(ann.element.qualifier + '.' + ann.element.member)
				else:
					for elem in ann.element:
						elems_values.append(elem.name + '=' + elem.value.value)
				annotation += ','.join(elems_values)
			annotation += ')'
			lines.append(annotation)

		# class...
		lines.append('public class ' + class_decl.name + 'PO extends BasePO<' + class_decl.name + '> implements Serializable {')
		lines.append('')

		# constructor...
		lines.append('public ' + class_decl.name + 'PO(' + class_decl.name + ' entity) {')
		lines.append('super(entity);')
		lines.append('}')
		lines.append('')

		# transform the fields into methods...

		for field in class_decl.fields:
			has_xml_annotation = False
			for ann in field.annotations:
				m = re.search('^Xml.*', ann.name)
				if m:
					annotation = '@'+ann.name+'('
					elems_values = []
					if ann.element != None:
						if type(ann.element) is javalang.tree.MemberReference:
							elems_values.append(ann.element.qualifier + '.' + ann.element.member)
						else:
							for elem in ann.element:
								elems_values.append(elem.name + '=' + elem.value.value)
						annotation += ','.join(elems_values)
					annotation += ')'
					lines.append(annotation)
					has_xml_annotation = True

			if has_xml_annotation:
				lines.append('@JsonGetter')
				lines.append('public ' + field.type.name + ' get' + self._upperfirst(field.declarators[0].name) + '() {')
				lines.append('    return entity.get' + self._upperfirst(field.declarators[0].name) + '();')
				lines.append('}')
				lines.append('')

				lines.append('@JsonSetter')
				lines.append('public void set' + self._upperfirst(field.declarators[0].name) + '(' + field.type.name + ' ' + self._lowerfirst(field.declarators[0].name) + ') {')
				lines.append('    entity.set' + self._upperfirst(field.declarators[0].name) + '(' + self._lowerfirst(field.declarators[0].name) + ');')
				lines.append('}')
				lines.append('')


		# close class
		lines.append('}')
		lines.append('')

		content = '\n'.join(lines)

		parse_result.body = content
		parse_result.file_name = self.get_output_file_name()
		return parse_result

	def get_output_file_name(self):
		return self.class_name + 'PO.java'

def main():
	"""
	The input for the program is a FILE that contains a Java class.

	The Java class contains a Hibernate Entity. Besides an Entity, the class
	may also be a DTO.

	The program will create a file for the class with only the Hibernate Entity
	related fields and methods. And will create another file for the DTO.
	"""
	# From: https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-python
	script_dir 		= os.path.dirname(__file__)
	abs_file_path 	= os.path.join(script_dir, 'class.txt')

	entity_parser = EntityParser()
	dto_parser	  = DtoParser()

	with open(abs_file_path, 'r') as f:
		parse_result = entity_parser.parse(f)
		with open(parse_result.file_name, 'w') as o:
			o.write(parse_result.body)

	with open(abs_file_path, 'r') as f:
		parse_result = dto_parser.parse(f)
		with open(parse_result.file_name, 'w') as o:
			o.write(parse_result.body)

if __name__ == '__main__':
	main()

sys.exit(0)
