#!/usr/bin/python
# Bronson Mathews 2019
# pip install pyqt5
# https://build-system.fman.io/pyqt5-tutorial

import sys
import subprocess
import os
import shutil
import argparse
import pathlib
import ast
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


config = {}
log_to_file = False



def log(str=''):
    print(str)
    if not log_to_file:
        return

    with open("log.txt", "a") as f:
        f.write(str + '\n')
        f.close()
    return


def parse_enums(data):
	# parse qt enums
	key = 'AcceptMode'
	if (key in data):
		string = data[key].lower()
		if (string == 'acceptopen'):
			data[key] = QFileDialog.AcceptOpen
		elif (string == 'acceptsave'):
			data[key] = QFileDialog.AcceptSave
			
	key = 'DialogLabel'
	if (key in data):
		string = data[key].lower()
		if (string == 'lookin'):
			data[key] = QFileDialog.LookIn
		elif (string == 'filename'):
			data[key] = QFileDialog.FileName
		elif (string == 'filetype'):
			data[key] = QFileDialog.FileType
		elif (string == 'accept'):
			data[key] = QFileDialog.Accept
		elif (string == 'reject'):
			data[key] = QFileDialog.Reject

	key = 'FileMode'
	if (key in data):
		string = data[key].lower()
		if (string == 'anyfile'):
			data[key] = QFileDialog.AnyFile
		elif (string == 'existingfile'):
			data[key] = QFileDialog.ExistingFile
		elif (string == 'directory'):
			data[key] = QFileDialog.Directory
		elif (string == 'existingfiles'):
			data[key] = QFileDialog.ExistingFiles
		elif (string == 'directoryonly'):
			data[key] = QFileDialog.DirectoryOnly

	key = 'ViewMode'
	if (key in data):
		string = data[key].lower()
		if (string == 'detail'):
			data[key] = QFileDialog.Detail
		elif (string == 'list'):
			data[key] = QFileDialog.List

	# options is an array
	key = 'Options'
	if (key in data):
		options = QFileDialog.Options()
		for i in range(0, len(data[key])):
			string = data[key][i]
			if (string == 'showdirsonly'):
				options.setOption(QFileDialog.ShowDirsOnly)
			elif (string == 'dontresolvesymlinks'):
				options.setOption(QFileDialog.DontResolveSymlinks)
			elif (string == 'dontconfirmoverwrite'):
				options.setOption(QFileDialog.DontConfirmOverwrite)
			elif (string == 'dontusenativedialog'):
				options.setOption(QFileDialog.DontUseNativeDialog)
			elif (string == 'readonly'):
				options.setOption(QFileDialog.ReadOnly)
			elif (string == 'hidenamefilterdetails'):
				options.setOption(QFileDialog.HideNameFilterDetails)
			elif (string == 'dontusecustomdirectoryicons'):
				options.setOption(QFileDialog.DontUseCustomDirectoryIcons)

		data[key] = options

	return data


class qt_app(QWidget):
	def __init__(self):
		super().__init__()
		return

	def file_dialog(self, data):
		# setup defaults
		caption = 'Save'
		if ('Caption' in data):
			caption = data['Caption']

		directory = ''
		if ('Directory' in data):
			directory = data['Directory']	

		str_filter = 'All Files (*)'
		if ('Filter' in data):
			str_filter = data['Filter']	

		# init dialog
		dialog = QFileDialog(self, caption, directory, str_filter)

		# dialog options
		if ('Options' in data):
			dialog.setOptions(data['Options'])

		if ('AcceptMode' in data):
			dialog.setAcceptMode(data['AcceptMode'])

		if ('FileMode' in data):
			dialog.setFileMode(data['FileMode'])

		if ('ViewMode' in data):
			dialog.setViewMode(data['ViewMode'])

		if ('DialogLabel' in data):
			dialog.setLabelText(data['DialogLabel'], caption)

		# show and return
		fileNames = []
		if (dialog.exec()):
			fileNames = dialog.selectedFiles()
		return dialog.selectedFiles()



if __name__ == '__main__':
	# https://doc.qt.io/qt-5/qfiledialog.html
	
	if (len(sys.argv) > 1):
		json_string = sys.argv[1]

	
	# example save dialog
	#json_string = "{'AcceptMode':'AcceptSave','Directory':'c:\', 'Caption':'Save', 'Filter':'All Files (*)'}"
	
	# clean json
	data = ast.literal_eval(json_string)
	data = parse_enums(data)

	# qt app
	app = QApplication(sys.argv)
	ex = qt_app()
	out = ex.file_dialog(data)
	log(out)

