#!/usr/bin/env python
import os
import subprocess

def run_cmd(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    ##print(f"{cmd}:\n{out.decode()}")
    if process.returncode != 0 and err:
        print(f"Ошибка: {err.decode()}")
        return None
    return out.decode()


def main():
    print("Проверка наличия Nginx...")
    nginx_status = run_cmd("systemctl is-active nginx")
    if nginx_status == "active\n":
        print("!!! WARNING !!! An active Nginx instance has been detected. If you continue, all data will be overwritten.")
        choice = input("Continue? (yes/no): ")
        if choice.lower() != "yes":
            print("Выход...")
            return

    print("Обновление и установка Nginx...")
    run_cmd("yum update -y")
    run_cmd("yum install -y nginx")
    run_cmd("systemctl start nginx")

    print("Проверка установки Nginx...")
    nginx_status = run_cmd("systemctl is-active nginx")
    if nginx_status != "active\n":
        print("Ошибка при установке Nginx!")
        return

    print("Настройка веб-страницы...")
    with open('/usr/share/nginx/html/index.html', 'w') as f:
        f.write('<html><body><h1>TEST TASK DONE!</h1><img src="https://www.epam.com/content/dam/epam/whitepapers/a-call-to-action-for-generative-ai/a_call_to_action_for_generative_ai_cs_4.jpg" /></body></html>')

    print("Запуск Nginx...")
    run_cmd("systemctl restart nginx")
    print("Установка и настройка Nginx успешно завершены!")

if __name__ == "__main__":
    main()