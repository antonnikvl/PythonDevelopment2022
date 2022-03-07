import cmd
import pynames
import shlex
import importlib
import inspect
from pkgutil import iter_modules

class PynamesCmd(cmd.Cmd):
    gen_names = []
    class_names = []
    complex_names = []
    complex_class_names = {}
    classes_map = {}

    for submodule in iter_modules(pynames.generators.__path__):
        short_name = submodule.name
        gen_names.append(short_name)
        full_name = 'pynames.generators.' + submodule.name
        module = importlib.import_module(full_name)
        class_list = []
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and obj.__module__ == full_name:
                class_list.append((name.replace('FullnameGenerator', '').replace('NamesGenerator', '').replace('Names', '').replace('Generator', ''), obj))
        if len(class_list) == 1:
            classes_map[short_name] = class_list[0][1]
            classes_map[class_list[0][0]] = class_list[0][1]
            class_names.append(class_list[0][0])
        else:
            m = {}
            names = []
            for n, c in class_list:
                m[n] = c
                names.append(n)
            complex_names.append(short_name)
            classes_map[short_name] = m
            complex_class_names[short_name] = names 

    lang_names = ['EN', 'RU']
    gender_names = ['female', 'male']

    def __init__(self, *args, **kwargs):
        super(PynamesCmd, self).__init__(*args, **kwargs)
        self.lang = 'native'

    def find_names_with_prefix(self, prefix, names):
        if prefix:
            return [
                n for n in names
                if n.startswith(prefix)
            ]
        else:
            return names

    def do_language(self, line):
        'Choose language'
        if len(line) == 0:
            print('None language name entered')
        elif not line in self.lang_names:
            print('Unknown language')
        else:
            l = line.lower()
            self.lang = l

    def complete_language(self, text, line, start_index, end_index):
        return self.find_names_with_prefix(text, self.lang_names)

    def do_generate(self, line):
        'Generate name'
        s = shlex.split(line)
        correct = True
        g = 'm'
        if len(s) == 0:
            print('Command should include at least a class name')
            correct = False
        elif not s[0] in self.classes_map:
            print('Unknown class name')
            correct = False
        else:
            res_class = self.classes_map[s[0]]
            idx = 0
            if s[0] in self.complex_class_names:
                if len(s) < 2:
                    print('Enter subclasss name too')
                    correct = False
                elif not s[1] in res_class:
                    print('Unknown subclass')
                    correct = False
                else:
                    res_class = res_class[s[1]]
                idx += 1
            if len(s) - idx > 1:
                g = s[idx + 1]
                if not g in self.gender_names:
                    print('Unknown gender')
                    correct = False
                else:
                    g = g[0]
        if correct:
            gen = res_class()
            try:
                print(gen.get_name_simple(gender=g, language=self.lang))
            except Exception:
                print(gen.get_name_simple(gender=g))

    def complete_helper(self, prefix, line, last_arg_variants):
        commands = shlex.split(line)
        empty = not (prefix and not prefix.isspace())
        if len(commands) == 1 and empty:
            return self.find_names_with_prefix(prefix, self.class_names + self.complex_names)
        elif len(commands) == 2 and not empty:
            if prefix[0].isupper():
                return self.find_names_with_prefix(prefix, self.class_names)
            else:
                return self.find_names_with_prefix(prefix, self.gen_names + self.complex_names)
        elif (len(commands) == 4 or (len(commands) == 3 and empty)) and ((commands[1] in self.complex_class_names) and (commands[2] in self.complex_class_names[commands[1]])):
            return self.find_names_with_prefix(prefix, last_arg_variants)
        elif (len(commands) == 3 or (len(commands) == 2 and empty)) and (commands[1] in self.complex_names):
            return self.find_names_with_prefix(prefix, self.complex_class_names[commands[1]])
        elif (len(commands) == 3 or (len(commands) == 2 and empty)) and (commands[1] in self.class_names or commands[1] in self.gen_names):
            return self.find_names_with_prefix(prefix, last_arg_variants)
        else:
            return []

    def complete_generate(self, prefix, line, start_index, end_index):
        return self.complete_helper(prefix, line, self.gender_names)

    def do_info(self, line):
        'Print info about names count or available languages'
        s = shlex.split(line)
        correct = True
        g = 'm'
        if len(s) == 0:
            print('Command should include at least a class name')
            correct = False
        elif not s[0] in self.classes_map:
            print('Unknown class name')
            correct = False
        else:
            res_class = self.classes_map[s[0]]
            idx = 0
            if s[0] in self.complex_class_names:
                if len(s) < 2:
                    print('Enter subclasss name too')
                    correct = False
                elif not s[1] in res_class:
                    print('Unknown subclass')
                    correct = False
                else:
                    res_class = res_class[s[1]]
                idx += 1
        if correct:
            gen = res_class()
            if len(s) - idx > 1:
                g = s[idx + 1]
                if g == 'male':
                    print(gen.get_names_number(genders='m'))  
                elif g == 'female':
                    print(gen.get_names_number(genders='f'))
                elif g == 'language':
                    result = []
                    for l in ['en', 'ru']:
                        has_lang = True
                        try:
                            gen.get_name_simple(language=l)
                        except Exception:
                            has_lang = False
                        if has_lang:
                            result.append(l)
                    print(*result)
                else:
                    print('Unknown parameter')
            else:
                print(gen.get_names_number())

    def complete_info(self, prefix, line, start_index, end_index):
        genders_lang = self.gender_names + ['language']
        return self.complete_helper(prefix, line, genders_lang)

pynamesCmd = PynamesCmd()
pynamesCmd.cmdloop()