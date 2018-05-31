# coding:utf-8

import os
import datetime
import sys
import numpy as np
from skimage import io
from PIL import Image

from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename

import openslide

from lib.MysqlTool import MysqlTool
from lib.upload_file import uploadfile

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)

app = Flask(__name__)
app.config["SECRET_KEY"] = 'Youneverknowqc'
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path,'static/data/')
app.config["THUMBNAIL_FOLDER"] = os.path.join(app.root_path,'static/data/thumbnail/')

ALLOWED_EXTENSIONS = set(['svs', 'tif', 'ndpi', 'vms', 'vmu', 'scn', 'mrxs', 'tiff', 'svslide', "bif"])

DB_NAME = 'histoqc'
DB_IP = 'localhost'
DB_PORT = 3306
DB_USER = 'ren.zuo'
DB_PASSWORD = 'ZQTTzr1995'
DB_TABLE = 'file'

mysql_db = MysqlTool(DB_NAME, DB_IP, DB_PORT, DB_USER, DB_PASSWORD)


if not os.path.exists(app.config["UPLOAD_FOLDER"]):
	os.makedirs(app.config["UPLOAD_FOLDER"])
if not os.path.exists(app.config["THUMBNAIL_FOLDER"]):
	os.makedirs(app.config["THUMBNAIL_FOLDER"])


def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gen_file_name(filename):
	i = 1
	while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
		name, extension = os.path.splitext(filename)
		filename = '%s_%s%s' % (name, str(i), extension)
		i += 1
	return filename


def process(filename, metadata, mimetype):
	file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
	name, extension = os.path.splitext(filename)
	thumbname = '%s%s' % (name, '.png')
	thumb_path = os.path.join(app.config["THUMBNAIL_FOLDER"], thumbname)

	parsed_file = openslide.OpenSlide(file_path)
	thumb = np.array(parsed_file.get_thumbnail((100, 100)))
	io.imsave(thumb_path, thumb)

	width, height = parsed_file.dimensions
	fsize = os.path.getsize(file_path)
	fsize = round(fsize / float(1024 * 1024 * 1024), 2)

	Url = thumbname
	FileName = filename
	UploadDate = datetime.date.today().strftime("%m/%d/%Y")
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

	mysql_db.insert(DB_TABLE, [Url, FileName, UploadDate, UploaderContactInfo, TissueType, SlideCreationDate, BaseMagnification, ArtifactsTypes,
			   StainType, Comments, ImageSizeInPixels, ImageSizeInGB, FileType, Scanner, PreparationType, SpecimenType])

	return uploadfile(name=filename, type=mimetype, size=ImageSizeInGB)


@app.route('/')
def histoqc():
	return redirect('/gallery')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
	if request.method == 'POST':
		if 'file' not in request.files:
			return jsonify({'code': -1, 'filename': '', 'msg': 'No file part.'})
		
		curfile = request.files['file']
		metadata = request.form

		if curfile.filename == '':
			return jsonify({'code': -1, 'filename': '', 'msg': 'No selected file.'})

		filename = secure_filename(curfile.filename)
		filename = gen_file_name(filename)
		mimetype = curfile.content_type

		if not allowed_file(curfile.filename):
			result = uploadfile(name=filename, type=mimetype, size=0, not_allowed_msg="File type not allowed")
		else:
			# save file to disk
			curfile.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
			result = process(filename, metadata, mimetype)
		return jsonify({"files": [result.get_file()]})
		# return redirect('/gallery')
	else:
		return render_template('upload.html')


@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
	return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)


@app.route('/gallery')
def gallery():
	fileList = mysql_db.selectAll(DB_TABLE)
	return render_template('gallery.html', files=fileList, thumb_path=app.config["THUMBNAIL_FOLDER"])


@app.route('/about')
def about():
	return render_template('about.html')


if __name__ == '__main__':
	app.run()
#		host = '0.0.0.0',
#		port = 15000,
#		debug = True
#	)
