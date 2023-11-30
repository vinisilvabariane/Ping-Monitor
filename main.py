import threading
import time
import socket
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import ping3
import smtplib
from tkinter import messagebox
from email.mime.text import MIMEText

smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'tihbaextrema@gmail.com'
sender_password = 'dyvbhqkhqguzvxmj'
recipient_email = 'tihbaextrema@gmail.com'
subject = 'Dispositivos que pararam de responder ao ping'
device_list = []
previous_statuses = {}
ip_indexes = {}

class PingMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Ping Monitor')
        self.root.state('zoomed')  # Inicia maximizado

        self.table_columns = ('Device', 'Status')
        self.table = ttk.Treeview(root, columns=self.table_columns, show='headings')
        for col in self.table_columns:
            self.table.heading(col, text=col.title())
            self.table.column(col, anchor='center')
        self.table.pack(fill='both', expand=True)  # Ajuste de posição da tabela

        self.add_button = tk.Button(root, text="Add Device", command=self.add_device)
        self.add_button.pack()

        self.remove_button = tk.Button(root, text="Remove Selected", command=self.remove_selected)
        self.remove_button.pack()

        self.start_monitoring_button = tk.Button(root, text="Start Monitoring", command=self.start_monitoring)
        self.start_monitoring_button.pack()

        self.stop_monitoring_button = tk.Button(root, text="Stop Monitoring", command=self.stop_monitoring)
        self.stop_monitoring_button.pack()

        self.status_label = tk.Label(root, text="Not Monitoring", anchor="e", justify="right")
        self.status_label.pack(side="bottom", anchor="e", padx=10, pady=5)

        instructions_text = """
        Instruções de uso:

        1-) Adicione os IPs requisitados.
        2-) Comece o monitoramento.
        3-) Em caso de remoção de IPs, pare o monitoramento,
        exclua e depois comece de novo.
        """
        self.instructions_label = tk.Label(root, text=instructions_text, anchor="w", justify="left")
        self.instructions_label.pack(side="bottom", anchor="w", padx=10, pady=5)

        self.version_label = tk.Label(root, text="Versão 3.0", anchor="e", justify="right")
        self.version_label.pack(side="bottom", anchor="e", padx=10, pady=5)

        self.monitoring = False  # Variável de controle
        self.thread_ping = None  # Variável para armazenar a thread

        # Adicionar linhas separadoras
        separator_ips = ttk.Separator(root, orient="horizontal")
        separator_ips.pack(fill="x", padx=10, pady=(5, 0))

        separator_status = ttk.Separator(root, orient="horizontal")
        separator_status.pack(fill="x", padx=10, pady=(0, 5))

    def add_device(self):
        ips = simpledialog.askstring("Add Devices", "Enter IP addresses (separated by comma or space):")
        if ips:
            new_ips = [ip.strip() for ip in ips.replace(",", " ").split()]
            for ip in new_ips:
                if ip and ip not in device_list:
                    device_list.append(ip)
                    previous_statuses[ip] = None
                    ip_indexes[ip] = self.table.insert('', 'end', values=(ip, ''))

    def remove_selected(self):
        selection = self.table.selection()
        for item in selection:
            ip = self.table.item(item, "values")[0]
            device_list.remove(ip)
            del previous_statuses[ip]
            self.table.delete(item)

    def start_monitoring(self):
        if not self.monitoring:
            self.monitoring = True
            self.clear_table_entries()
            # Adiciona uma variável de condição para indicar à thread que ela deve continuar
            self.stop_signal = threading.Event()
            self.thread_ping = threading.Thread(target=self.update_table)
            self.thread_ping.daemon = True
            self.thread_ping.start()
            self.status_label.config(text="Monitoring", fg="green")

    def clear_table_entries(self):
        for ip in device_list:
            self.table.item(ip_indexes[ip], values=(ip,''))

    def stop_monitoring(self):
        if self.monitoring:
            self.monitoring = False
            # Adiciona um sinalizador para indicar à thread que ela deve parar
            self.stop_signal.set()
            self.thread_ping.join(timeout=5)  # Aguarda a thread terminar com um timeout de 5 segundos
            self.status_label.config(text="Not Monitoring", fg="red")
            # Adiciona uma verificação se a thread ainda está ativa antes de limpar as entradas da tabela
            if self.thread_ping.is_alive():
                self.show_thread_active_warning()

    def update_table(self):
        while not self.stop_signal.is_set():  # Continua enquanto o sinalizador não estiver definido
            non_responding_devices = []

            for ip in device_list:
                try:
                    ip_address = socket.gethostbyname(ip)
                    response = ping3.ping(ip_address)
                except socket.error:
                    response = None

                if response is None:
                    if previous_statuses[ip] != 'Not Responding':
                        previous_statuses[ip] = 'Not Responding'
                        non_responding_devices.append(ip)
                else:
                    if previous_statuses[ip] != 'OK':
                        previous_statuses[ip] = 'OK'

            for ip in device_list:
                status = previous_statuses[ip]
                self.table.item(ip_indexes[ip], values=(ip, status))

            # Move a verificação de dispositivos não responsivos para fora do loop
            if non_responding_devices:
                self.send_alert_email(non_responding_devices)

            time.sleep(1)

    def send_alert_email(self, non_responding_devices):
        subject = 'Alerta de Dispositivos Não Respondendo'
        if non_responding_devices:
            body = "Os seguintes dispositivos não estão respondendo ao ping:\n\n"
            for ip in non_responding_devices:
                body += f"{ip}\n"
            sender_email = 'tihbaextrema@gmail.com'
            sender_password = 'dyvbhqkhqguzvxmj'
            recipient_email = 'tihbaextrema@gmail.com'
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = recipient_email

            try:
                # Conecta-se ao servidor SMTP
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)

                # Envio do e-mail
                server.sendmail(sender_email, [recipient_email], msg.as_string())

                # Desconecta do servidor SMTP
                server.quit()

                # Mostra uma mensagem de sucesso
                self.show_email_success_message()

            except Exception as e:
                print(f"Erro ao enviar e-mail: {e}")

                # Mostra uma mensagem de falha
                self.show_email_failure_message()

    def show_thread_active_warning(self):
        messagebox.showwarning("Aviso","Monitoramento Parado!!")

    def show_email_failure_message(self):
        messagebox.showerror("Erro ao Enviar E-mail", "Ocorreu um erro ao enviar o e-mail.")

def main():
    root = tk.Tk()
    app = PingMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()