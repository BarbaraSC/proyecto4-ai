import hashlib
import os
import app


def allowed_file(filename):
    """
    Checks if the format for the file received is acceptable. For this
    particular case, we must accept only image files. This is, files with
    extension ".png", ".jpg", ".jpeg" or ".gif".

    Parameters
    ----------
    filename : str
        Filename from werkzeug.datastructures.FileStorage file.

    Returns
    -------
    bool
        True if the file is an image, False otherwise.
    """
    
    # Current implementation will allow any kind of file.
    file_ext = os.path.splitext(filename)[1]
    #extensions = ['UPLOAD_EXTENSIONS'] = [".png", ".jpg", ".jpeg", ".gif"]
    if file_ext not in [".png", ".jpg", ".jpeg", ".gif", ".PNG", ".JPG", ".JPEG", ".GIF"]:
        return False
    else:
        return True


def get_file_hash(file):
    """
    Returns a new filename based on the file content using MD5 hashing.
    It uses hashlib.md5() function from Python standard library to get
    the hash.

    Parameters
    ----------
    file : werkzeug.datastructures.FileStorage
        File sent by user.

    Returns
    -------
    str
        New filename based in md5 file hash.
    """
    # Current implementation will return the original file name.
    # TODO   

    extension = os.path.splitext(file.filename)[1]
    hashed_name = hashlib.md5(file.stream.read())
    file.stream.seek(0)

    return hashed_name.hexdigest() + extension
