# swot-backend
Backend API for Swot

## Used technology

All Python dependencies can be found in requirements.txt.

Notably:
- Flask - the webserver handling routing
- Gunicorn - the tool used to manage workers allowing the application to harness concurrent requests
- SQLAlchemy - The tool used to manage database models and write programmatic queries to the database
- Alembic - A tool which works in unison with SQLAlchemy to migrate the database to add new changes to models

On the backend:
- SaltStack - Used to bootstrap the host and handle auto-deployment of the softare
- Docker - used to containerise the application allowing for simple deployment
- NGINX - A web server being used as a reverse proxy to forward requests to the Docker container running NGINX. (Note: NGINX is containerised, but port 80 is being exposed)

## Installation

Swot runs on Python 3.8, the latest version of Python, though in theory should run on earlier versions as well since no 3.8 specific features are used.

### Environment setup

Most dependency management must be done using the command line.

#### Python
Confirm a working Python installation by running the following in a command prompt windoww.

Windows:
```batch
py -3 -V
```

MacOS/UNIX (varies depending on setup):
```bash
python3 -V
```

#### PIP
Confirm a working pip installation by running the following.

Windows:
```batch
py -3 -m pip -V
```

A breakdown of this command:
- `py` call Python
- `-3` select Python 3
- `-m` call a Python module
- `pip` run PIP
- `-V` ask pip for the version

MacOS/UNIX:
```bash
python3 -m pip -V
```

If both of these commands return successfully then you can continue to the next stage.

If one of these commands fails to install then the installation is not ready.

See the following documents:
- [Python](https://www.python.org/downloads/release/python-382/)
- [PIP](https://packaging.python.org/tutorials/installing-packages/#ensure-you-can-run-pip-from-the-command-line)

### Installing dependencies

Open a terminal and navigate to the code directory.

Next run the following command:

Windows:
```batch
py -3 -m pip install -r requirements.txt
```

MacOS/UNIX:
```bash
python3 -m pip install -r requirements.txt
```

A breakdown of this command:
- `pip` run the package manager
- `install` switch to installing packages
- `-r requirements.txt` install packages listed in requirements.txt

If no errors are encountered then you should be good to progress to the next stage.

### Configuration

Swot backend is configured through the use of a YAML file.

Swot attempts to look for a file named `config.yaml` so you must copy `config-default.yaml`, make any necessary modifications and save it as `config.yaml`.

### Running Swot

Running swot is the easiest part of the process.

Windows:
```batch
py -3 app.py
```

MacOS/UNIX:
```bash
python3 app.py
```

If configured correctly you should see a message about Swot starting up as a webserver.

It should then be accessible using whatever configuration options you selected.

## Configuration options

A breakdown of all the available config options is as follows:

- `host` - the block for configuration of the webserver
    - `host` - what IP to listen on
    - `port` - what port to listen on (note on UNIX ports < 1024 require superuser permissions)
    - `debug` - Whether to run the webserver in debug mode, recommended for local execution
    - `migrate_on_startup` - Should database migration occur automatically on startup (recommended for users not planning to develop)
- `recaptcha` - the block for configuration of Recaptcha anti-spam
    - `key` - The private site key for recaptcha, set to a jargon string if you do not have one.
- `flask` - configuration of flask
    - `SECRET_KEY` - The random string used for signing session cookies in the app
- `db` - configuration of the database
    - `use_sqlite` - Ignore all other options and use a SQLite database, recommended for local setups.
    - `host` - IP address of the database
    - `port` - port the database is running on
    - `username` - username for the database
    - `password` - password for the database
    - `database` - which postgresql database to use