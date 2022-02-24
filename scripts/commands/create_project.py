import logging
import os
import shutil
import subprocess
import sys
import distutils.dir_util

class Command():
    def execute(self, args):
        PROJECT_NAME = args.project_name
        PROJECT_DIR = os.path.join(os.getcwd(), PROJECT_NAME if args.newdir else '').replace("\\", "/")
        SHADER_SDK_BASE_DIR = os.environ['SHADER_SDK_BASE_DIR'].replace("\\", "/")
        CMAKE_EXECUTABLE = os.environ['CMAKE_EXECUTABLE']

        try:
            src = os.path.join(SHADER_SDK_BASE_DIR, 'scripts', 'template')
            if args.newdir:
                shutil.copytree(src, PROJECT_DIR)
            else:
                distutils.dir_util.copy_tree(src, PROJECT_DIR)
        except FileExistsError:
            logging.error('%s already exists!' % PROJECT_NAME)
            sys.exit(1)

        for subDir, dirs, files in os.walk(PROJECT_DIR):
            for fileName in files:
                if fileName.endswith(('.cpp', '.h', '.txt', '.json')):
                    filePath = os.path.join(subDir, fileName) 
                    with open(filePath, 'r') as f:
                        buf = f.read()
                    with open(filePath, 'w') as f:
                        f.write(buf.replace('%PROJECT_NAME_PLACEHOLDER%', PROJECT_NAME)
                                   .replace('%SHADER_SDK_BASE_DIR%', SHADER_SDK_BASE_DIR))

        logging.info('Shader %s created successfully!' % PROJECT_NAME)

        BUILD_PATH = os.path.join(PROJECT_DIR, 'build', 'wasi').replace("\\", "/")

        cmake_build_cmd = [CMAKE_EXECUTABLE,
                '--build',
                BUILD_PATH]

        cmake_wasi_cmd = [CMAKE_EXECUTABLE,
                '-G','Ninja',
                '-DCMAKE_BUILD_TYPE=Release',
                '-DBEAM_SHADER_SDK=' + os.environ['SHADER_SDK_BASE_DIR'].replace("\\", "/"),
                '-DCMAKE_TOOLCHAIN_FILE=' + os.path.join(os.environ['WASI_PATH'], 'share', 'cmake', 'wasi-sdk.cmake').replace("\\", "/"),
                '-DCMAKE_SYSROOT=' + os.path.join(os.environ['WASI_PATH'], 'share', 'wasi-sysroot').replace("\\", "/"),
                '-DWASI_SDK_PREFIX=' + os.environ['WASI_PATH'].replace("\\", "/"),
                '-DCMAKE_CXX_COMPILER_FORCED=True',
                '-DCMAKE_C_COMPILER_FORCED=True',
                '-S' + PROJECT_DIR,
                '-B' + BUILD_PATH]

        with open(os.open(os.path.join(PROJECT_DIR, 'wasi_init.sh'), os.O_CREAT | os.O_WRONLY, 0o777), 'w') as f:
            f.write('#!/bin/sh\n')
            f.write(' '.join(cmake_wasi_cmd))
        with open(os.open(os.path.join(PROJECT_DIR, 'build.sh'), os.O_CREAT | os.O_WRONLY, 0o777), 'w') as f:
            f.write('#!/bin/sh\n')
            f.write(' '.join(cmake_build_cmd))

        subprocess.run(cmake_wasi_cmd, check=True)
        subprocess.run(cmake_build_cmd, check=True)
