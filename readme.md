

# Installation
```bash
$ pip install pitester
```

```bash
$ python setup.py install
```

# Usage
```bash
$ pitester -h

# run a testsuite with a csv file
$ pitester -s testsuite.csv

# run a specific test case
$ pitester -c Dummy_0101
```

# Create a Test Suite
Test suite written with csv format. The column name of the first row is fixed, please refer the sample as below. ```TestCase ID``` and ```Run``` are required.

```text
Prefix,TestCase ID,Title,Type,Run,Result,Log,Duration Time
,Dummy_0101,,,0,,,
,Dummy_0102,,,1,,,
,Dummy_0103,,,1,,,
,Dummy_0104,,,1,,,
,Dummy_0105,,,1,,,
,Dummy_0106,,,1,,,
,Dummy_0107,,,1,,,
,Dummy_0108,,,1,,,
,Dummy_0109,,,,,,
,Dummy_0110,,,,,,
```

## Naming convention of TestCase ID
The naming of the TestCase ID follows this rule: ```<TestSuiteName>_<ID Number>```. Actually TestCase ID is like index, pi-tester will try to find the test script from the name then execute the case.

* The **TestSuiteName** is the same as the name of test script.
* ID Number is arbitrary.
* The TestCase ID is a **class name** in the test script.

## Run
* 1: excute it.
* 0: not excute it.

# Create Test Cases

### 1. Create a directory for test cases
The name(Dummy) of the directory must the same as the name of test script(Dummy.py)

```bash
$ mkdir Dummy
$ cd Dummy
$ touch Dummy.py
```

### 2. Write down the test script in the .py file.

* The class name is same as ```TestCase ID```
* The method ```run``` must be implemented.
* Return value of ```run```
    * first value:  ```True``` means Pass, ```Flase``` means Fail
    * second value: log meesage.

```python
class Dummy_0101:
    '''
    write doc here
    '''
    def __init__(self):
        pass

    def run(self):
        return True, 'call dummy api success'
```
