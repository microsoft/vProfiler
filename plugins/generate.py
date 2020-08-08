import os

def generate_sosreport():
    print("Now running sosreport")
    os.system("sudo sosreport --batch --quiet --tmp-dir .; sudo chown `whoami` sosreport*")

if __name__ == "__main__":
    generate_sosreport()
