# phio

A Python package for laser-induced photoionization simulations.

## Installation

`phio` requires Python 3.9 or newer. The recommended installation method is to create a virtual environment and install the project in editable mode.

### macOS

#### 1. Install Python

If Python 3.9 or newer is not already installed, install it from [python.org](https://www.python.org/) or using Homebrew.

Check your Python version:

```bash
python3 --version
```

You should see Python 3.9 or newer.

#### 2. Clone the Repository

```bash
git clone https://github.com/BenJako1/phio.git
cd phio
```

#### 3. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

After activation, your terminal should show `(.venv)` at the beginning of the prompt.

#### 4. Upgrade pip

```bash
python -m pip install --upgrade pip
```

#### 5. Install phio in Editable Mode

```bash
python -m pip install -e .
```

The `-e` option installs the project in editable mode, meaning changes to the source code are immediately available without reinstalling the package.

### Windows

#### 1. Install Python

Install Python 3.9 or newer from [python.org](https://www.python.org/).

During installation, make sure to enable:

**Add Python to PATH**

Check that Python is available:

```powershell
py --version
```

You should see Python 3.9 or newer.

#### 2. Install Git

If Git is not already installed, download and install it from [git-scm.com](https://git-scm.com/).

Check that it is available:

```powershell
git --version
```

#### 3. Clone the Repository

Open PowerShell or Command Prompt and run:

```powershell
git clone https://github.com/BenJako1/phio.git
cd phio
```

#### 4. Create a Virtual Environment

In PowerShell:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If you are using Command Prompt instead:

```cmd
.venv\Scripts\activate
```

After activation, your terminal should show `(.venv)` at the beginning of the prompt.

#### 5. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

#### 6. Install phio in Editable Mode

```powershell
python -m pip install -e .
```

The `-e` option installs the project in editable mode, so changes to the source code are immediately available without reinstalling the package.

## Verify the Installation

Once the installation has completed, you can verify that Python can import the package:

```bash
python -c "import phio; print('phio installed successfully')"
```

If this prints:

```text
phio installed successfully
```

the installation was successful.

## Development Workflow

If you are working on the source code, keep the virtual environment activated while developing.

### macOS

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

Because `phio` is installed in editable mode, you can modify files under `src/` and immediately use the changes without running `pip install` again.

## Updating the Project

To get the latest changes from GitHub:

```bash
git pull
```

There is normally no need to reinstall the package after pulling changes when it is installed in editable mode.

## Deactivating the Virtual Environment

When you are finished working:

```bash
deactivate
```

## Troubleshooting

### `python` Is Not Recognized on Windows

Try using the Python launcher instead:

```powershell
py --version
```

If `py` is also unavailable, reinstall Python and make sure Python is added to your `PATH`.

### PowerShell Does Not Allow Activation

If PowerShell reports that script execution is disabled, you can either use Command Prompt or allow locally created scripts for your user account:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### `pip install -e .` Fails

Make sure you are running the command from the root of the repository—the directory containing `pyproject.toml`:

```text
phio/
├── pyproject.toml
├── src/
└── ...
```

Then run:

```bash
python -m pip install -e .
```

## Repository

Source code and development history are available on GitHub:

https://github.com/BenJako1/phio

## License

`phio` is released under the MIT License.

## Disclosure on the use of generative AI

Generative AI was used to some degree in certain parts of `phio` development, the LLM used primarily for this was `GPT-5.6 Luna`. While some methods were suggested or checked by AI, all code in `phio` was understood by a human before being used in the code base.
