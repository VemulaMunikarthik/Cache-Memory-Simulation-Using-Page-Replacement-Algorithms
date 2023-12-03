from flask import Flask,session,render_template,request,redirect,g,url_for,jsonify
from youtubesearchpython import VideosSearch
from pytube import YouTube
import os
import shutil
import time

app = Flask(__name__)
app.secret_key = 'gorilla'
ytname=''
vdo_list =[]

def move_file(source_folder, destination_folder, file_name):
    source_path = os.path.join(source_folder, file_name)
    destination_path = os.path.join(destination_folder, file_name)

    try:
        os.rename(source_path, destination_path)
        print(f"File '{file_name}' moved successfully from '{source_folder}' to '{destination_folder}'.")
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found in '{source_folder}'.")
    except Exception as e:
        print(f"Error: {e}")

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        vdoname = request.form['userinput']
        algo = request.form['sct']
        start_time = time.time()
        if vdoname in vdo_list:
            
            vdo_list.remove(vdoname)
            vdo_list.append(vdoname)
            ytname = vdoname+'.mp4'
        else:
            ytname = vdoname+'.mp4'
            if len(vdo_list) < 3:
                vdo_list.append(vdoname)
            else:
                    if algo:
                        out =vdo_list.pop(0)
                        print(out)
                        vdo_list.append(vdoname)
            videosSearch = VideosSearch(vdoname, limit=2)
            results = videosSearch.result()
            video_links = []
            for result in results['result']:
                video_links.append(result['link'])
            link = video_links[0]

            yt = YouTube(link)
            video_stream = yt.streams.get_lowest_resolution()
            static_folder = os.path.join(os.getcwd(), 'static')
            ytname = os.path.join(static_folder, vdoname + '.mp4')
            ytname = vdoname+'.mp4'
            video_stream.download(filename=ytname)
            # ytname = vdoname+'.mp4'
            # video_stream.download(filename= ytname)
            print("Video downloaded")
            source_folder = '"C:\Users\muni karthik\Desktop\osproj"'
            destination_folder = '"C:\Users\muni karthik\Desktop\osproj"/static'
            file_name = ytname
            move_file(source_folder, destination_folder, file_name)
        end_time = time.time()
        elapsed = end_time - start_time
        return render_template('cache.html',ytname=ytname,elapsed = elapsed)
    return render_template('index.html')

@app.route('/cache',methods=['GET','POST'])
def cache():
    return render_template('cache.html')

if __name__ == '__main__':
    app.run(debug=True)