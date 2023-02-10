import os
import colorama

# test
colorama.init()
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
#init colors
wrong_symbols = ['\\', '|', '/', '*', '?', '"', '<', '>']

def create_src_path():
    try:
        if not os.path.exists("src"):
            os.mkdir("src")
            print(f"{GREEN}[+] src created{RESET}")
        if not os.path.exists("output"):
            os.mkdir("output")
            print(f"{GREEN}[+] output created{RESET}")
        if not os.path.exists("model"):
            os.mkdir("model")
            print(f"{GREEN}[+] model created{RESET}")
    except Exception as ex:
        print(ex)

def del_empty_dirs(path):
    for d in os.listdir(path):
        a = os.path.join(path, d)
        if os.path.isdir(a):
            del_empty_dirs(a)
            if not os.listdir(a):
                os.rmdir(a)
                print(a, ' DELETED')

def name_checker(name):
    tempa = ""
    fl = False
    for sym in wrong_symbols:
        if sym in name:
            tempa = name.replace(sym, '')
            fl = True
    if fl:
        return tempa
    else:
        return name

def init_project(path):
    try:
        while True:
            print(f"[?]{GRAY}NAME PROJECT:{RESET}")
            project_name_e = input()
            project_name = path + "\\" + project_name_e
            if os.path.exists(f"{project_name}"):
                print(f"[+]{GREEN}PROJECT {project_name} CREATED{RESET}")
                return project_name
                
            try:
                os.mkdir(f"{project_name}")
                
            except Exception as ex:
                print(f"init_project mkdir:{ex}")

            if os.path.exists(f"{project_name}"):
                print(f"[+]{GREEN}PROJECT {project_name} ALREADY CREATED{RESET}")
                return project_name
    except Exception as ex:
        print(ex)

def find_index_path(str):
    return ''.join(x for x in str if x.isdigit())

