import hashlib
import subprocess
import time
from os import path, walk
import conf

from pandas._libs import json

file_existence = path.exists('Dvcfile')

data_Conf_file  = conf.dataConf_path
code_conf_file  = conf.codeConf_path
data_dir_path = conf.data_path
code_dir_path = conf.code_path

files = []
subdirs = []

def get_checksum(files,path):
    checksum_lst = []
    for file in files:
        file_path = path +'/'+file

        hasher_object = hashlib.md5()
        with open(file_path,'rb') as open_file:
            content = open_file.read()
            hasher_object.update(content)
        checksum_lst.append(hasher_object.hexdigest())
    zip_object = zip(files , checksum_lst)

    return dict(zip_object)

def update_dataConffile(dict):
    with open(data_Conf_file, 'w+') as outfile:
        json.dump(dict, outfile)

def update_codeConffile(dict):
    with open(code_conf_file, 'w+') as outfile:
        json.dump(dict, outfile)

def dir_structure(dir_path):
    for root, dirs, filenames in walk(dir_path):
        for subdir in dirs:
            subdirs.append(path.relpath(path.join(root, subdir), dir_path))

        for f in filenames:
            files.append(path.relpath(path.join(root, f), dir_path))
    return files

def gitCommands():

    git_status = 'git status -s'
    status = subprocess.call(git_status, shell=True)
    print('returned value:', status)

    git_add = 'git add .'
    add = subprocess.call(git_add, shell=True)
    print('returned value:', add)

    git_commit = 'git commit -m "updated" .'
    commit = subprocess.call(git_commit, shell=True)
    print('returned value:', commit)

    git_push = 'git push origin master'
    push = subprocess.call(git_push, shell=True)
    print('returned value:', push)


if not file_existence:

    commands = ['git init',
                'dvc init',
                'dvc add data',
                'mkdir output',
                'dvc run -d code/pytrain.py -d data -d data.dvc -o output/model.pkl python code/pytrain.py',
                'mkdir prediction',
                'dvc run -d output/model.pkl  -o prediction/eval.txt -o prediction/metrics.json python code/pyprediction.py',
                'dvc run -f Dvcfile  -d code -d output/model.pkl -d prediction/eval.txt -d eval.txt.dvc -o output/1 -o output/2 python code/pyinfer.py',
                'dvc pipeline show --ascii',
				'dvc remote add -d myremote s3://dvcdataaltran/sourcedata/',
                'echo  conf.py>> .gitignore',

                ]
    p = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for cmd in commands:
        p.stdin.write(cmd + "\n")
    p.stdin.close()
    print(p.stdout.read())

    git_remote = 'git remote add origin https://github.com/m-niharika/demo.git'
    remote = subprocess.call(git_remote, shell=True)

    gitCommands()
    data_files = dir_structure(data_dir_path)
    data_dict = get_checksum(data_files,data_dir_path)
    update_dataConffile(data_dict)
    files=[]

    code_files = dir_structure(code_dir_path)
    code_dict = get_checksum(code_files, code_dir_path)
    update_codeConffile(code_dict)

else:
    updated_data_files = dir_structure(data_dir_path)
    updated_data_dict = get_checksum(updated_data_files, data_dir_path)
    files = []

    with open(data_Conf_file, 'rb') as json_file:
        last_data_info = json.load(json_file)

    for key in updated_data_dict:
        if key in last_data_info:
            if(updated_data_dict[key]!=last_data_info[key]):
                print("updated----",key,updated_data_dict[key])
                print("last-----",key,last_data_info[key])
                update_dataConffile(updated_data_dict)

                commands = ['dvc add data']
                p = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                for cmd in commands:
                    p.stdin.write(cmd + "\n")
                p.stdin.close()
                print(p.stdout.read())
                gitCommands()

    updated_code_files = dir_structure(code_dir_path)
    updated_code_dict = get_checksum(updated_code_files, code_dir_path)

    with open(code_conf_file, 'rb') as json_file:
        last_code_info = json.load(json_file)

    for key in updated_code_dict:
        if key in last_code_info:
            if(updated_code_dict[key]!=last_code_info[key]):
                print("updated----",key,updated_code_dict[key])
                print("last-----",key,last_code_info[key])
                update_codeConffile(updated_code_dict)
                gitCommands()

























