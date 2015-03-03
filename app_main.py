from flask import Flask
from flask import g
from flask import render_template
from flask import request
import os
from utility.server_info import ServerInfo

app = Flask(__name__)

@app.before_request
def server_info_init():
  g.server_info = ServerInfo.Create()

@app.route('/')
def home_page():
  return render_template('home.html')

@app.route('/about.html')
def about_page():
  return render_template('about.html')

@app.route('/contact_us.html')
def contact_us_page():
  return render_template('contact_us.html')

@app.route('/demo.html')
def demo_page():
  return render_template('demo.html')

@app.route('/faq.html')
def faq_page():
  return render_template('faq.html')

@app.route('/home.html')
def about_page():
  return render_template('home.html')

@app.route('/release.html')
def release_page():
  return render_template('release.html')

# for debugging layout template
@app.route('/layout.html')
def layout_page():
  return render_template('layout.html')

if __name__ == '__main__':
  try:
    app.run(debug=True)
  except KeyboardInterrupt:
    pass
  finally:
    # scan and make the directory tree clean every time 
    for rootdir, subdir, files in os.walk("./"):
      for item in files:
        if item.endswith(".pyc"):
          try:
            os.remove(rootdir + "/" + item)
          except:
            pass
