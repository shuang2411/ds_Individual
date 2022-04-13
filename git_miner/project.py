from pydriller import Repository
from util_module import RepositoryClone
from pydriller import Git
from smell_detector import Organic
from smell_detector import OrganicParser



def _path_to_class(str):
    idx1 = str.find("org")
    idx2 = str.find(".java")

    
    if idx1 == -1 or idx2 == -1:
        raise Exception('Sub string not found!')
    
    sliced = str[idx1:idx2].split('/')

    return ".".join(sliced)

class Project:

    def __init__(self, name, url, branch, starting_commit, ending_commit):
        self.name = name
        self.branch = branch
        self.url = url
        self.starting_commit = starting_commit
        self.ending_commit = ending_commit

        self.git = None

        #  {author_name: n of modified files}
        self.author_modified_files = {}
        self.commit_most_modified_lines = {'hash': None, 'lines': 0}

    def collect_statistics(self):
        repo_local_path = RepositoryClone.clone(self.name, self.url, self.branch)
        repo = Repository(self.url, from_commit=self.starting_commit, to_commit=self.ending_commit)

        generator = repo.traverse_commits()

        for commit in generator:
            project_smells = self.detect_smells_all_commit(commit.hash,repo_local_path)
            
            for files in commit.modified_files :
                path = files.new_path
                if '/test' in path:
                    continue
                
                class_name = _path_to_class(path)
                
                total_class, total_method = project_smells.get_smell_for_class(class_name)
                print(total_class, total_method)
                return
           

    def process_commit(self, commit, project_smells):
        modified_files = commit.modified_files 
        
        for files in modified_files:
            path = files.new_path
            if '/test' in path:
                continue
            
            class_name = _path_to_class(path)
            
            total_class, total_method = project_smells.get_smell_for_class(class_name)
            print(total_class, total_method)
        # print(f'{modified_files} files is modified in commit {commit.hash}')
        
        # if author_name in self.author_modified_files:
        #     self.author_modified_files[author_name] += modified_files
        # else:
        #     self.author_modified_files[author_name] = modified_files

        # modified_lines = commit.lines
        # if self.commit_most_modified_lines['lines'] < modified_lines:
        #     self.commit_most_modified_lines = {'hash': commit.hash, 'lines': modified_lines}

    def get_statistics(self):
        _hash, _lines = self.commit_most_modified_lines.values()

        author_name = max(self.author_modified_files, key=self.author_modified_files.get)

        return f'Project name: {self.name}:\n ' \
               f'\tThe author with most modifications is {author_name} with ' \
               f'{self.author_modified_files[author_name]} modified files.\n' \
               f'\tThe commit with most modifie lines is {_hash} with {_lines} modified lines.'

    def detect_smells_initial_commit(self):
        repo_local_path = RepositoryClone.clone(self.name, self.url, self.branch)

        # we want to checkout the project to initial commit
        self.git = Git(repo_local_path)
        self.git.checkout(self.starting_commit)

        # detect the code smells
        organic = Organic(self.name, repo_local_path)
        smell_file_path = organic.detect_smells()
        
        
        parser = OrganicParser(smell_file_path)
        project_smells = parser.parse()
        print(project_smells)
        
        
    def detect_smells_all_commit(self,hash,repo_local_path):
        repo_local_path = RepositoryClone.clone(self.name, self.url, self.branch)

        # we want to checkout the project to initial commit
        self.git = Git(repo_local_path)
        self.git.checkout(hash)

        # detect the code smells
        organic = Organic(self.name, repo_local_path)
        smell_file_path = organic.detect_smells()
        
        
        parser = OrganicParser(smell_file_path)
        project_smells = parser.parse()
        return project_smells
        
        

