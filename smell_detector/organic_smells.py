class ProjectSmells:

    def __init__(self):
        self.smelly_elements = []


    def add_smelly_class(self, smelly_class):
        self.smelly_elements.append(smelly_class)

    def get_total_smells(self):
        total_class = 0
        total_method = 0

        for e in self.smelly_elements:
            total_class_e, total_method_e = e.get_total_smells()
            total_class += total_class_e
            total_method += total_method_e

        return total_class, total_method
    
    def get_smell_for_class(self, path):
        for e in self.smelly_elements:
            if e.path == path:
                return e.get_total_smells()

        return 0,0
    # def __str__(self):
    #     total_class, total_method = self.get_total_smells()

    #     return f'Commit hash {len(self.smelly_elements)} smelly classes with a total of {total_class + total_method}' \
    #            f' smells {total_class} class-level smells and {total_method} method-level smell'

    class SmellyClass:
        def __init__(self, path):
            self.path = path

            self.class_smells = []
            self.method_smells = []

        def has_smells(self):
            return self.class_smells or self.method_smells

        def add_class_level_smells(self, smell_list):
            if smell_list is not None:
                self.class_smells += smell_list

        def get_class_smells(self):
            return self.class_smells

        def get_method_smells(self):
            return self.method_smells
            
        def get_total_smells(self):
            total_class = len(self.class_smells)
            total_method = len(self.method_smells)
            return total_class, total_method

