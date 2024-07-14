import platform
import csv
import os
import re
import subprocess
import cpuinfo


def get_cpu_info():
    system_info = cpuinfo.get_cpu_info()
    cpu_name = system_info['brand_raw']

    match = re.search(r"(i\d)-(\d{4})", cpu_name)
    if match:
        cpu_series = match.group(1)
        cpu_model_number = match.group(2)
        return f"{cpu_series}-{cpu_model_number}"
    else:
        return cpu_name  # Falls das Muster nicht gefunden wird, gib den ganzen Namen zurück


cpu_model = "Core " + get_cpu_info()


def Code_Name():
    csv_file = csv.reader(open('intel-processor/intel_core_processors_v1_8.csv', "r"), delimiter=",")

    for row in csv_file:
        #if current rows 2nd value is equal to input, print that row
        if cpu_model == row[0]:
            return row[3]


print(f"CPU Model: {cpu_model}")  # Ausgabe des ermittelten CPU-Modells
print(f"Code Name: {Code_Name()}")


def get_gpu_info_windows():
    try:
        # Befehl für wmic, um die Informationen über die Grafikkarte zu erhalten
        command = 'wmic path win32_videocontroller get caption'

        # Ausführen des Befehls und Erfassen der Ausgabe
        output = subprocess.check_output(command, shell=True, universal_newlines=True)

        # Aufsplitten der Ausgabe in Zeilen und Extrahieren der Produktinformationen
        lines = output.strip().split('\n')

        gpu_info = []

        for line in lines[1:]:
            info = line.strip()
            if info:
                # Überprüfe, ob der Hersteller in der Zeile enthalten ist (NVIDIA, AMD, Intel)
                if 'NVIDIA' in info:
                    manufacturer = 'NVIDIA'
                    product_name = info.replace('NVIDIA', '').strip()
                    gpu_info.append((product_name, manufacturer))
                elif 'AMD' in info:
                    manufacturer = 'AMD'
                    product_name = info.replace('AMD', '').strip()
                    gpu_info.append((product_name, manufacturer))
                elif 'Intel' in info:
                    manufacturer = 'Intel'
                    csv_file = csv.reader(open('intel-processor/intel_core_processors_v1_8.csv', "r"), delimiter=",")

                    product_name = info.replace('Intel', '').strip()
                    gpu_info.append((product_name, manufacturer))

        # Wenn eine oder mehrere Grafikkarten gefunden wurden, gib sie aus
        if gpu_info:
            for product_name, manufacturer in gpu_info:
                print(f"GPU: {manufacturer} {product_name}")
        else:
            print("No NVIDIA, AMD, or Intel GPU found.")

    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)


def get_gpu_info_linux():
    try:
        lshw_output = subprocess.check_output(['lshw', '-C', 'display'], universal_newlines=True)

        product_info = [line.strip() for line in lshw_output.splitlines() if 'vendor:' in line.lower()]

        print("\nGPU manufacture: ")
        if product_info:
            for info in product_info:
                print(info)
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)


def get_gpu_info_macos():
    command = ['/usr/sbin/system_profiler', 'SPDisplaysDataType']
    output = subprocess.check_output(command).decode('utf-8')
    print(output)


platform = platform.system()

if platform == "Windows":
    get_gpu_info_windows()
elif platform == "Linux":
    get_gpu_info_linux()
elif platform == "MacOS":
    get_gpu_info_macos()
else:
    print("Your System Could Not be Identified")
