import socket
import concurrent.futures
import importlib
import subprocess
import sys
import urllib.parse

def ensure_import(module_name):
    try:
        importlib.import_module(module_name)
        print(f"Модуль {module_name} успешно импортирован.")
    except ImportError:
        print(f"Модуль {module_name} не найден. Установка...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        print(f"Модуль {module_name} установлен. Повторная попытка импорта...")
        importlib.import_module(module_name)
        print(f"Модуль {module_name} успешно импортирован после установки.")

def ensure_imports():
    modules = ["socket", "concurrent.futures", "urllib.parse"]
    for module in modules:
        ensure_import(module)

def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    sock.close()
    return port, result == 0

def scan_ports(ip, ports):
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, ip, port) for port in ports]
        for future in concurrent.futures.as_completed(futures):
            port, is_open = future.result()
            if is_open:
                print(f"Сканирую {port} - успех. Айпи - {ip}, Порт - {port}")
                open_ports.append(port)
            else:
                print(f"Сканирую {port} - мимо.")
    return open_ports

def main():
    ensure_imports()
    url = input("Введите URL сайта (с http/https): ")
    parsed_url = urllib.parse.urlparse(url)
    hostname = parsed_url.hostname
    ip = socket.gethostbyname(hostname)
    print(f"IP-адрес сайта: {ip}")
    ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 115, 135, 139, 143, 194, 443, 445, 1433, 3306, 3389, 5632, 5900, 25565]
    open_ports = scan_ports(ip, ports_to_scan)
    if open_ports:
        print(f"Открытые порты: {', '.join(map(str, open_ports))}")
    else:
        print("Нет открытых портов среди указанных.")

if __name__ == "__main__":
    main()
