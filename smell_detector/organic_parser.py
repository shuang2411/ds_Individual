import json
from .organic_smells import ProjectSmells

def _get_smells(data):
    smells = []

    if not data:
        return None

    for d in data:
        smells.append(d['name'])

    return smells


class OrganicParser:

    def __init__(self,smell_file_path):
        self.smell_file = smell_file_path

    def parse(self) -> ProjectSmells:
        with open(self.smell_file) as smell_file:
            data = json.load(smell_file)

        project_smells = ProjectSmells()


        for d in data:
            if '/test' in d['sourceFile']['fileRelativePath']:
                continue

            smelly_class = project_smells.SmellyClass(d['fullyQualifiedName'])
            smelly_class.add_class_level_smells(_get_smells(d['smells']))
            
            print(smelly_class.fully_qualified_name)
            
            for method in d['methods']:
                if method['smells']:
                    smelly_class.add_class_level_smells(_get_smells(method['smells']))

            if smelly_class.has_smells():
                project_smells.add_smelly_class(smelly_class)

        return project_smells
