from os import listdir, system, chdir
from os.path import isfile, join
from tqdm import tqdm

source_dir="./samples"

contents = [ f for f in listdir(source_dir) if isfile(join(source_dir,f))]

cleaned = []

upper = filter(lambda m: '.TS' in m, contents)
for f in upper:
    cleaned.append(f)

lower = filter(lambda m: '.ts' in m, contents)
for f in lower:
    uppered = f.replace(".ts", ".TS")
    cleaned.append(uppered)

chdir("ffpb")
for n in tqdm(cleaned):
    source_vid = "\""+source_dir + "/" + n +"\""
    dest_vid = "\""+source_dir + "/" + n.replace(".TS", ".mp4")+"\""
    # command = source_vid + " " + dest_vid
    command_nvid = source_vid + " -c:v h264_nvenc -preset fast " + dest_vid   # -preset slow output
    # ffpb_conv = "python ffpb.py -i " + command
    ffpb_conv_nvid = "python ffpb.py -hwaccel cuda -hwaccel_output_format cuda -i " + command_nvid
    system(ffpb_conv_nvid)




