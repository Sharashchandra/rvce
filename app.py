from flask import Flask, render_template,url_for,request,session,redirect
from hashlib import sha256
from pymongo import MongoClient
app=Flask(__name__)
app.config['SECRET_KEY']=b'N\x83Y\x99\x04\xc9\xcfI\xb7\xfc\xce\xd1\xcf\x01\xa8\xccr\xbb&\x1b\x11\xac\xc7V'

#Configuring mongodb
client = MongoClient()
db = client['rvce']
users = db.users
db_entries = {"name" : "", "email" : "", "password" : "", "category" : "", "entity_name" : "", "entity_location" : "", "capacity" : 0}

visit = False

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/list_banks")
def list_banks():
    return render_template('list_banks.html')


@app.route("/list_rest")
def list_rest():
    return render_template('list_rest.html')

@app.route("/list_govt")
def list_govt():
    return render_template('list_govt.html')   

@app.route("/details")
def details():
    return render_template('details.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        db_entries["name"] = request.form['Name']
        db_entries["email"] = request.form['email']
        db_entries["password"] = sha256(request.form['pwd'].encode()).hexdigest()
        users.insert_one(db_entries)
        return redirect(url_for('signin'))
    return render_template("signup.html")


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        emailin = request.form['email']
        passwordin = request.form['password']
        result = users.find_one({"email" : emailin})
        if sha256(passwordin.encode()).hexdigest() == result['password']:
            return redirect(url_for('addowner'))
        return render_template('signin.html')
    return render_template("signin.html")

@app.route("/addowner", methods=['GET', 'POST'])
def addowner():
    visit = True
    if request.method == 'POST':
        entity_name = request.form['Entity_Name']
        location = request.form['Location']
        capacity = request.form['Capacity']
        category = request.form['Category']
        return redirect(url_for("/addowner"))
    return render_template("owner_form.html", visit=visit)

@app.route("/final")
def final():
    visit = True

    #!/usr/bin/env python
    # coding: utf-8

    # In[1]:


    import numpy as np
    import tensorflow as tf
    import cv2
    import matplotlib.pyplot as plt
    from time import sleep
    import time
    import subprocess as sp
    get_ipython().run_line_magic('matplotlib', 'notebook')


    # In[28]:


    tf.__version__


    # In[29]:


    mpath = '/home/manur/Downloads/faster_rcnn_inception_v2_coco_2018_01_28/'


    # In[30]:


    video = cv2.VideoCapture('/home/manur/TownCentreXVID.avi')


    # In[31]:


    fig = plt.figure()
    ax = fig.add_subplot(111)

    plt.ion()

    fig.show()
    fig.canvas.draw()


    # In[32]:


    xdata=[0]
    ydata=[0]
    def plot(value):
        xdata.append(xdata[-1]+1)
        ydata.append(value)
        ax.clear()
        ax.plot(xdata,ydata)
        fig.canvas.draw()
        time.sleep(0.1)


    # In[ ]:


    def process_output(boxes, scores, classes, num, img):
        bl = []
        for i in range(boxes.shape[1]):
            bl.append([boxes[0,i,0]*720,boxes[0,i,1]*1280,boxes[0,i,2]*720,boxes[0,i,3]*1280])
        scores = scores[0].tolist()
        classes = [int(x) for x in classes[0].tolist()]
        num = int(num[0])
        count = 0
        hm = []
        for i in range(len(bl)):
                if classes[i] == 1 and scores[i] > 0.6:
                    count += 1
                    box = bl[i]
                    hm.append(bl[i])
                    cv2.rectangle(img,(int(box[1]),int(box[0])),(int(box[3]),int(box[2])),(255,0,0),2)
        plot(count)
        sp.call("bash /home/manur/Downloads/query.sh {}".format(str(count)))
        return img



    # In[ ]:


    sess = tf.Session()
    graph = tf.get_default_graph()

    with graph.as_default():
        with sess.as_default():
            saver = tf.train.import_meta_graph(mpath + 'model.ckpt.meta')
            saver.restore(sess,mpath + 'model.ckpt')
            sess.run(tf.global_variables_initializer())
            image_tensor = graph.get_tensor_by_name('image_tensor:0')
            detection_boxes = graph.get_tensor_by_name('detection_boxes:0')
            detection_scores = graph.get_tensor_by_name('detection_scores:0')
            detection_classes = graph.get_tensor_by_name('detection_classes:0')
            num_detections = graph.get_tensor_by_name('num_detections:0')

            r, img = video.read()
            i =0
            while(1):

                i = i+1
                img = cv2.resize(img, (1280, 720))
                fd = {image_tensor:np.expand_dims(img, axis=0)}
                (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores, detection_classes, num_detections], feed_dict=fd)
                cv2.imshow("preview",process_output(boxes, scores, classes, num, img))
                key = cv2.waitKey(1)
                if key & 0xFF == ord('q'):
                    break
                r,img = video.read()


    # In[ ]:




    return render_template("final.html")

@app.errorhandler(404)
def not_found():
    return render_template('404.html')

if __name__=='__main__':
    app.run(debug=True)
