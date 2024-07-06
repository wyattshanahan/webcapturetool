from driver import print_report

# THIS DOCUMENT CONTAINS AUTOMATED UNIT TESTS. IT IS NOT REQUIRED FOR THE EXECUTION OF THE WEBCAPTURETOOL.


def test_print_report(capsys):
    print_report(5, 5, 0, 1, False)
    captured = capsys.readouterr()
    print("out")
    print(captured.out)
    assert captured.out == '\n*====================*\n Final Report        \n\n Total Processed: 11  \n Total Successful: 10 \n Total Failures: 1   \n*====================*\n'
