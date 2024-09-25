import pytest
from core.libs.exceptions import FyleError

def test_fyle_error_initialization():
    error = FyleError(status_code=404, message="Not Found")
    assert isinstance(error, Exception)
    assert error.status_code == 404
    assert error.message == "Not Found"

def test_fyle_error_default_status_code():
    error = FyleError(status_code=None, message="Test Message")
    assert error.status_code == 400  

def test_fyle_error_to_dict():
    error = FyleError(status_code=500, message="Internal Server Error")
    error_dict = error.to_dict()
    assert isinstance(error_dict, dict)
    assert error_dict['message'] == "Internal Server Error"
    assert 'status_code' not in error_dict 

def test_fyle_error_inheritance():
    error = FyleError(status_code=403, message="Forbidden")
    assert isinstance(error, Exception)
    assert isinstance(error, FyleError)

def test_fyle_error_str_representation():
    error = FyleError(status_code=400, message="Bad Request")
    assert str(error) == ""  

def test_fyle_error_repr_representation():
    error = FyleError(status_code=401, message="Unauthorized")
    assert repr(error).startswith("<FyleError")