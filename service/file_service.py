import hashlib
import os
from uuid import uuid4
from werkzeug.datastructures import FileStorage
from constants.constants import DOCUMENT_EXT, ARCHIVE_EXT
from exceptions import ApiError
from models import File
import magic


def get_file_type(stream):
    header = stream.read(1024)
    stream.seek(0)
    file_format = magic.from_buffer(header, mime=True).split('/')
    return file_format[0]


def get_file_hash(stream):
    sha1sum = hashlib.sha1()

    chunk = stream.read(2 ** 16)
    while len(chunk) != 0:
        sha1sum.update(chunk)
        chunk = stream.read(2 ** 16)

    stream.seek(0)
    return sha1sum.hexdigest()


def get_file_size(stream):
    size = stream.seek(0, os.SEEK_END)
    stream.seek(0)
    return size


def get_file_ext(filename: str):
    split_name = filename.split('.')
    return '.' + split_name[-1] if len(split_name) >= 2 else ''


def get_folder(file_type: str, file_ext: str):
    if file_type == 'application' and file_ext in DOCUMENT_EXT:
        return 'documents'
    elif file_type == 'application' and file_ext in ARCHIVE_EXT:
        return 'archives'
    elif file_type == 'image':
        return 'images'
    else:
        return 'others'


def save_file(file: FileStorage):
    file_hash = get_file_hash(file.stream)
    file_type = get_file_type(file.stream)
    file_ext = get_file_ext(file.filename)
    folder = get_folder(file_type, file_ext)

    exist_file = File.get_or_none(hash=file_hash)
    if not exist_file:
        user_files_folder = os.environ.get("USER_FILES_FOLDER")
        url = f'{folder}/{file_hash + get_file_ext(file.filename)}'
        file.save(f'{user_files_folder}/{url}')
    else:
        url = exist_file.url

    new_file = File(
        id=str(uuid4()),
        hash=file_hash,
        url=url,
        filename=file.filename
    )
    new_file.save(force_insert=True)
    return new_file


def get_file(file_id: str):
    file = File.get_or_none(id=file_id)
    if not file:
        raise ApiError.FileNotFound()

    user_files_folder = os.environ.get("USER_FILES_FOLDER")
    url = f'{user_files_folder}/{file.url}'
    if not os.path.isfile(url):
        raise ApiError.FileNotFound()

    return url, file.filename
