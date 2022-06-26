# from https://stackoverflow.com/questions/490195/split-a-multi-page-pdf-file-into-multiple-pdf-files-with-python
# pdf2iamge 纯纯sb，不支持中文搞什么吃的。

# wand 给出的图片质量太低了，垃圾

# import pdf2image

# 安装 poppler: https://stackoverflow.com/questions/18381713/how-to-install-poppler-on-windows
# 安装 poppler-data: https://tm23forest.com/contents/poppler-for-windows (Poppler-datadir is ./share/poppler (relative path from binary).) 直接下载然后命名

# 直接用 pdftoppm 命令就可以了，不用什么 pdf2image

import os

# https://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python
from pathlib import Path

downdir=os.getcwd()
outdir=os.getcwd()

# 最新的pdf文件
pdf_path_obj = sorted(Path(downdir).glob("*.pdf"), key=os.path.getctime,reverse=True)[0]
pdf_path=pdf_path_obj.as_posix()
# print(type(pdf_path))
out_path = outdir + os.sep + pdf_path_obj.stem

comm=f"pdftoppm \"{pdf_path}\" -jpeg \"{out_path}\""
# print(comm)
os.system(comm)

padding_ori_dict={"0"+str(each):str(each) for each in range(1,10)}

os.chdir(outdir)

# 有时候用 1,2,3,4 有时候又用 01,02,03,04 搞不懂这群老外咋想的...
## 全给你format了

for each in os.listdir(outdir):
    if each.endswith(".jpg"):
        head=each.split("-")[0]
        mid=each.split("-")[1].replace(".jpg", "")
        if mid in padding_ori_dict.keys():
            new_mid=padding_ori_dict[mid]
            new_name=head+"-"+new_mid+".jpg"
            os.rename(each,new_name)

print("done.")


