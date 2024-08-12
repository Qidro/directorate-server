from flask import request
from exceptions import ApiError
from service import file_service


def file_required(extensions: list = None, max_size: int = None):
    def _file_required(fn):
        def wrapper(*args, **kwargs):
            try:
                file = request.files['file']
            except KeyError:
                raise ApiError.BadRequest('File not found. Send file in field "file"')

            max_size_exist = max_size is not None
            if max_size_exist and file_service.get_file_size(file.stream) > max_size * (1024 * 1024):
                raise ApiError.BadRequest(f'File is too big (max size: {max_size}MB)')

            extensions_exist = extensions is not None
            file_ext = file_service.get_file_ext(file.filename)
            if extensions_exist and file_ext not in extensions:
                raise ApiError.BadRequest('Wrong file type')

            return fn(file, *args, **kwargs)

        return wrapper

    return _file_required
