import logging
import os
import requests
import shutil
import subprocess
import sys

class Command():
    def execute(self, args):
        logging.getLogger().setLevel(logging.INFO)

        PLATFORM_NAME = os.environ['PLATFORM_NAME']
        SHADER_SDK_BASE_DIR = os.environ['SHADER_SDK_BASE_DIR'].replace("\\", "/")
        CMAKE_EXECUTABLE = os.environ['CMAKE_EXECUTABLE']
        GIT_EXECUTABLE = os.environ['GIT_EXECUTABLE']

        logging.info('Platform: %s' % PLATFORM_NAME)
        logging.info('Beam shader-sdk path: %s' % SHADER_SDK_BASE_DIR)
        logging.info('CMake executable: %s' % CMAKE_EXECUTABLE)
        logging.info('Git executable: %s' % GIT_EXECUTABLE)

        if not [s for s in os.listdir(SHADER_SDK_BASE_DIR) if s.startswith('wasi-sdk')]:
            if PLATFORM_NAME == 'Linux':
                wasi_url = 'https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-12/wasi-sdk-12.0-linux.tar.gz'
            elif PLATFORM_NAME == 'Darwin':
                wasi_url = 'https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-12/wasi-sdk-12.0-macos.tar.gz'
            elif PLATFORM_NAME == 'Windows':
                wasi_url = 'https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-12/wasi-sdk-12.0-mingw.tar.gz'
            else:
                print('ERROR: Unknown system: %s' % PLATFORM_NAME)
                sys.exit(1)

            logging.info('Downloading wasi-sdk from %s' % wasi_url)

            r = requests.get(wasi_url)

            with open("wasi-sdk.tar.gz", "wb") as code:
                code.write(r.content)

            logging.info('Unpacking wasi-sdk to %s' % SHADER_SDK_BASE_DIR)
            shutil.unpack_archive('wasi-sdk.tar.gz', SHADER_SDK_BASE_DIR)

            os.remove('wasi-sdk.tar.gz')

        WASI_PATH = os.path.join(SHADER_SDK_BASE_DIR, [s for s in os.listdir(SHADER_SDK_BASE_DIR) if s.startswith('wasi-sdk')][0]).replace("\\", "/")

        logging.info('WASI path: %s' % WASI_PATH)

        BUILD_PATH = os.path.join(SHADER_SDK_BASE_DIR, 'build').replace("\\", "/")
        HOST_BUILD_PATH = os.path.join(BUILD_PATH, 'host').replace("\\", "/")
        WASI_BUILD_PATH = os.path.join(BUILD_PATH, 'wasi').replace("\\", "/")

        git_submodule_update_cmd = [GIT_EXECUTABLE,
                '-C', SHADER_SDK_BASE_DIR,
                'submodule', 'update',
                '--init']

        cmake_init_cmd = [CMAKE_EXECUTABLE,
                '-DCMAKE_INSTALL_PREFIX=' + SHADER_SDK_BASE_DIR,
                '-S' + SHADER_SDK_BASE_DIR,
                '-B' + HOST_BUILD_PATH]

        cmake_build_cmd = [CMAKE_EXECUTABLE,
                '--build', HOST_BUILD_PATH,
                '--config', 'Release',		
                '--target', 'generate-sid',
                '--parallel'
                ]
        
        cmake_build_debug_cmd = [CMAKE_EXECUTABLE,
                '--build', HOST_BUILD_PATH,
                '--config', 'Debug',		
                '--target', 'bvm',
                '--parallel'
                ]

        cmake_install_cmd = [CMAKE_EXECUTABLE,
                '--install',
                HOST_BUILD_PATH]

        cmake_wasi_cmd = [CMAKE_EXECUTABLE,
                '-G', 'Ninja',
                '-DCMAKE_BUILD_TYPE=Release',
                '-DCMAKE_TOOLCHAIN_FILE=' + os.path.join(WASI_PATH, 'share', 'cmake', 'wasi-sdk.cmake'),
                '-DCMAKE_SYSROOT=' + os.path.join(WASI_PATH, 'share', 'wasi-sysroot'),
                '-DWASI_SDK_PREFIX=' + WASI_PATH,
                '-DCMAKE_CXX_COMPILER_FORCED=True',
                '-DCMAKE_C_COMPILER_FORCED=True',
                '-S' + SHADER_SDK_BASE_DIR,
                '-B' + WASI_BUILD_PATH]

        cmake_build_wasi_cmd = [CMAKE_EXECUTABLE,
                '--build', WASI_BUILD_PATH
                ]

        #try:
            #os.remove(BUILD_PATH)
        #except FileNotFoundError:
        #    pass 

        subprocess.run(git_submodule_update_cmd, check=True)
        subprocess.run(cmake_init_cmd, check=True)
        subprocess.run(cmake_build_cmd, check=True)
        subprocess.run(cmake_install_cmd, check=True)
        subprocess.run(cmake_build_debug_cmd, check=True)

        #os.remove(BUILD_PATH)
        subprocess.run(cmake_wasi_cmd, check=True)
        subprocess.run(cmake_build_wasi_cmd, check=True)

        logging.info('Initialization done!')
