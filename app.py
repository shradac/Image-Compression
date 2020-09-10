import os
import sys
import imgtotxt
import txttoimg
from flask import Flask,render_template,request,redirect,send_from_directory,make_response

app=Flask(__name__)
s=dict()

@app.route('/',methods=['GET','POST'])
def home():
	return render_template('home.html',u="Upload Image",c="COMPRESS!",ul='/compressed')

@app.route('/uploaded', methods = ['GET', 'POST'])
def upload_file():
	if request.method=='POST':
		f = request.files['fileToUpload']
		imgname=f.filename
		f.save(imgname)
		imgtotxt.imgtotxt(imgname)
		return render_template('home.html',u="Image Uploaded!",l="Upload Text")

@app.route('/compressed',methods=['GET','POST'])
def compress():
	if request.method=='POST':
		os.system('gcc huffman.c')
		v=os.popen('./a.out')
		v=v.read().split('\n')
		v=v[:len(v)-1]
		keys,data=[int(i.split(': ')[0]) for i in v],[i.split(': ')[1] for i in v]
		global s
		s=dict(zip(keys,data))
		dtbw=[]
		with open('test1.txt') as f:
			for i in f:
				try:
					dtbw.append(s[int(i)])
				except:
					dtbw.append(i)
		dtbw=[str(i)+'\n' for i in dtbw]
		open('compressed.txt','w').writelines(dtbw)
		response=make_response(send_from_directory('/home/karthik/image-compression','compressed.txt'))
		response.headers["Content-Disposition"]="attachment; filename=compressed.txt"
		#os.system('rm compressed.txt')
		return response 
		
	

@app.route('/decompressed',methods=['GET','POST'])
def decompress():
	if request.method=='POST':
		global s
		d=[]
		with open('compressed.txt','r') as f:
			l=[]
			f=f.read().split('\n')
			f=f[:len(f)-1]
			l,size=[i for i in f[:len(f)-1]],f[-1:][0]
			for i in l:
				for key,value in s.items():
					if value==i:
						d.append(key)
			d=[str(i)+'\n' for i in d]
			d.append(str(size))
			open('decompressed.txt','w').writelines(d)
			txttoimg.txttoimg('decompressed.txt')
			#response=make_response(send_from_directory('/home/karthik/image-compression','test.jpg'))
			response=make_response(send_from_directory('/home/karthik/image-compression','pic.jpg'))
			response=make_response(render_template('home.html'))
			response.headers["Content-Disposition"]="attachment; filename=compressed_img.jpeg"
			return response


if __name__=='__main__':
	app.run(debug=True)