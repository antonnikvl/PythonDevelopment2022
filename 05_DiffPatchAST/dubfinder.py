import sys
import inspect
from importlib import import_module
from ast import parse, walk, unparse
from difflib import SequenceMatcher
from textwrap import dedent

name_ast_list = []

def process_function(name, obj):
    ast_tree = parse(dedent(inspect.getsource(obj)))
    replace_attrs = ['name', 'id', 'arg', 'attr']
    for node in walk(ast_tree):
        for attr in replace_attrs:
            if hasattr(node, attr):
                setattr(node, attr, '_')
    name_ast_list.append((name, unparse(ast_tree)))

def recursive_traversal(parent_name, elem):
    for name, object in inspect.getmembers(elem):
        if inspect.isclass(object):
            if not name.startswith('__'):
                recursive_traversal(parent_name + '.' + name, object)
        elif inspect.ismethod(object) or inspect.isfunction(object):
            process_function(parent_name + '.' + name, object)

for module_name in sys.argv[1:]:
    imported_module = import_module(module_name)
    recursive_traversal(module_name, imported_module)

name_ast_list.sort(key=lambda name_ast: name_ast[0])

results = []

for i in range(len(name_ast_list)):
    for j in range(i + 1, len(name_ast_list)):
        ratio = SequenceMatcher(None, name_ast_list[i][1], name_ast_list[j][1]).ratio()
        if ratio > 0.95:
            results.append((name_ast_list[i][0], name_ast_list[j][0]))


for r in results:
    print(r[0], ':', r[1])