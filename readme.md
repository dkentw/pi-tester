

# Installation
```bash
python setup.py install
```

# Usage
```bash
$ pitester -h

# run a testsuite with a csv file
$ pitester -s testsuite.csv

# run a specific test case
$ pitester -c Dummy_0101
```

# Create A Test Case

### 1. Create a directory for test cases
The name(Dummy) of the directory must the same as the name of test script(Dummy.py)

```bash
$ mkdir Dummy
$ cd Dummy
$ touch Dummy.py
```

### 2. Writ down the test script in the py file.
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