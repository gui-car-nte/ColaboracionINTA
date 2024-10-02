# ColaboracionINTA

Program capable of calculating magnetic moment based on data extracted from sensor readings and user-input distances.

## SETUP:

To use the program run the following commands on your terminal of choice.

### 1. Create a virtual environment:

Linux:

```bash
python3 -m venv mi_entorno
```

Windows:

```cmd
python -m venv mi_entorno
```

### 2. Activate the virtual environment:

Linux:

```bash
source mi_entorno/bin/activate
```

Windows:

```cmd
mi_entorno\Scripts\activate.bat
```

### 3. Install the program's required modules:

```python
pip install -r requirements.txt
```

### 4. Create executable file:

```python
pip install pyinstaller

pyinstaller main.py --onefile --noconsole --add-data "src/front/resource/*;resource/" --name='Magnetic Moment Calculation' --icon=src\front\resource\inta_icon.ico
```
