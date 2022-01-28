from flask import Flask, render_template, Response, request, jsonify
import werkzeug
import os, shutil
import subprocess
import numpy as np
image_path = ""
image_counter = 0
takethis = "UTKU"
app = Flask(__name__)
inProcess = False
timestamps = []
name = "uploaded"

@app.route('/', methods=['GET','POST'])
def index():
    return "rPPG flask server connected"

@app.route('/test', methods=['GET'])
def test():
    return takethis

@app.route('/clean', methods=['POST'])
def clean_directory():
    cleanse_uploaded_directory()
    cleanse_results_directory()
    global image_counter
    image_counter = 0
    return "cleaned successfully"

@app.route('/rppg', methods=['POST'])
def get_rppg_prediction():
    global timestamps
    time = request.form['timestamp']
    print('timestamp is ' + time)
    timestamps += [time]

    global inProcess
    if image_counter > 50 and inProcess is False:
        inProcess = True
        write_time_stamps()
        subprocess.run(["python3", "main.py"])
        inProcess = False
        cleanse_uploaded_directory()
        results = get_results()
        print("RETURNING " + results)
        cleanse_results_directory()
        return results
    else:
        for key in request.files:
            read_and_save_file(key)
    return "Calculating..."

@app.route('/get_result', methods=['GET'])
def get_results():
    try:
        Data = np.genfromtxt("results/results.txt", dtype=float,encoding=None, delimiter=",")
    except:
        print("RESULTS TXT IS NOT WRITTEN")
        return "Pulse rate could not measured"
    (unique, counts) = np.unique(Data, return_counts=True)
    frequencies = np.asarray((unique, counts)).T
    # Sort 2D numpy array by 2nd Column
    sorted_freqs = frequencies[frequencies[:,1].argsort()]
    sorted_freqs = sorted_freqs.astype(int)
    try:
        most_probable_bpm = sorted_freqs[frequencies.shape[0] - 1][0]
        second_probable_bpm = sorted_freqs[frequencies.shape[0] - 2][0]
    except:
        print("RESULTS TXT IS EMPTY")
        return "Pulse rate could not measured"
    estimation = (most_probable_bpm + second_probable_bpm) / 2
    print('--SORTED--')
    print(sorted_freqs)
    den = 0
    nom = 0
    for i in range(sorted_freqs.shape[0]):
        den += sorted_freqs[i][0]
        nom += sorted_freqs[i][1] * sorted_freqs[i][0]
    #print('den' + str(den))
    #print('nom' + str(nom))
    #estimation = int(nom/den)
    return "Pulse rate is " + str(estimation)

def write_time_stamps():
    global timestamps
    f = open(f"{name}/timestamps.txt","w")
    f.write(",".join(timestamps))
    f.close()

def read_and_save_file(file_key):
    global image_counter
    imagefile = request.files[file_key]
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    global image_path 
    image_path = "uploaded/" + filename
    imagefile.save('uploaded/' + str(image_counter) + ".png")  # save file to uploaded folder
    image_counter = image_counter + 1
    print("image counter " + str(image_counter))

def cleanse_uploaded_directory():
    folder = 'uploaded'
    global image_counter
    image_counter = 0
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def cleanse_results_directory():
    folder = 'results'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == '__main__':
    cleanse_uploaded_directory()
    app.run(host='0.0.0.0', port='8080', debug=True)