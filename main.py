import platform
import csv
import os
import re
import subprocess
import cpuinfo

system_info = cpuinfo.get_cpu_info()
cpu_name = system_info['brand_raw']


def get_cpu_info():
    match = re.search(r"(i\d)-(\d{4,5})", cpu_name)
    if match:
        cpu_series = match.group(1)
        cpu_model_number = match.group(2)
        return f"Core {cpu_series}-{cpu_model_number}"
    else:
        return cpu_name  # Falls das Muster nicht gefunden wird, gib den ganzen Namen zurück


cpu_model = get_cpu_info()


def Code_Name():
    with open('intel-processor/intel_core_processors_v1_8.csv', "r") as file:
        csv_file = csv.reader(file, delimiter=",")
        for row in csv_file:
            if cpu_model == row[0]:
                return row[3]
    return "Code Name not found"


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
    global manufacturer, product
    try:
        output = subprocess.check_output(['lshw', '-C', 'display'], universal_newlines=True)

        lines = output.strip().split('\n')
        product, manufacturer = None, None

        for line in lines:
            if 'product' in line:
                product = line.split(': ')[1].strip()
            elif 'vendor' in line:
                manufacturer = line.split(': ')[1].strip()

        if product and manufacturer:
            print(f"Chipset Model: {product}")
            print(f"Manufacturer: {manufacturer}")
        else:
            print("Required information not found.")
        return product, manufacturer

    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None, None


def get_gpu_info_macos():
    try:
        command = ['/usr/sbin/system_profiler', 'SPDisplaysDataType']
        output = subprocess.check_output(command, universal_newlines=True)
        lines = output.strip().split('\n')
        chipset_model, manufaturer = None, None

        for line in lines:
            if 'Chipset Model' in line:
                chipset_model = line.split(': ')[1].strip()
            elif 'Vendor' in line:
                manufacturer = line.split(': ')[1].strip()

        if chipset_model and manufacturer:
            print(f"Chipset Model: {chipset_model}")
            print(f"Manufacturer: {manufacturer}")
        else:
            print("Required information not found.")
        return chipset_model, manufacturer

    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None, None


platform_name = platform.system()

if platform_name == "Windows":
    get_gpu_info_windows()
elif platform_name == "Linux":
    get_gpu_info_linux()
elif platform_name == "Darwin":
    get_gpu_info_macos()
else:
    print("Your System Could Not be Identified")


def questioncpu():
    global cpu_model, cpu_name
    question = input(f"Is the {cpu_model} your CPU [y/n]: ")

    if question.lower() == "y":
        if cpu_model == system_info['brand_raw']:
            print("yay")
        else:
            Code_Name()
            print(f"CPU Model: {cpu_model}")  # Ausgabe des ermittelten CPU-Modells
            print(f"Code Name: {Code_Name()}")
    elif question.lower() == "n":
        cpu_name = input("Please enter your CPU (e.g. i5-12400): ")
        cpu_model = get_cpu_info()
        questioncpu()
    else:
        print("Please enter y/n")
        questioncpu()


questioncpu()
