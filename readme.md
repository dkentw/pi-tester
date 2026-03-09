
# pi-tester

A lightweight Python automation test framework. Test cases are defined as Python classes, organized via CSV test suite files. Results are reported to the console, HTML, CSV, and JUnit XML.

Requires Python 3.6+.

# Installation

```bash
pip install uv
uv sync
```

# Usage

```bash
# show help
pitester -h

# run a test suite from a csv file
pitester -s testsuite.csv

# run a specific test case (supports regex)
pitester -c Dummy_0101

# run all test cases found in the working directory
pitester -a

# run multiple csv files in order from a list file
pitester -l csv_list.txt

# generate test script templates from a csv file
pitester -g testsuite.csv

# output JUnit XML report
pitester -s testsuite.csv -x results.xml

# pass runtime variables into test cases
pitester -s testsuite.csv -v var1:AAA,var2:192.168.1.1

# enable debug logging
pitester -d debug -s testsuite.csv
```

# Create a Test Suite

Test suites are CSV files. The first row is a fixed header. `TestCase ID` and `Run` are required columns.

```text
Prefix,TestCase ID,Title,Type,Run,Result,Log,Duration Time
,Dummy_0101,,,0,,,
,Dummy_0102,,,1,,,
,Dummy_0103,,,1,,,
```

**Run values:**
- `1` — execute the case
- `0` — skip the case
- _(empty)_ — skip the case

## TestCase ID naming convention

Format: `<TestSuiteName>_<Number>`

- **TestSuiteName** must match the directory name and the `.py` script name
- **Number** is arbitrary
- The full ID is also the **class name** inside the script

# Create Test Cases

### 1. Create a directory matching the suite name

```bash
mkdir Dummy
cd Dummy
touch Dummy.py
```

### 2. Write test classes in the `.py` file

- Class name must match the `TestCase ID` in the CSV
- Must implement a `run()` method
- `run()` returns `(bool, str)`: `True` = Pass, `False` = Fail, plus a log message

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

### 3. Using runtime variables

Variables passed with `-v` are injected as instance attributes before `run()` is called:

```bash
pitester -s Dummy.csv -v var1:hello,var2:192.168.0.1
```

```python
class Dummy_0103:
    def __init__(self):
        self.var1 = 'default'  # overridden at runtime by -v var1:hello

    def run(self):
        return True, self.var1
```

# Reports

After each run, reports are written to `Reports/Latest/`:

- `<SuiteName>.html` — per-suite detail report
- `SummaryReport.html` — overall summary across all suites
- `<SuiteName>.xml` — JUnit XML (always written; use `-x` to specify a custom filename)
- `<SuiteName>.csv` — copy of the input CSV with results filled in

# Agent Mode (Remote Execution)

`agent.py` is an XML-RPC server that allows pi-tester to execute commands on a remote machine.

**On the remote machine:**

```bash
python agent.py -s 0.0.0.0 -p 8000
```

**Registered RPC functions:**

| Function | Description |
|---|---|
| `exec_command_async` | Launch a process and return immediately |
| `exec_command_sync` | Launch a process and return its output |
| `receive_file` | Write a file to a path on the remote host |
| `ping` | Returns `'pong'` — use to check connectivity |
