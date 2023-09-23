import os


class UtilsService:
    @staticmethod
    def root_dir():
        file_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(file_dir, ".."))
