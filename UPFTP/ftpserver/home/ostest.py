# -*- encoding: utf-8 -*-
import os
path=os.path.join(os.getcwd(),'zw')
print(len(os.listdir(path)))
# rootdir = os.getcwd()               #获取当前路径
# x  = u'统计文件大小.csv'
# f = open(os.path.join(rootdir,x), "w+")
# for dirname in  os.listdir(rootdir):  #获取二级目录所有文件夹与文件
#     Dir = os.path.join(rootdir, dirname)    #路径补齐
#     count = 0
#     if (os.path.isdir(Dir)):           #判断是否为目录
#         for r, ds, files in os.walk(Dir): #遍历目录下所有文件根，目录下的每一个文件夹(包含它自己), 产生3-元组 (dirpath, dirnames, filenames)【文件夹路径, 文件夹名字, 文件名称】
#             for file in files:      #遍历所有文件
#                 size = os.path.getsize(os.path.join(r, file)) #获取文件大小
#                 count += size
#         if ((count/1024.0/1024.0) < 1024):
#             print (Dir +'\t' + '%.2f'% (count/1024.0/1024.0)+'MB')
#             f.write(Dir+','+  '%.2f'% (count/1024.0/1024.0)+'MB' + '\n')
#         else:
#             print (Dir + '\t' + '%.2f' % (count / 1024.0 / 1024.0/1024.0) + 'GB')
#             f.write(Dir + ',' + '%.2f' % (count / 1024.0 / 1024.0/1024.0) + 'GB' + '\n')
#     else:
#         continue
# f.close()