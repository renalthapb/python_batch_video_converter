from os import listdir, system, chdir
from os.path import isfile, join, splitext, exists
from tqdm import tqdm

video_formats_dict =[{"avi":".avi","mp4":".mp4","mkv":".mkv","ts":".ts",
               "mpeg":".mpeg","mov":".mov"}]


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
            format = video_formats_dict[0]["mp4"]
        elif choice == "2":
            format = video_formats_dict[0]["mkv"]
        elif choice == "3":
            format = video_formats_dict[0]["avi"]
        elif choice == "4":
            format = video_formats_dict[0]["mov"]
        elif choice == "5":
            format = video_formats_dict[0]["ts"]
        elif choice == "6":
            format = video_formats_dict[0]["mpeg"]
        elif choice == "99":
            main()
        else:
            print("\nNot Valid Choice")
            format = "NA"
    return format

def single_convert():
    chdir("ffpb")
    print("\n==========================\n"
          "||SINGLE VIDEO CONVERTER||\n"
          "==========================\n")
    file = input("Enter video file path to Convert: ")
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
            command = source_vid + " -c:v h264_nvenc -preset fast " + dest_vid
            ffpb_conv = "python ffpb.py -hwaccel cuda -hwaccel_output_format cuda -i " + command
            system(ffpb_conv)
            print("Done Converting")
            chdir("../")
            main()
    else:
        print("File Not Exist\n"
              "Please enter correct path")
        chdir("../")
        single_convert()

def batch_convert():
    chdir("ffpb")
    print("\n=========================\n"
          "||BATCH VIDEO CONVERTER||\n"
          "=========================\n")
    directory = input("Enter directory path to Convert: ")
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
                batch_specific_format(directory,contents)
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
        for n in tqdm(contents):
            file_name, file_extension = splitext(n)
            source_vid = "\"" + directory + "/" + n + "\""
            dest_vid = "\"" + directory + "/" + n.replace(file_extension, target_format) + "\""
            command = source_vid + " -c:v h264_nvenc -preset fast " + dest_vid
            ffpb_conv = "python ffpb.py -hwaccel cuda -hwaccel_output_format cuda -i " + command
            system(ffpb_conv)
        print("Done Converting")
        chdir("../")
        main()

def batch_specific_format(directory,contents):
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
        print("\n=== Target Video Format ===")
        target_format = video_format()
        if target_format == "NA":
            chdir("../")
            batch_convert()
        else:
            for n in tqdm(video_file):
                file_name, file_extension = splitext(n)
                source_vid = "\"" + directory + "/" + n + "\""
                dest_vid = "\"" + directory + "/" + n.replace(file_extension, target_format) + "\""
                command = source_vid + " -c:v h264_nvenc -preset fast " + dest_vid
                ffpb_conv = "python ffpb.py -hwaccel cuda -hwaccel_output_format cuda -i " + command
                system(ffpb_conv)
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

