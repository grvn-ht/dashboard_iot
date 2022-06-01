import requests
from PIL import Image
import io
import datetime
import mysql.connector
import time

mydb = mysql.connector.connect(
  host="db",
  port=3306,
  user="root",
  password="root",
  database="db",
  auth_plugin="mysql_native_password")

mycursor = mydb.cursor(buffered=True)
mycursor_insert = mydb.cursor(buffered=True)
mycursor_gif = mydb.cursor(buffered=True)

mycursor.execute("SHOW TABLES")

hr = datetime.datetime.now().strftime("%H")
hr = int(hr)

if mycursor.rowcount == 0:
    mycursor.execute("CREATE TABLE placard \
                    (id INT AUTO_INCREMENT PRIMARY KEY, \
                    date TIMESTAMP DEFAULT NOW(), \
                    temperature INT, \
                    humidite INT, photo_url VARCHAR(255))")
    mycursor.close()
else:
    if hr >= 8 or hr <2:

	    response = requests.get("http://192.168.1.68/helloWorld")
	    dic = response.json()
	    te = dic['Temperature']
	    hu = dic['Humidite']

	    requests.get("http://192.168.1.1/capture")
	    time.sleep(5)

	    dat = datetime.datetime.now().strftime("%m.%d.%Y+%H:%M:%S")

	    photo_path = "/photo/"+dat+".jpg"

	    response = requests.get("http://192.168.1.1/saved-photo")
	    byt = response.content
	    image = Image.open(io.BytesIO(byt))
	    image = image.save(photo_path)

	    image2 = Image.open(io.BytesIO(byt))
	    image2 = image2.save("/photo/last_pic.jpg")

	    sql = "INSERT INTO placard (temperature, humidite, photo_url) VALUES (%s, %s, %s)"
	    val = (te, hu, photo_path)

	    mycursor_insert.execute(sql, val)

	    mydb.commit()

	    mycursor_insert.close()

	    sql_gif = "SELECT photo_url from placard where date >= '2022-04-15' ORDER BY date;"
	    mycursor_gif.execute(sql_gif)
	    photo_gif = mycursor_gif.fetchall()
	    if len(photo_gif) > 100:
	        extrait=[]
	        modul = int(len(photo_gif)/100)
	        for i,lll in enumerate(photo_gif):
	            if i%modul == 0:
	                extrait.append(lll[0])
	        gif = []
	        for image in extrait:
	            im = Image.open(image)
	            gif.append(im)

	        gif[0].save('/photo/weed.gif', save_all=True,optimize=False, append_images=gif[1:], loop=0)
	    else:
	        gif = []
	        for image in photo_gif:
	            im = Image.open(image[0])
	            gif.append(im)

	        gif[0].save('/photo/weed.gif', save_all=True,optimize=False, append_images=gif[1:], loop=0)
	    mycursor_gif.close()
