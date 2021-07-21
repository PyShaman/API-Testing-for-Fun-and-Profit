# API Testing for Fun and Profit
_User guide_


**List of contents**

**1. Python version and installation**

**2. Installing required packages and tools**

**3. Usage**

**4. Output**

**5. Generating Allure Reports**

**6. Reproduce swagger.yml file**



_1. Python version and installation_

Tests are written in Python 3.8+ and it should be ran on this version or higher.
User can download newest version of Python at [Python download site](https://www.python.org/downloads/).

Install [PIP](https://pypi.org/project/pip/).

_2. Installing required packages and tools_

After cloning [API Testing for Fun and Profit](https://github.com/PyShaman/migo_money.git) repository locally user should enter
migo_money folder and create separate virtual environment for this project by using following command:
```
$ python -m venv venv
```
Python will create new directory called venv and install there basic packages. Next step is to activate virtual environment:
```
PS > ./venv/Scripts/Activate.ps1
```
for Windows systems or
```
$ ./venv/Scripts/activate
```
for Linux.
When virtual environment will be activated the user will see additional mark at console:
```
(venv) path\migo_money >
```
Next step is to install required packages using following command:
```
PS > pip install -r requirements.txt
```
for Windows systems or
```
$ pip3 install -r requirements.txt
```
for Linux.

This will automatically download and install all necessary packages.

_3. Usage:_

To run all tests use following command:
```
$ pytest -v
```

_4. Output:_

The tests will perform API tests for https://qa-interview-api.migo.money endpoints.

_5. Generating Allure Reports_

To generate Allure Reports please follow [installation guide](https://docs.qameta.io/allure/#_installing_a_commandline).

To initiate Allure Listener use following command:
```
$ pytest --alluredir=/tmp/my_allure_results
```
To see actual report use following command:
```
$ allure serve /tmp/my_allure_results
```

_6. Reproduce swagger.yml file_

To reproduce swagger.yml file copy and paste content of file in the following [Swagger Editor](https://editor.swagger.io/)
