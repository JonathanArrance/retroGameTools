import multiprocessing
import glob
import os
import shutil
import py7zr
import re
import subprocess

#The source where the compressed files live - full path to direcotry
SOURCE_DIR='/mnt/'

#The directory to decompress the 7zip file to, temporary local storage
DECOMPRESS_DIR='/ps2'

#The destination directory of the iso can be the same as the decompression directory
DEST='/'

#how many files to decompress at the same time
OPERATORS=3

def decompressor(file_path):
    #decompress the 7zip file and place it in the DECOMPRESS_DIR
    #check if it is and iso or a bin/cue - convert if need be
    #copy iso to final location
    #clean up

    continue_flag = True
    #the file_path = /yo/yo2/yo3/file.7z
    filesplit = str(file_path).split('/')

    try:
        unzip = py7zr.SevenZipFile(file_path, mode='r')
        unzip.extractall(path=f"{DECOMPRESS_DIR}")
        unzip.close()
    except Exception as e:
        print(f"Could not extract {file_path}: {e}")
        continue_flag = False

    if continue_flag == True:
        listings = os.listdir(f"{DECOMPRESS_DIR}+'/'+{filesplit[-1][:-3]}")
        for l in listings:
            #look at the file and see if it is an iso
            iso = re.search("\.iso$", l)
            cue = re.search("\.cue$", l)
            #Check the file size and copy the file to the dest dir
            if iso:
                copy_file(l,filesplit)
                #check the file size get megabytes
                #mb = os.path.getsize(f"{DECOMPRESS_DIR}+'/'+{filesplit[-1][:-3]}+'/'+{l}") / (1024 * 1024)
                #if mb >= 650:
                #    dst = DEST + '/DVD/'
                #    #copy to the DVD directory
                #    shutil.copy(l, dst)
                #else:
                #    dst = DEST + '/CD/'
                #    #copy to the CD directory
                #    shutil.copy(l, dst)
            elif cue:
                subprocess.run(["bin2iso", f"{l}"])
                new_iso = l[:-4]
                copy_file(new_iso+".iso",filesplit)
            else:
                print('No supported file type found.')
            
            #remove the decompressed file after it has been moved
            os.rmdir(f"{DECOMPRESS_DIR}+'/'+{filesplit[-1][:-3]}")


def copy_file(iso,filesplit):
    #check the file size get megabytes
    mb = os.path.getsize(f"{DECOMPRESS_DIR}+'/'+{filesplit[-1][:-3]}+'/'+{iso}") / (1024 * 1024)
    if mb >= 650:
        dst = DEST + '/DVD/'
        #copy to the DVD directory
        shutil.move(iso, dst)
    else:
        dst = DEST + '/CD/'
        #copy to the CD directory
        shutil.move(iso, dst)

def mulitiprocess_worker(self,zip_paths):
        """
        DESC: Start a multi processing job to build out the uber meter data.
        INPUT: csv_paths - array of inf host path csvs that will be processed.
        OUTPUT:
        NOTES:
        """

        #break chunk up items
        chunks = [zip_paths[x:x+OPERATORS] for x in range(0, len(zip_paths), OPERATORS)]

        #run through the chunks and process the csv file
        for chunk in chunks:
            print(f"Decompressiing the following {chunk}")
            process = [multiprocessing.Process(target=self.decompressor, args=(zip_path,)) for zip_path in chunk]

            for p in process:
                p.start()

            for p in process:
                p.join()

def main():
    #check if our directories exsis
    if os.path.isdir(DEST):
        print('Destination directory exsists')
    else:
        raise('Destination directory does not exsist')

    if os.path.isdir(SOURCE_DIR):
        print('Source directory exsists')
    else:
        raise('Source directory does not exsist')
    
    if os.path.isdir(DECOMPRESS_DIR):
        print('Decompression directory exsists')
    else:
        raise('Decompression directory does not exsist')

    #check if the CD and DVD directories exsist
    #if not make them
    if os.path.isdir(DEST+'/DVD/') is False:
        os.mkdir(DEST+'/DVD/')
    
    if os.path.isdir(DEST+'/CD/') is False:
        os.mkdir(DEST+'/CD/')

    #list the files in the
    mulitiprocess_worker(glob.glob(f"{SOURCE_DIR}/*.7z"))

if __name__ == '__main__':
    main()