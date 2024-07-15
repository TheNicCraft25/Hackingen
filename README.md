# Hackingen

Ein Python-Skript zur Erkennung und Ausgabe von CPU- und GPU-Informationen, einschließlich des Codenamens der CPU und der GPU-Daten für verschiedene Betriebssysteme.

## Übersicht

Dieses Skript ermittelt die CPU-Informationen anhand des CPU-Namens und sucht nach dem zugehörigen Codenamen in einer CSV-Datei. Es kann auch GPU-Informationen für Windows, Linux und macOS abrufen und bietet eine interaktive Möglichkeit, die erkannten oder manuell eingegebenen Informationen zu bestätigen.

## Anforderungen

- Python 3.x
- Abhängigkeiten: `cpuinfo`

## Installation

1. Klone das Repository:
   ```bash
   git clone https://github.com/TheNicCraft25/Hackingen.git
   cd Hackingen
   ```

2. Installiere die Abhängigkeiten:
   ```bash
   pip install py-cpuinfo
   ```

3. Stelle sicher, dass die Datei `intel_core_processors_v1_8.csv` im Verzeichnis `intel-processor` vorhanden ist.

## Verwendung

Führe das Skript aus:
```bash
python script.py
```

Das Skript wird die CPU- und GPU-Informationen ermitteln und interaktive Eingabeaufforderungen anzeigen, um die erkannten Informationen zu bestätigen oder manuell einzugeben.

## Code-Erklärung

### CPU-Informationen abrufen

Der folgende Codeabschnitt ermittelt die CPU-Informationen:
```python
import cpuinfo
import re

system_info = cpuinfo.get_cpu_info()
cpu_name = system_info['brand_raw']

def get_cpu_info():
    match = re.search(r"(i\d)-(\d{4,5})", cpu_name)
    if match:
        cpu_series = match.group(1)
        cpu_model_number = match.group(2)
        return f"Core {cpu_series}-{cpu_model_number}"
    else:
        return cpu_name

cpu_model = get_cpu_info()
```

### CPU-Codename abrufen

Der Codename der CPU wird aus einer CSV-Datei abgerufen:
```python
import csv

def code_name():
    with open('intel-processor/intel_core_processors_v1_8.csv', "r") as file:
        csv_file = csv.reader(file, delimiter=",")
        for row in csv_file:
            if cpu_model == row[0]:
                return row[3]
    return "Code Name not found"

print(f"CPU Model: {cpu_model}")
print(f"Code Name: {code_name()}")
```

### GPU-Informationen abrufen

Je nach Betriebssystem werden verschiedene Methoden verwendet, um die GPU-Informationen abzurufen:

#### Windows
```python
import subprocess

def get_gpu_info_windows():
    # Windows-spezifischer Code
```

#### Linux
```python
def get_gpu_info_linux():
    # Linux-spezifischer Code
```

#### macOS
```python
def get_gpu_info_macos():
    # macOS-spezifischer Code
```

### Interaktive Eingabeaufforderungen

Das Skript bietet interaktive Eingabeaufforderungen, um die ermittelten Informationen zu bestätigen oder manuell einzugeben:
```python
def questioncpu():
    # CPU-Eingabeaufforderung

def questiongpu():
    # GPU-Eingabeaufforderung
```

## Autor

[TheNicCraft25](https://github.com/TheNicCraft25)

## Lizenz

Dieses Projekt ist lizenziert unter der MIT-Lizenz.
