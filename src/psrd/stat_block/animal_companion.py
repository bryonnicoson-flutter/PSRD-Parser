from psrd.stat_block.utils import colon_filter, default_closure, collapse_text
from psrd.universal import StatBlockSection, filter_name

def is_animal_companion(sb, book):
	fields = dict(sb.keys)
	if fields.has_key('AC') or fields.has_key("Ability Scores"):
		for detail in sb.details:
			if detail.__class__ == StatBlockSection and detail.name.endswith('th-Level Advancement'):
				return True
		if fields.has_key('Ability Scores'):
			return True
	return False

def animal_companion_parse_function(field):
	functions = {
		'ac': default_closure('ac'),
		'cmd': default_closure('cmd'),
		'attack': default_closure('attack'),
		'ability scores': default_closure('ability_scores'),
		'special abilities': default_closure('special_abilities'),
		'special qualities': default_closure('special_qualities'),
		'sq': default_closure('special_qualities'),
		'special attacks': default_closure('special_attacks'),
		'size': default_closure('size'),
		'speed': default_closure('speed'),
		'bonus feat': default_closure('bonus_feat')
	}
	return functions[field.lower()]

def parse_animal_companion(sb, book):
	ac = {'type': 'animal_companion', 'subtype': 'base', 'source': book, 'name': filter_name(sb.name.strip()), 'sections': []}
	text = []
	for key, value in sb.keys:
		animal_companion_parse_function(key)(ac, value)
	for detail in sb.details:
		if detail.__class__ == StatBlockSection and detail.name.endswith('th-Level Advancement'):
			advancement = {'level': detail.name[:3], 'source': book, 'type': 'animal_companion', 'name': filter_name(ac['name'])}
			for key, value in detail.keys:
				animal_companion_parse_function(key)(advancement, value)

			advancement['subtype'] = 'advancement'
			ac['sections'].append(advancement)
		else:
			text.append(detail)
	if ac["name"].endswith('th-Level Advancement'):
		ac['level'] = ac['name'][:3]
		ac['subtype'] = "advancement"
	if len(text) > 0:
		collapse_text(ac, text)
	return ac

