# Audio Cryptography Project Instructions

## Project Stack

| Name           | Version  |
|:--------------:|:--------:|
| Python         | 3.12.4   |
| typer          | 0.12.3   |
| wave           | 0.0.2    |


## Development Environment Configuration

### Clone Project

The first thing to do is to clone the repository

### Python Env Setup

Create a virtual environment to install dependencies inside it and activate it.

**IMPORTANT**: It is suggested to use `poetry` package and environment manager when using this application which is explained further down.

#### Virtualenv package

Install Virtualenv package

```sh
pip install virtualenv --upgrade
```

Create a virtual environment

```sh
virtualenv .env
```

Activate virtual environment in linux

```sh
source .venv/bin/activate
```

Activate virtual environment in windows

```sh
.\.env\Scripts\activate.bat
```

To save all dependencies version always after installation use bellow command.

```sh
pip freeze > requirements.txt
```

To install all current dependencies on your environment:

```sh
pip install -r requirements.txt
```

---

#### pipenv package

Install pipenv package

```sh
pip install pipenv --upgrade
```

activate virtual environment

```sh
pipenv shell
```

To install a package you can use bellow command. One of feature of this virtual environment is to lock the dependencies automatically.

**NOTICE:** It maybe slow on your local machine.

To install all current dependencies on your environment:

```sh
pipenv install
```

#### [Poetry](https://python-poetry.org/docs/cli/#new)

__Install Poetry on Linux__

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

__Install Poetry on Windows__

**TIP**: do bellow command on Powershell Administrator

```ps
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

__Config__
```sh
# Creates the address of the .env folder in the program directory, It is null by default
poetry config virtualenvs.in-project true
# The address of the .env folder
poetry config virtualenvs.path .
```

__Add__
```sh
# Installing a package in the desired group
poetry add --group GROUP_NAME PACKAGE_NAME
```

1) To initialize project and poetry package manager in your project when it does NOT exists. (for developers)

```sh
poetry init
```

2) To install all packages with poetry that is documented in `poetry.lock` do bellow command:

```sh
poetry install
```

3) To install a package in poetry:

```sh
poetry add typer
```

4) To install a package in poetry in **`dev group`**:

```sh
poetry add typer --group=dev
```

5) To activate poetry environment:

```sh
poetry shell
```

or step 3 on pip instruction

#### Run Project

You can check for help for encryption as demonstrated below:

```sh
python main.py encrypt --help
```

You can check for help for decryption as demonstrated below:

```sh
python main.py decrypt --help
```

You can encrypt as shown below (file_path can be both relative and absolute):

**IMPORTANT**: before using the application, you have to set a secret key generated by fernet inside the settings as demonstrated below:

first generate the key using fernet inside python interactive shell,

```sh
python
```

```python
>>> from cryptography.fernet import Fernet
>>> Fernet.generate_key()
```

copy the generated key without the `b''` around it and place it in the settings.py as demonstrated,

`src/configs/settings.toml`

replace your secret key with the one below:

```toml
[settings.encryption]
fkey = "ILRYCAcHIlzzhQTNW6UOxUBBHfDznb2lUJfu3Lj1gJo="
```

**IMPORTANT**: You can use the fast flag to encrypt/decrypt faster in the cost security, you can only decrypt a file with also `--fast` switch if you encrypt the file with it.

You can decrypt as shown below (file_path can be both relative and absolute):

```sh
python main.py decrypt -i file_path -o file_path -k key_string
python main.py decrypt --in file_path --out file_path --key key_string
```

Please look at the examples below:

```sh
python main.py encrypt --in test_PamelaGoing.wav --out ./test_encrypted.wav
python main.py decrypt --in ./test_encrypted.wav --out ./test_decrypted.wav --key gAAAAABmiTwPzV06GoXucoybSIECvmYLnMlJhr6wnBBJaiFDs0_yCdXjFUBdz9W0GpBllrUyN4ct574q_iZ3kIsohHNTSxtU-g==
```

or with fast,

```sh
python main.py encrypt --fast --in test_PamelaGoing.wav --out ./test_encrypted.wav
main.py decrypt --fast --in ./test_encrypted.wav --out ./test_decrypted.wav --key gAAAAABmiTwPzV06GoXucoybSIECvmYLnMlJhr6wnBBJaiFDs0_yCdXjFUBdz9W0GpBllrUyN4ct574q_iZ3kIsohHNTSxtU-g==
```

or short form,

```sh
python main.py encrypt -f -i test_PamelaGoing.wav -i ./test_encrypted.wav
main.py decrypt -f -i ./test_encrypted.wav -o ./test_decrypted.wav -k
gAAAAABmiTwPzV06GoXucoybSIECvmYLnMlJhr6wnBBJaiFDs0_yCdXjFUBdz9W0GpBllrUyN4ct574q_iZ3kIsohHNTSxtU-g==
```

for plotting, testing and generating binary files for NIST refer to `--help`

```sh
python test --help
python plot --help
python nist --help
```

for plotting, testing and generating binary files for NIST refer to `--help`

```sh
python test --help
python plot --help
python nist --help
```


Thanks for reading.
