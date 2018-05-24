# coding:utf-8

from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import glob
import datetime
import time

import openslide
from skimage import io
import numpy as np
import sys
from PIL import Image

from MysqlTool import MysqlTool
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)


ALLOWED_EXTENSIONS = set(['svs', 'tif', 'ndpi', 'vms', 'vmu', 'scn', 'mrxs', 'tiff', 'svslide', "bif"])

UPLOAD_PATH = 'static/files'
THUMB_PATH = 'static/files/thumbs'
DOWNLOAD_PATH = 'static/files'

PATTERN = '*'

DB_NAME = 'histoqc'
DB_IP = 'localhost'
DB_PORT = 3306
DB_USER = 'ren.zuo'
DB_PASSWORD = 'ZQTTzr1995'
DB_TABLE = 'file'


def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process(filename, metadata):
	file_path = os.path.join(UPLOAD_PATH, filename)
	parsed_file = openslide.OpenSlide(file_path)
	thumb = np.array(parsed_file.get_thumbnail((100, 100)))
	io.imsave(os.path.join(THUMB_PATH, filename[:-4]+'.png'), thumb)
	[width, height] = parsed_file.dimensions
	fsize = os.path.getsize(file_path)
	fsize = round(fsize / float(1024 * 1024 * 1024), 2)

	Url = filename[:-4]+'.png'
	FileName = filename
	UploadDate = datetime.date.today().strftime("%Y%m%d")
	UploaderContactInfo = metadata.get('Email')
	TissueType = metadata.get('Tissue')
	SlideCreationDate = metadata.get('date')
	BaseMagnification = metadata.get('magnification')
	ArtifactsTypes = metadata.get('Artifacts')
	StainType = metadata.get('Stain')
	Comments =  metadata.get('Comments')
	ImageSizeInPixels = str(height)+'x'+str(width)
	ImageSizeInGB = fsize
	FileType = os.path.splitext(filename)[1]
	Scanner = metadata.get('Scanner')
	PreparationType = metadata.get('Preparation')
	SpecimenType = metadata.get('Specimen')
	mysql_tool.insert(DB_TABLE, [Url, FileName, UploadDate, UploaderContactInfo, TissueType, SlideCreationDate, BaseMagnification, ArtifactsTypes,
			   StainType, Comments, ImageSizeInPixels, ImageSizeInGB, FileType, Scanner, PreparationType, SpecimenType])


app = Flask(__name__)
mysql_tool = MysqlTool(DB_NAME, DB_IP, DB_PORT, DB_USER, DB_PASSWORD)
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/')
def histoqc():
	return render_template('histoqc.html')


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
	if request.method == 'POST':
		if 'file' not in request.files:
			return jsonify({'code': -1, 'filename': '', 'msg': 'No file part.'})
		
		fileList = request.files.getlist('file')
		metadata = request.form
		for file in fileList:
			if file.filename == '':
				return jsonify({'code': -1, 'filename': '', 'msg': 'No selected file.'})
			else:
				try:
					origin_file_name = file.filename
					filename = origin_file_name

					if not os.path.exists(UPLOAD_PATH):
						os.makedirs(UPLOAD_PATH)

					file.save(os.path.join(UPLOAD_PATH, filename))
					process(filename, metadata)

				except Exception as e:
					return jsonify({'code': -1, 'filename': filename, 'msg': 'Error occurred: %s' % e})

		return redirect('/gallery')
	else:
		return render_template('upload.html')


@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
	return send_from_directory(DOWNLOAD_PATH, filename, as_attachment=True)


@app.route('/gallery')
def gallery():
	fileList = mysql_tool.selectAll(DB_TABLE)
	return render_template('gallery.html', files=fileList)


if __name__ == '__main__':
	app.run(
		host = '0.0.0.0',
		port = 15000,
		debug = True
	)
