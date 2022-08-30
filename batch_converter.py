from os import listdir, system, chdir
from os.path import isfile, join, splitext, exists
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog

video_formats_dict ={"avi":".avi","mp4":".mp4","mkv":".mkv","ts":".ts",
               "mpeg":".mpeg","mov":".mov"}
hw_accel_dict = {"nvidia":"python ffpb.py -hwaccel cuda -hwaccel_output_format cuda -i ",
                 "intel":"python ffpb.py -hwaccel qsv -c:v h264_qsv -i ",
                 "dxva2":"python ffpb.py -hwaccel dxva2 -i ",
                 "none":"python ffpb.py -i "}

root = tk.Tk()
root.withdraw()

contents = []
directory = ""

def video_format():
    format = ""
    choice = '0'
    while choice == '0':
        print("Choose video format:\n"
              "1. MP4\n"
              "2. MKV\n"
              "3. AVI\n"
              "4. MOV\n"
              "5. TS\n"
              "6. MPEG\n"
              "99. Back to Main Menu")
        choice = input("Your Choice: ")
        if choice == "1":
            format = video_formats_dict["mp4"]
        elif choice == "2":
            format = video_formats_dict["mkv"]
        elif choice == "3":
            format = video_formats_dict["avi"]
        elif choice == "4":
            format = video_formats_dict["mov"]
        elif choice == "5":
            format = video_formats_dict["ts"]
        elif choice == "6":
            format = video_formats_dict["mpeg"]
        elif choice == "99":
            chdir("../")
            main()
        else:
            print("\nNot Valid Choice")
            format = "NA"
    return format

def hardware_acc():
    cmd = ""
    choice = '0'
    while choice == "0":
        print("Do you want to use Hardware acceleration?\n"
               "1. YES\n"
               "2. NO\n"
               "If You choose YES, make sure you have the hardware")
        choice = input("Your Choice: ")
        if choice == "1":
            choice = '0'
            while choice == '0':
                print("Choose HW accelerator:\n"
                      "1. NVida\n"
                      "2. Intel (experimental)\n"
                      "3. DXVA2 \n"
                      "4. Back")
                choice = input("Your Choice: ")
                if choice == "1":
                    cmd = hw_accel_dict["nvidia"]+",nv"
                elif choice == "2":
                    cmd = hw_accel_dict["intel"]+",it"
                elif choice == "3":
                    cmd = hw_accel_dict["dxva2"]+",dx"
                elif choice == "4":
                    chdir("../")
                    main()
                else:
                    print("Not Valid Choice")
                    chdir("../")
                    main()
        elif choice == "2":
            cmd = hw_accel_dict["none"]+",nn"
        else:
            chdir("../")
            main()
    return cmd

def single_convert():
    chdir("ffpb")
    print("\n==========================\n"
          "||SINGLE VIDEO CONVERTER||\n"
          "==========================\n\n\n"
          "===Choose Soucer File===")
    file = filedialog.askopenfilename()
    if exists(file):
        file_name, file_extension = splitext(file)
        print("=== Target Video Format ===")
        target_format=video_format()
        if target_format == "NA":
            chdir("../")
            single_convert()
        else:
            source_vid = "\""+file+"\""
            dest_vid = "\""+file_name+target_format+"\""
            cmd = hardware_acc()
            print(cmd)
            cmd_split = cmd.split(",")
            if cmd_split[1] == "nv":
                convert = cmd_split[0] + source_vid + " -c:v h264_nvenc -preset fast " + dest_vid
                system(convert)
                print("Done Converting")
                chdir("../")
                main()
            else:
                convert = cmd_split[0] + source_vid + " " + dest_vid
                system(convert)
                print("Done Converting")
                chdir("../")
                main()
    else:
        print("File Not Exist\n"
              "Please enter correct path")
        chdir("../")
        single_convert()

def batch_convert():
    global directory
    global contents
    chdir("ffpb")
    print("\n=========================\n"
          "||BATCH VIDEO CONVERTER||\n"
          "=========================\n\n\n"
          "===Choose Source Directory===")
    directory = filedialog.askdirectory()
    if exists(directory):
        contents = [f for f in listdir(directory) if isfile(join(directory, f))]
        choice = "0"
        while choice == "0":
            print("What source video format do you want to convert?\n"
                  "1. All video format in directory\n"
                  "2. Specific Format")
            choice = input("Your Choice: ")
            if choice == "1":
                batch_all_format(directory,contents)
            elif choice == "2":
                batch_specific_format()
            else:
                print("Not Valid Choice")
                chdir("../")
                batch_convert()
    else:
        print("Directory Not Exist\n"
              "Please enter correct path")
        chdir("../")
        batch_convert()

def batch_all_format(directory,contents):
    target_format = video_format()
    if target_format == "NA":
        chdir("../")
        batch_convert()
    else:
        cmd = hardware_acc()
        cmd_split = cmd.split(",")
        if cmd_split[1] == "nv":
            for n in tqdm(contents):
                file_name, file_extension = splitext(n)
                source_vid = "\"" + directory + "/" + n + "\""
                dest_vid = "\"" + directory + "/" + n.replace(file_extension, target_format) + "\""
                convert = cmd_split[0] + source_vid + " -c:v h264_nvenc -preset fast " + dest_vid
                system(convert)
            print("Done Converting")
            chdir("../")
            main()
        else:
            for n in tqdm(contents):
                file_name, file_extension = splitext(n)
                source_vid = "\"" + directory + "/" + n + "\""
                dest_vid = "\"" + directory + "/" + n.replace(file_extension, target_format) + "\""
                convert = cmd_split[0] + source_vid + " " + dest_vid
                system(convert)
            print("Done Converting")
            chdir("../")
            main()

def batch_specific_format():
    print("\n=== Source Video Format ===")
    source_format = video_format()
    if source_format == "NA":
        chdir("../")
        batch_convert()
    else:
        video_file =[]
        sort_video = filter(lambda m: source_format in m, contents)
        for f in sort_video:
            video_file.append(f)
        sort_video_upper = filter(lambda m: source_format.upper() in m, contents)
        for f in sort_video_upper:
            video_file.append(f)
        if not video_file:
            print("There's No Video File with %s format, please choose another format" % source_format)
            batch_specific_format()
        else:
            print("\n=== Target Video Format ===")
            target_format = video_format()
            if target_format == "NA":
                chdir("../")
                batch_convert()
            else:
                cmd = hardware_acc()
                cmd_split = cmd.split(",")
                if cmd_split[1] == "nv":
                    for n in tqdm(video_file):
                        file_name, file_extension = splitext(n)
                        source_vid = "\"" + directory + "/" + n + "\""
                        dest_vid = "\"" + directory + "/" + n.replace(file_extension, target_format) + "\""
                        convert = cmd_split[0] + source_vid + " -c:v h264_nvenc -preset fast " + dest_vid
                        system(convert)
                    print("Done Converting")
                    chdir("../")
                    main()
                else:
                    for n in tqdm(video_file):
                        file_name, file_extension = splitext(n)
                        source_vid = "\"" + directory + "/" + n + "\""
                        dest_vid = "\"" + directory + "/" + n.replace(file_extension, target_format) + "\""
                        convert = cmd_split[0] + source_vid + " " + dest_vid
                        system(convert)
                    print("Done Converting")
                    chdir("../")
                    main()


def main():
    choice = '0'
    while choice == '0':
        print("\n==========================\n"
              "||VIDEO CONVERTER By rpb||\n"
              "==========================\n"
              "Choose your choice:\n"
              "1. Individual Converter\n"
              "2. Batch Converter\n"
              "3. Exit")
        choice = input("Your choice: ")
        if choice =='1':
            single_convert()
        elif choice == "2":
            batch_convert()
        elif choice == "3":
            exit()
        else:
            print("Not Valid choice")
            main()

main()

