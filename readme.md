


# Create A Test Case

### 1. create a test suite in TestSuites/ folder

```bash
$ cd TestSuites
$ touch Dummy.csv
```

### 2. Refer the sample file in TestSuites/ folder to create the coloumn and data.

### 3. Create a folder for test cases in TestCases/

```bash
$ mkdir Dummy
$ cd Dummy
$ touch Dummy.py
```

### 4. Writ down the test script in the py file.


# Run Test Case

```bash
# Execute a test case by test case ID
python pi_tester.py -c Dummy_0102$

# Execute test cases by test suit
python pi_tester.py -s TestSuites/Dummy.csv
```
