# from https://stackoverflow.com/questions/490195/split-a-multi-page-pdf-file-into-multiple-pdf-files-with-python
# pdf2iamge 纯纯sb，不支持中文搞什么吃的。

# wand 给出的图片质量太低了，垃圾

# import pdf2image

# 安装 poppler: https://stackoverflow.com/questions/18381713/how-to-install-poppler-on-windows
# 安装 poppler-data: https://tm23forest.com/contents/poppler-for-windows (Poppler-datadir is ./share/poppler (relative path from binary).) 直接下载然后命名

# 直接用 pdftoppm 命令就可以了，不用什么 pdf2image

import os
import time

# https://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python
from pathlib import Path

from xpinyin import Pinyin

p=Pinyin()

with open("D:\simple_video_generate\svg_paths.txt","r",encoding="utf-8") as f:
    current_svg=f.readlines()[-1].strip("\n")
    print("文件夹名称是：{}".format(current_svg))

# current_svg=p.get_pinyin(chars)
# os.rename(src, dst)

os.chdir(current_svg)
downdir=os.getcwd()
outdir=os.getcwd()

# 最新的pdf文件
pdf_path_obj = sorted(Path(downdir).glob("*.pdf"), key=os.path.getctime,reverse=True)[0]
pdf_path=pdf_path_obj.as_posix()
filename=pdf_path.split(os.sep)[-1].replace(".pdf", "")
print(filename)
new_filename=p.get_pinyin(filename,"-")
print(new_filename)

os.rename(filename+".pdf",new_filename+".pdf")

pdf_path=pdf_path.replace(filename, new_filename)
# print(type(pdf_path))
out_path = new_filename 

comm=f"pdftoppm \"{pdf_path}\" -jpeg \"{out_path}\""
print(comm)
os.system(comm)

padding_ori_dict={"0"+str(each):str(each) for each in range(1,10)}

os.chdir(outdir)

# 有时候用 1,2,3,4 有时候又用 01,02,03,04 搞不懂这群老外咋想的...
## 全给你format了

for each in os.listdir(outdir):
    if each.endswith(".jpg"):
        last_hyphen_idx=each.rfind("-")
        head=each[0:last_hyphen_idx]
        tail=each[last_hyphen_idx+1:]
        mid=tail.replace(".jpg", "")
        if mid in padding_ori_dict.keys():
            new_mid=padding_ori_dict[mid]
            new_name=head+"-"+new_mid+".jpg"
            os.rename(each,new_name)

os.rename(new_filename+".pdf", filename+".pdf")

print("done.")


