#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, send_file
import pymysql.cursors
import time
import os
import pandas as pd
import numpy as np





#Initialize the app from Flask
app = Flask(__name__)
IMAGES_DIR = os.path.join(os.getcwd(), "images")
print(IMAGES_DIR)

#Configure MySQL
# conn = pymysql.connect(host='localhost',
#                        port = 8889,
#                        user='root',
#                        password='root',
#                        db='Project_real',
#                        charset='utf8mb4',
#                        cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

#Authenticates the login




@app.route("/upload", methods=["GET"])
def upload():
    return render_template("upload.html")


@app.route("/uploadImage", methods=["POST"])
def upload_image():
    if request.files:
        image_file = request.files.get("imageToUpload")
        caption = request.form["caption"]
        username = session["username"]
        allFollowers = request.form["allFollowers"]
        df = pd.read_csv(image_file)
        print(df.head(5))
        image_name = image_file.filename
        print(image_name)
        filepath = os.path.join(IMAGES_DIR, image_name)
        image_file.save(filepath)
        print(image_file)
        print(username)
        print("caption")
        print(caption)
        print(allFollowers)
        return redirect(url_for('home'))

        # if allFollowers == "0":
        #     query = 'SELECT groupName FROM CloseFriendGroup WHERE groupOwner = %s'
        #     cursor.execute(query, (username))
        #     conn.commit()
        #     data_group = cursor.fetchall()
        #
        #     if data_group:  # check if the user has at least one closefriend group so he can insert private photo
        #         # insert the photo
        #         print("enter data_group")
        #         image_name = image_file.filename

        #

        #
        #         cursor = conn.cursor()
        #         query = "INSERT INTO photo VALUES(Null, %s, %s, %s, %s, %s)"
        #
        #         cursor.execute(query, (username, time.strftime('%Y-%m-%d %H:%M:%S'), image_name, caption, int(allFollowers)))
        #
        #         conn.commit()
        #
        #         # select the photo id just inserted into DB which is not shared
        #         query = 'SELECT DISTINCT photoID FROM Photo AS p WHERE p.allFollowers = %s AND p.photoID NOT IN (SELECT photoID from Photo NATURAL JOIN Share WHERE Photo.allFollowers = %s);'
        #         cursor.execute(query, (0, 0))
        #         data = cursor.fetchall()
        #
        #         photoId = data[0]["photoID"]
        #         print("photo id")
        #         print(photoId)
        #
        #         conn.commit()
        #
        #         # task xiewy: need to add error here no closefriendgroup
        #
        #         cursor.close()
    #             return render_template("sharewith.html", closeFriendsGroup=data_group, photoId=photoId)
    #
    #         else:
    #             # if the user does not have any closefriend group
    #             # bring him to the post page
    #             # need at least one closefriend group
    #             # returns an error message to the html page
    #             session["username"] = username
    #             error = 'should have at least one close friends to post a private photo'
    #             # return redirect(url_for('home',error = error))
    #             return render_template("home.html", username=username, error=error)
    #     else:
    #         image_name = image_file.filename
    #         filepath = os.path.join(IMAGES_DIR, image_name)
    #
    #         image_file.save(filepath)
    #
    #         cursor = conn.cursor();
    #         query = "INSERT INTO photo VALUES(Null, %s, %s, %s, %s, %s)"
    #
    #         cursor.execute(query, (username, time.strftime('%Y-%m-%d %H:%M:%S'), image_name, caption, int(allFollowers)))
    #         conn.commit()
    #         cursor.close()
    #
    # return redirect(url_for('home'))
    #
    #
    #
    #
    #     image_name = image_file.filename
    #     filepath = os.path.join(IMAGES_DIR, image_name)
    #     image_file.save(filepath)
    #     cursor = conn.cursor();
    #     query = "INSERT INTO photo (timestamp, filePath, caption, username) VALUES (%s, %s, %s, %s)"
    #     cursor.execute(query, (time.strftime('%Y-%m-%d %H:%M:%S'), image_name, caption))
    #     conn.commit()
    #
    #     message = "Image has been successfully uploaded."
    #     return render_template("upload.html", message=message)
    # else:
    #     message = "Failed to upload image."
    #     return render_template("upload.html", message=message)

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run()



# SELECT Liked.photoID, COUNT(Liked.photoID) AS likes FROM Photo LEFT JOIN Liked USING(photoID) JOIN Person ON photo.photoOwner = person.username WHERE
# isPrivate = 0 OR Liked.username = 'zy123' OR Liked.username IN (SELECT groupOwner FROM belong NATURAL JOIN
# closefriendgroup WHERE username = 'zy123' UNION SELECT followeeUsername FROM follow WHERE
# followerUsername = 'zy123' AND acceptedfollow = 1 AND allFollowers = 1) GROUP BY photoID