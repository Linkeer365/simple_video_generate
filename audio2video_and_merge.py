import subprocess

# 直接用命令行跑是没问题的，但不知道为什么pycharm就是不能识别出这个ffmpeg的环境变量

import os
from time import sleep
import shutil

# for i in os.environ.get("PATH").split(";"):
#     print(i)
#
# os._exit(0)

ffmpeg_path=r"D:\ffmpeg\ffmpeg-2022-02-21-git-b8e58f0858-full_build\bin"
finish_dir=r"D:\AllDowns"

finish_name=[each.replace(".pdf","") for each in os.listdir(".") if each.endswith(".pdf")][0]
print(finish_name)

cwd=os.getcwd()

if os.path.exists("mylist.txt"):
    open("mylist.txt","w").close()

def a2v(audio_file:str,img_file:str,video_file:str) -> None:
    if img_file == "":
        print("no img.")
    elif audio_file == "":
        print("no audio.")
    else:
        not_divisible_by_two="-vf \"scale=2*trunc(iw/2):2*trunc(ih/2),setsar=1\""
        
        command_str=f"ffmpeg -loop 1 -i \"{img_file}\" -i \"{audio_file}\" {not_divisible_by_two} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -shortest \"{video_file}\" -y"
        
        # 至今不清楚这条该怎么写hh
        ## 破案了，不能用 -r 0.1

        # command_str=f"ffmpeg -hide_banner -loop 1 -i \"{img_file}\" -i \"{audio_file}\" {not_divisible_by_two} -c:v libx264 -preset ultrafast -tune stillimage -c:a copy -pix_fmt yuv420p -shortest \"{video_file}\" -y"
        
        print(command_str)
        # os.system ('chcp 65001')
        os.system(command_str)


def path_format(path,suffix,cwd):
    if not path.endswith(suffix):
        path+=f"{suffix}"
    if not os.sep in path:
        path=cwd+os.sep+path
    print(path)
    return path

if __name__=="__main__":
    files=os.listdir(".")
    mp3_files=[each for each in files if each.endswith(".mp3")]
    mp3_files=sorted(mp3_files,key=lambda x:int(x.split("-")[-1].replace(".mp3","")))
    pic_files=[each for each in files if each.endswith(".jpg")]
    pic_files=sorted(pic_files,key=lambda x:int(x.split("-")[-1].replace(".jpg","")))
    
    mp3_pic_zip=zip(mp3_files,pic_files)

    for mp3,pic in mp3_pic_zip:
        audio_file=cwd+os.sep+mp3
        img_file=cwd+os.sep+pic
        video_file=cwd+os.sep+mp3.replace(".mp3", "")+".mp4"
        a2v(audio_file, img_file, video_file)
        with open("mylist.txt","a",encoding="gbk") as f:
            f.write(f"file \'{video_file}\'\n")
        print("one done.")

    # poppler 会出现乱码很烦，换了一种写法

    # print(mp3_files)
    # os._exit(0)
    # for each in mp3_files:
    #     if each.endswith(".mp3"):
    #         print(each)
    #         filename=each.replace(".mp3","")
    #         print(filename)
    #         img_file=filename+".jpg"
    #         print(img_file)
    #         # assert img_file in files
    #         audio_file=path_format(filename,".mp3",cwd)
    #         # if not "loud" in audio_file:
    #             # audio_file2=path_format("loud_"+filename, ".mp3", cwd)
    #         # else:
    #             # audio_file2=audio_file
    #         # volume_raise_comm=f"ffmpeg -i \"{audio_file}\" -af \"volume=50\" \"{audio_file2}\" -y"
    #         # print(volume_raise_comm)
    #         # os.system(volume_raise_comm)
    #         # sleep(3)
    #         img_file=path_format(filename,".jpg",cwd)
    #         video_file=path_format(filename,".mp4",cwd)
    #         a2v(audio_file,img_file,video_file)
    #         with open("mylist.txt","a",encoding="gbk") as f:
    #             f.write(f"file \'{video_file}\'\n")
    #         print("one done.")
    finish_path=finish_dir+os.sep+finish_name+".mp4"
    concat_comm=f"ffmpeg -f concat -safe 0 -i mylist.txt -c copy \"{finish_path}\" -y"
    os.system(concat_comm)
    shutil.copyfile(finish_path, "video-collection/{}.mp4".format(finish_name))

    
