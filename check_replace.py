import os


class Scaner(object):
    def __init__(self) -> None:
        super().__init__()
        self.current_work_dir = ""
        self.all_filepath = []

    def get_current_work_dir(self):
        self.current_work_dir = os.path.dirname(__file__)

    def get_all_filepath(self, dir_path: str, ignore_path_set: set):
        '''
        TODO:
        1. ignore sets;
        2. only scan sets;
        '''
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if os.path.isdir(file_path):
                self.get_all_filepath(file_path, ignore_path_set)
            else:
                contain_flag = False
                for item in ignore_path_set:
                    if item in file_path:
                        contain_flag = True
                        break
                if contain_flag:
                    continue
                self.all_filepath.append(file_path)


class Examiner(object):
    def __init__(self, target_str: str, err_str: str) -> None:
        super().__init__()
        self.file_path = ""
        self.target_str = target_str
        self.err_str = err_str

    def insert_file(self, file_path):
        self.file_path = file_path

    def check_and_replace(self):
        file_content = ""
        with open(self.file_path, "r", encoding="utf-8") as file_object:
            for line in file_object.readlines():
                file_content += self.str_find_replace(
                    line=line, target_str=self.target_str, err_str=self.err_str)
        with open(self.file_path, "w+", encoding="utf-8") as file_object:
            file_object.write(file_content)

    @staticmethod
    def str_find_replace(line: str, target_str: str, err_str: str) -> str:
        if line.find(target_str) != -1:
            pass
        if line.find(err_str) != -1:
            line = line.replace(err_str, target_str)
        return line


if __name__ == "__main__":
    scaner = Scaner()
    scaner.get_current_work_dir()
    print("current_work_dir:{current_work_dir}\n".format(
        current_work_dir=scaner.current_work_dir))
    scaner.get_all_filepath(scaner.current_work_dir, ignore_path_set={
                            ".git", ".py", ".vscode", ".DS_Store"})

    examiner = Examiner(target_str="command=ssh -tt -i ",
                        err_str="command=ssh -i ")
    for file_path in scaner.all_filepath:
        examiner.insert_file(file_path=file_path)
        examiner.check_and_replace()
