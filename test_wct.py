from driver import print_report, build_dir_name, process_default_args, make_dir, process_std_exceptions
import datetime
import pytest
import os
import shutil
from selenium.common.exceptions import TimeoutException, WebDriverException

# THIS DOCUMENT CONTAINS AUTOMATED UNIT TESTS. IT IS NOT REQUIRED FOR THE EXECUTION OF THE WEBCAPTURETOOL.


# test that the report is being printed and calculating correctly
def test_print_report(capsys):
    print_report(5, 5, 0, 1, False)
    captured = capsys.readouterr()
    assert captured.out == '\n*====================*\n Final Report        \n\n Total Processed: 11  \n Total Successful: 10 \n Total Failures: 1   \n*====================*\n'

def test_print_extended(capsys):
    print_report(5,5,0,1,True)
    captured = capsys.readouterr()
    assert captured.out == "\n*====================*\n Final Report        \n\n Total Processed: 11  \n Total Successful: 10 \n Total Failures: 1   \n*====================*\n\n*====================*\n Extended Report        \n HTTPS: 5\n HTTP: 5\n Timeout: 0\n Other Errors: 1\n*====================*\n"

# test that build_file_name is constructing and returning the file name as intended using datetime and string formatting
def test_build_dir_name():
    current_time = datetime.datetime.now()
    function_result = build_dir_name()
    comparison_value = "./" + current_time.strftime("%Y%m%d_%H%M%S") + "_screenshots"
    assert function_result == comparison_value


def test_process_default_args_success():
    argv = ["placeholder value", "final.csv"] # construct argv array for test
    assert process_default_args(argv) == "final.csv"


def test_process_default_args_fail(): # test that a nonexistent csv file is detected and that the program exits
    argv = ["placeholder", "nonexistent.csv"]
    with pytest.raises(SystemExit) as exc_info:
        process_default_args(argv)
    assert exc_info.value.code == "Error: file not found."


def test_process_default_args_noargs(): # test that program exits if no arguments passed
    argv = ["placeholder"]
    with pytest.raises(SystemExit) as exc_info:
        process_default_args(argv)
    assert exc_info.value.code == "Error: no arguments provided."


def test_process_default_args_help(): # verify that -h help flag is detected successfully
    argv = ["placeholder","-h"]
    with pytest.raises(SystemExit) as exc_info:
        process_default_args(argv)
    assert exc_info.value.code == "Usage: python driver.py <csv file name>"

def test_make_dir_success(): # verify directory created successfully
    name = build_dir_name()
    status = make_dir(name)
    status = (status == 0) and (os.path.exists(name))
    if os.path.exists(name): # cleanup
        shutil.rmtree(name)
    else:
        assert False
    assert (status)

def test_make_dir_fail():
    name = build_dir_name()
    make_dir(name) # make dir, then try and make again to verify name conflict handled correctly
    with pytest.raises(SystemExit) as exc_info:
        make_dir(name)
    if os.path.exists(name): # cleanup
        shutil.rmtree(name)
    else:
        assert False
    assert exc_info.value.code == "Error: directory already exists."

def test_process_default_args_timeout(): # test that timeout is processed successfully
    LOG_FILE = './webcapturetesting.txt'
    e = TimeoutException("Test Timeout")
    url = "test.com"
    result = process_std_exceptions(LOG_FILE, e, url, True)
    if os.path.exists(LOG_FILE): #cleanup
        os.remove(LOG_FILE)
    else:
        assert False # fail test if file not found, since means did not write to output file as needed
    assert 'timeout' == result

def test_process_default_args_timeout_nobool(): # test without the timeout boolean
    LOG_FILE = './webcapturetesting.txt'
    e = TimeoutException("Test Timeout No Bool")
    url = "test.com"
    result = process_std_exceptions(LOG_FILE, e, url)
    if os.path.exists(LOG_FILE): #cleanup
        os.remove(LOG_FILE)
    else:
        assert False # fail test if file not found, since means did not write to output file as needed
    assert 'misc' == result

def test_process_default_args_timeout_false(): # test timeout with False as the bool
    LOG_FILE = './webcapturetesting.txt'
    e = TimeoutException("Test Timeout False")
    url = "test.com"
    result = process_std_exceptions(LOG_FILE, e, url, False)
    if os.path.exists(LOG_FILE): #cleanup
        os.remove(LOG_FILE)
    else:
        assert False # fail test if file not found, since means did not write to output file as needed
    assert 'misc' == result

def test_process_default_args_nss(): # test nssFailure processing
    LOG_FILE = './webcapturetesting.txt'
    e = WebDriverException("e=nssFailure")
    url = "test.com"
    result = process_std_exceptions(LOG_FILE, e, url)
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    else:
        assert False
    assert 'nssFailure' == result

def test_process_default_args_connexion(): # test connectionFailure processing
    LOG_FILE = './webcapturetesting.txt'
    e = WebDriverException("e=connectionFailure")
    url = "test.com"
    result = process_std_exceptions(LOG_FILE, e, url)
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    else:
        assert False
    assert 'connexionfailure' == result

def test_process_default_args_dns(): # test DNSnotfound processing
    LOG_FILE = './webcapturetesting.txt'
    e = WebDriverException("e=dnsNotFound")
    url = "test.com"
    result = process_std_exceptions(LOG_FILE, e, url)
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    else:
        assert False
    assert 'dnsNotFound' == result

def test_process_default_args_redirect(): # test redirect loop processing
    LOG_FILE = './webcapturetesting.txt'
    e = WebDriverException("e=redirectLoop")
    url = "test.com"
    result = process_std_exceptions(LOG_FILE, e, url)
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    else:
        assert False
    assert 'redirect' == result

def test_process_default_args_misc(): # test non categorised processing
    LOG_FILE = './webcapturetesting.txt'
    e = WebDriverException("")
    url = "test.com"
    result = process_std_exceptions(LOG_FILE, e, url)
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    else:
        assert False
    assert 'misc' == result