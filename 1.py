from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
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
notification_type = None  # None, 'connected', 'disconnected'
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

def find_processes_by_port(port):
    processes_info = []

    for conn in psutil.net_connections(kind="inet"):
        if conn.laddr.port == port:
            pid = conn.pid
            if pid:
                try:
                    process = psutil.Process(pid)
                    process_name = process.name()
                    ip = conn.laddr.ip
                    processes_info.append((process_name, pid, ip))
                except psutil.NoSuchProcess:
                    continue

    return processes_info

def main():
    global notification_type
    while not stop_flag.is_set():
        connections_status = [find_processes_by_port(port) for port in ports]
        has_connections = any(connections_status)

        if has_connections and notification_type != 'connected':
            threading.Thread(target=show_md, args=("Detected connection.",0x30,)).start()
            notification_type = 'connected'

        elif not has_connections and notification_type != 'disconnected':
            threading.Thread(target=show_md, args=("Host terminated the session.",)).start()
            notification_type = 'disconnected'

        time.sleep(1)

class iconControl:
    def __init__(self):
        self.icon = None

    def open_repository(self):
        wb.open("https://github.com/Pilm404/Anti-Veyon")

    def status(self):
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        threading.Thread(target=show_md, args=(f"Status:\nThe program is running as administrator: {'yes' if is_admin else 'no'} \nIs the host connected: {'yes' if notification_type == 'connected' else 'no'}",)).start()

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
