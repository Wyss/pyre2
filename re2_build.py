import os.path
from os.path import join as pjoin
import subprocess
from os import rename, makedirs
import shutil

PACKAGE_PATH =          os.path.abspath(os.path.dirname(__file__))
MODULE_PATH =           pjoin(PACKAGE_PATH, 're2')

RE2_SRC_PATH =          pjoin(PACKAGE_PATH, 're2_cpp')

RE2_INSTALL_PATH = pjoin(MODULE_PATH, 'src', 're2_cpp')

INSTALL_H_FILES = [ "filtered_re2.h",
                    "re2.h",
                    "set.h",
                    "stringpiece.h",
                    "variadic_function.h"]
INSTALL_LIB_FILES = ["libre2.so"]

def re2Clean():
    re2clean = subprocess.Popen(['make clean'], shell=True, 
                               cwd=RE2_SRC_PATH)
    re2clean.wait()
    if os.path.exists(RE2_INSTALL_PATH):
        shutil.rmtree(RE2_INSTALL_PATH)


def re2Build():
    install_include_path = pjoin(RE2_INSTALL_PATH, "include", "re2")
    install_lib_path = pjoin(RE2_INSTALL_PATH, "lib")
    # from http://stackoverflow.com/questions/10021428/macos-how-to-link-a-dynamic-library-with-a-relative-path-using-gcc-ld
    e_cmd = 'make -j4 LDFLAGS="-install_name %s/libre2_dyn.so" obj/so/libre2.so;' % (install_lib_path)    # only build the static libs
    # e_cmd = 'make -j4 obj/libre2.a;'    # only build the static libs
    re2build = subprocess.Popen([e_cmd],
                                shell=True, 
                                cwd=RE2_SRC_PATH)
    re2build.wait()
    # copy files to install
    if not os.path.exists(install_include_path):
        makedirs(install_include_path)
    for f in INSTALL_H_FILES:
        shutil.copyfile(pjoin(RE2_SRC_PATH, "re2", f), 
                        pjoin(install_include_path, f))

    if not os.path.exists(install_lib_path):
        makedirs(install_lib_path)
    for f in INSTALL_LIB_FILES:
        shutil.copyfile(pjoin(RE2_SRC_PATH, "obj", "so", f), 
                        pjoin(install_lib_path, f))

    # rename(pjoin(install_lib_path, 'libre2.a'), 
    #         pjoin(install_lib_path, 'libre2_static.a'))
    rename(pjoin(install_lib_path, 'libre2.so'), 
            pjoin(install_lib_path, 'libre2_dyn.so'))
if __name__ == '__main__':
    re2Clean()
    re2Build()
