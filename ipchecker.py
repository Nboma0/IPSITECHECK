
import socket
import concurrent.futures

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

if __name__ == "__main__":
    url = input("Введите URL сайта (без http/https): ")
    ip = socket.gethostbyname(url)
    print(f"IP-адрес сайта: {ip}")
    ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 115, 135, 139, 143, 194, 443, 445, 1433, 3306, 3389, 5632, 5900, 25565]
    open_ports = scan_ports(ip, ports_to_scan)
    if open_ports:
        print(f"Открытые порты: {', '.join(map(str, open_ports))}")
    else:
        print("Нет открытых портов среди указанных.")
