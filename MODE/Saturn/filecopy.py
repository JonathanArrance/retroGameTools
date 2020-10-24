#!/bin/python
import os
import re
import shutil
import subprocess
import time

gamesdir = '/mnt/win/RetroGames/SegaSatrun/SegaSaturn2018July10'
target = '/media/jon/sega/Saturn/USA/'
region = '(USA)'

readin = os.scandir(gamesdir)
'''
def procedure():
    try:
        #copy the zip file to the external HD
        shutil.copy(zippath,path)
    except Exception as e:
        print(e)

    try:
        #extract the zip
        archive = py7zr.SevenZipFile('%s'%(n), mode='r')
        archive.extractall(path="%s"%(path))
        archive.close()
    except Exception as e:
        print(e)

    try:
        #delete the old zip remnent
        os.remove(delpath)
    except Exception as e:
        print(e)
'''

for game in readin:
    #print(game.name)
    if region in game.name:
        n = game.name
        print("Working on %s"%(n))
        s = n.split(region)
        #construct a directory name from the zip file name.
        dirname = str(s[0]).strip().replace(' ','_')

        #The path to copy the zip file to
        path = os.path.join(target,dirname)

        #path to the original zip file
        zippath = os.path.join(gamesdir,n)

        #path to copied zip file
        czippath = os.path.join(path,n)
        new_czippath = os.path.join(path,dirname+".7z")

        #path to delete once unzipped
        delpath = os.path.join(target,dirname)
        delpath2 = os.path.join(delpath,dirname+".7z")

        if(os.path.isdir(path)):
            print('The path exists, %s is multi-disk.'%(n))

            try:
                print("Coping %s to %s"%(n,path))
                #copy the zip file to the external HD
                shutil.copy(zippath,path)
            except Exception as e:
                print(e)

            try:
                print("Renameing file")
                #rename the zipfile to the clean name
                os.rename(czippath,new_czippath)
            except Exception as e:
                print(e)

            try:
                print("Unzipping %s"%(new_czippath))
                arg = '-o%s'%path
                subprocess.call(['7z','e','-spf',new_czippath,arg])
            except Exception as e:
                print(e)

            try:
                #delete the old zip remnent
                os.remove(delpath2)
            except Exception as e:
                print(e)
        else:
            print("Making new directory path %s."%(path))

            try:
                print("Makeing %s."%(path))
                os.mkdir(path)
            except Exception as e:
                print(e)

            try:
                print("Coping %s to %s"%(n,path))
                #copy the zip file to the external HD
                shutil.copy(zippath,path)
            except Exception as e:
                print(e)

            try:
                print("Renameing file")
                #rename the zipfile to the clean name
                os.rename(czippath,new_czippath)
            except Exception as e:
                print(e)

            try:
                print("Unzipping %s"%(new_czippath))
                arg = '-o%s'%path
                subprocess.call(['7z','e','-spf',new_czippath,arg])
            except Exception as e:
                print(e)

            try:
                #delete the old zip remnent
                os.remove(delpath2)
            except Exception as e:
                print(e)
             
    time.sleep(2)