import main
import os
directory = "QRArxiv"
if not os.path.exists(directory):
    os.makedirs(directory)
    print(os.listdir())
    for file in os.listdir():
        if file.endswith(".pdf"):
            try:
                main.QRArxiv(file,dir=directory)
                print("The file {} is ready to eat.".format(file))
            except PermissionError:
                print("""Permission error'""")
                continue

            except Exception:
                print("ouch. {} hurts.".format(file))
else:
    filesonmain = os.listdir()
    filesondir  = os.listdir(directory)
    print(filesonmain)
    print(filesondir)
    for file in filesonmain:
        if file.endswith('.pdf'):
            if (file[:-4]+'-qr.pdf' not in filesondir):
                main.QRArxiv(file,dir=directory)
                print("Done\tThe file {} is ready to eat.".format(file))
            else:
                print("Stopped\tThe file {0} is already in the folder {1}. If you want to redo the operation, delete it or move it from {1}.".format(file,directory))
