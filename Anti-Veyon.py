from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import socket
import threading
import time
import psutil
import ctypes
import win32service
import win32serviceutil
import webbrowser as wb

ports = [11100, 11200, 11300]
app_name = "Anti Veyon Guard"
service_name = "VeyonService"
active_connections = []
stop_flag = threading.Event()

def show_md(message, icon=0x40):
    ctypes.windll.user32.MessageBoxW(None, message, app_name, icon | 0x0 | 0x1000)

def service_status():
    services = [s for s in psutil.win_service_iter() if s.name() == service_name]
    if not services:
        return False
    return True

def stop_service():
    is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    if is_admin:
        status = win32serviceutil.QueryServiceStatus(service_name)
        if status[1] == win32service.SERVICE_RUNNING:
            win32serviceutil.StopService(service_name)
            threading.Thread(target=show_md, args=("The service has been stopped successfully.",)).start()
            return True
        elif status[1] == win32service.SERVICE_STOPPED:
            win32serviceutil.StartService(service_name)
            threading.Thread(target=show_md, args=("The service has been started successfully.", 0x30)).start()
            return True
        else:
            return False
    else:
        threading.Thread(target=show_md, args=("To perform this action, please restart the program as administrator to continue.", 0x10,)).start()

def status_check():
    res = []
    for ip in list(set(active_connections)):
        ip = socket.gethostbyaddr(ip)[0]
        res.append(ip)
    return res

def find_service():
    global active_connections
    last_connection = active_connections
    while not stop_flag.is_set():
        if last_connection != active_connections:
            threading.Thread(target=show_md, args=("Detected conection",)).start()
            last_connection = active_connections

    time.sleep(1)

def main():
    global active_connections
    threading.Thread(target=find_service).start()
    while not stop_flag.is_set():
        temp_connetions = []
        for conn in psutil.net_connections(kind="tcp"):
            if conn.status == "ESTABLISHED" and conn.laddr.port in ports:
                temp_connetions.append(conn.laddr.ip)
        active_connections = temp_connetions
        time.sleep(1)

class iconControl:
    def __init__(self):
        self.icon = None

    def open_repository(self):
        wb.open("https://github.com/Pilm404/Anti-Veyon")

    def status(self):
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        threading.Thread(target=show_md, args=(f"Status:\nThe program is running as administrator: {'yes' if is_admin else 'no'} \nActive connections {status_check()}",)).start()

    def exit_app(self, icon, item):
        global main_thread
        if self.icon:
            stop_flag.set()
            main_thread.join()
            self.icon.stop()

    def create_image(self):
        image = Image.new('RGB', (64, 64), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 64, 64), fill=(255, 0, 0))
        return image

    def setup_tray_icon(self):
        menu = Menu(
            MenuItem('Status', lambda icon, item: self.status()),
            MenuItem('Stop or restart service', lambda icon, item: stop_service()),
            MenuItem('Open GitHub repository', lambda icon, item: self.open_repository()),
            MenuItem('Exit', lambda icon, item: self.exit_app(icon, item))
        )

        self.icon = Icon("Anti-Veyon Guard", self.create_image(), "Anti-Veyon Guard", menu)
        self.icon.run()

if __name__ == "__main__":
    if service_status():
        show_md(f"Welcome to Anti-Veyon Guard program. To open actions click on hidden icons then click on red square. {'Some functions of the program will be unavailable because you launched it, no, you are not an administrator.' if not ctypes.windll.shell32.IsUserAnAdmin() else ''} The program will start after pressing the OK button.")
        main_thread = threading.Thread(target=main)
        main_thread.start()
        iconControl().setup_tray_icon()
    else:
        show_md("The Veyon program service is not installed", 0x10)
