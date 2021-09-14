# -*- coding: utf-8 -*-

"Automatically handle things during building FPGA OS in SD card"

__author__ = 'QidiLiu'

from tkinter import filedialog
from tkinter.messagebox import showinfo
import os
import re

check_flag = True

while check_flag:
    project_dir = filedialog.askdirectory(title='Please select the directory of FPGA project')
    for root, dirs, files in os.walk(project_dir):
        if 'settings.sh' in files:
            check_flag = False
            break
        else:
            showinfo(title='Warning!', message='Wrong directory! Please select the directory of FPGA project that contains "settings.sh".')
            break

os.chdir(project_dir)
os.system('/bin/bash settings.sh')


rtl_bd_dir = project_dir + '/fpga/prj/phasemeter/rtl/BD'
os.system('rm -rf {rtl_bd_dir}/*'.format(rtl_bd_dir=rtl_bd_dir))

build_src_dir = project_dir + '/fpga/prj/phasemeter/project/redpitaya.srcs/sources_1/bd/'
os.chdir(build_src_dir)
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith('_bd.tcl'):
            os.system('cp {}/{} {}/'.format(root, file, rtl_bd_dir))

os.chdir(rtl_bd_dir)
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith('_bd.tcl'):
            os.rename('{}/{}'.format(root, file), '{}/{}.tcl'.format(root, file.split("_bd")[0]))

os.system('cp {}/fpga/prj/phasemeter/project/redpitaya.srcs/sources_1/imports/phasemeter/rtl/HDL/RP_user.v {}/fpga/prj/phasemeter/rtl/HDL/'.format(project_dir, project_dir))

for root, dirs, files in os.walk("."):
    for file in files:
        if file == 'filter_1.tcl':
            with open ('{}/{}'.format(root, file), 'r') as f:
                lines = f.readlines()
            with open ('{}/{}'.format(root, file), 'w+') as f:
                for line in lines:
                    text = re.sub('../../../../../../../../../../octave/lowpass_coeff.coe', '../../../../../../coe/lowpass_coeff.coe', line)
                    f.writelines(text)

os.chdir(project_dir)
os.system('make -f Makefile.x86 all')
os.system('make -f Makefile.x86 install')
os.system('make -f Makefile.x86 zip')

showinfo(title='OS build finished!', message='SD-card version of FPGA program was successfully built. Now you should copy all files from "/<project-dir>/build" to "/boot".')

