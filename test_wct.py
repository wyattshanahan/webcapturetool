from driver import print_report, build_dir_name
import datetime

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
