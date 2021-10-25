import logging
import os
import shutil
import subprocess
import sys

class Command():
    def execute(self, args):
        PROJECT_NAME = args.project_name
        SHADER_SDK_BASE_DIR = os.environ['SHADER_SDK_BASE_DIR']
        CMAKE_EXECUTABLE = os.environ['CMAKE_EXECUTABLE']

        try:
            shutil.copytree(os.path.join(SHADER_SDK_BASE_DIR, 'scripts', 'template'), PROJECT_NAME);
        except FileExistsError:
            logging.error('%s already exists!' % PROJECT_NAME)
            sys.exit(1)

        for subDir, dirs, files in os.walk(PROJECT_NAME):
            for fileName in files:
                if fileName.endswith(('.cpp', '.h')):
                    filePath = os.path.join(subDir, fileName) 
                    with open(filePath, 'r') as f:
                        buf = f.read()
                    with open(filePath, 'w') as f:
                        f.write(buf.replace('%PROJECT_NAME_PLACEHOLDER%', PROJECT_NAME))

        logging.info('Shader %s created successfully!' % PROJECT_NAME)

        BUILD_PATH = os.path.join(PROJECT_NAME, 'build', 'wasi').replace("\\", "/")

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
                '-S' + PROJECT_NAME,
                '-B' + BUILD_PATH]

        subprocess.run(cmake_wasi_cmd, check=True)
        subprocess.run(cmake_build_cmd, check=True)
