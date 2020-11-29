# Convert modularized code into a Python package

Put code into a folder, e.g. "python_package" in the workspace. Inside the folder, you need to create a few folders and files:

* a `setup.py` file, which is required in order to use pip install
* a folder called 'distributions', which is the name of the Python package
    * inside the 'distributions' folder, you need the `Gaussiandistribution.py` file, `Generaldistribution.py`
    * an `__init__.py` file
    * `license.txt`
    * `setup.cfg`
    * a `README.md` file

Set up a virtual environment first. A virtual environment is a siloed Python installation apart from your main Python installation. That way you can easily delete the virtual environment without affecting your Python installation.

Open a new terminal window in the workspace by clicking 'NEW TERMINAL' and type:

* this command to create a virtual environment `python3 -m venv venv_name` where `venv_name` is the name you want to give to your virtual environment. You'll see a new folder appear with the Python installation named `venv_name`.
* In the terminal, type `source venv_name/bin/activate`. You'll notice that the command line now shows (`venv_name`) at the beginning of the line to indicate you are using the venv_name virtual environment.
* Now, you can type `pip install python_package/.` That should install your distributions Python package.
* Try using the package in a program to see if everything works!

Start the python interpreter from the terminal typing:

* `python3`

Then within the Python interpreter, you can use the distributions package:

* `from distributions import Gaussian`
* `gaussian_one = Gaussian(25, 2)`
* `gaussian_one.mean`
* `gaussian_one + gaussian_one`

etcetera... In other words, you can import and use the Gaussian class because the distributions package is now officially installed as part of your Python installation.

## Upgrade

Note that if you change the code in the distributions folder after pip installing the package, Python will not know about the changes. You'll need to run `pip install [package_name] --upgrade` when you make changes to the package files.

## Unit Tests

When you're ready to test out the code, in the terminal:

* Run the unit tests by typing `python3 -m unittest test`.

## Upload to PyPi

The Python package is located in the folder python_package

You need to create a `setup.cfg` file, `README.md` file, and `license.txt` file (e.g. MIT licence). You also need to create accounts for the pypi test repository and pypi repository.

Once you have all the files set up correctly, you can use the following commands on the command line (note that you need to make the name of the package unique, so change the name of the package from distributions to something else. That means changing the information in `setup.py` and the folder name:

* `cd python_package`
* `python3 setup.py sdist bdist_wheel`
* `pip install twine`

### Commands to upload to the PyPi test repository

* `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
* `pip install --index-url https://test.pypi.org/simple/ distributions`

### Command to upload to the PyPi repository

* `twine upload dist/*`
* `pip install distributions`
