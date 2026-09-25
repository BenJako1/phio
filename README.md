# phio

A Python package for laser-induced photoionization simulations.

## Installation

phio requires Python 3.9 or newer. The recommended installation method is to create a virtual environment and install the project in editable mode. {"fallbackMarkdown":"(GitHub
)","reference":{"matched_text":"","prefix":null,"start_idx":573,"end_idx":590,"safe_urls":["https://raw.githubusercontent.com/BenJako1/phio/main/pyproject.toml"],"refs":[],"alt":"(GitHub
)","prompt_text":null,"type":"grouped_webpages","style":null,"fallback_items":null,"error":null,"status":"done","items":[{"title":"","url":"https://raw.githubusercontent.com/BenJako1/phio/main/pyproject.toml","attribution":"GitHub","pub_date":null,"snippet":null,"attribution_segments":null,"supporting_websites":[],"refs":[{"turn_index":1,"ref_type":"view","ref_index":0}],"hue":null,"attributions":null}]},"showLoginRequiredCard":false}

### macOS
1. Install Python

If Python 3.9 or newer is not already installed, install it from python.org
 or using Homebrew.

Check your Python version:

python3 --version


You should see Python 3.9 or newer.

2. Clone the repository
git clone https://github.com/BenJako1/phio.git
cd phio

3. Create a virtual environment
python3 -m venv .venv


Activate it:

source .venv/bin/activate


After activation, your terminal should show (.venv) at the beginning of the prompt.

4. Upgrade pip
python -m pip install --upgrade pip

5. Install phio in editable mode
python -m pip install -e .


The -e option installs the project in editable mode, meaning changes to the source code are immediately available without reinstalling the package.

### Windows
1. Install Python

Install Python 3.9 or newer from python.org
.

During installation, make sure to enable:

Add Python to PATH

Check that Python is available:

py --version


You should see Python 3.9 or newer.

2. Install Git

If Git is not already installed, download and install it from git-scm.com
.

Check that it is available:

git --version

3. Clone the repository

Open PowerShell or Command Prompt and run:

git clone https://github.com/BenJako1/phio.git
cd phio

4. Create a virtual environment

In PowerShell:

py -m venv .venv


Activate it:

.\.venv\Scripts\Activate.ps1


If you are using Command Prompt instead:

.venv\Scripts\activate


After activation, your terminal should show (.venv) at the beginning of the prompt.

5. Upgrade pip
python -m pip install --upgrade pip

6. Install phio in editable mode
python -m pip install -e .


The -e option installs the project in editable mode, so changes to the source code are immediately available without reinstalling the package.

Verify the installation

Once the installation has completed, you can verify that Python can import the package:

python -c "import phio; print('phio installed successfully')"


If this prints:

phio installed successfully


the installation was successful.

Development workflow

If you are working on the source code, keep the virtual environment activated while developing:

macOS
source .venv/bin/activate

Windows PowerShell
.\.venv\Scripts\Activate.ps1


Because phio is installed in editable mode, you can modify files under src/ and immediately use the changes without running pip install again.

Updating the project

To get the latest changes from GitHub:

git pull


There is normally no need to reinstall the package after pulling changes when it is installed in editable mode.

Deactivating the virtual environment

When you are finished working:

deactivate

Troubleshooting
python is not recognized on Windows

Try using the Python launcher instead:

py --version


If py is also unavailable, reinstall Python and make sure Python is added to your PATH.

PowerShell does not allow activation

If PowerShell reports that script execution is disabled, you can either use Command Prompt or allow locally created scripts for your user account:

Set-ExecutionPolicy -Scope CurrentUser RemoteSigned


Then activate the environment again:

.\.venv\Scripts\Activate.ps1

pip install -e . fails

Make sure you are running the command from the root of the repository—the directory containing pyproject.toml:

phio/
├── pyproject.toml
├── src/
└── ...


Then run:

python -m pip install -e .

Repository

Source code and development history are available on GitHub:

https://github.com/BenJako1/phio

License

phio is released under the MIT License.
