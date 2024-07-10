# ColaboracionINTA

<!-- poner en ingles -->

## Start virtual environment

To create a virtual environment we must execute the following command in the terminal

Linux:

```bash
python3 -m venv mi_entorno
```

Windows:

```cmd
python -m venv mi_entorno
```

## Activate virtual environment  
To activate the virtual environment you must enter the following in the terminal

Linux:

```bash
source mi_entorno/bin/activate
```

Windows:

```cmd
mi_entorno\Scripts\activate.bat
```

## Start program

In order to start the program we must first install the dependencies, to do this we must execute the following command

```python
pip install -r requirements.txt
```

To start the program you must enter the following in the terminal

Linux:

```bash
python3 main.py
```

Windows:
```cmd
python main.py
```

## Create executable file

To create executable file you must enter the following in the terminal

```python
pip install pyinstaller

pyinstaller main.py --onefile --name=your_app_name --icon=youricon.ico
pyinstaller your_app_name.spec
```
