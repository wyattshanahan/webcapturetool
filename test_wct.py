from driver import print_report, build_dir_name, process_default_args
import datetime
import pytest

# THIS DOCUMENT CONTAINS AUTOMATED UNIT TESTS. IT IS NOT REQUIRED FOR THE EXECUTION OF THE WEBCAPTURETOOL.


# test that the report is being printed and calculating correctly
def test_print_report(capsys):
    print_report(5, 5, 0, 1, False)
    captured = capsys.readouterr()
    print("out")
    print(captured.out)
    assert captured.out == '\n*====================*\n Final Report        \n\n Total Processed: 11  \n Total Successful: 10 \n Total Failures: 1   \n*====================*\n'


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