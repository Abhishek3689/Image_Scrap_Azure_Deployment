from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
import pymongo
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)
import os

app = Flask(__name__)

@app.route("/",methods = ['GET'])
def home_page():
    return render_template('index.html')

@app.route("/image",methods=['POST',"GET"])
def images_result():
    if request.method=='POST':
        try:
            query=request.form['image'].replace(" ","")
            save_dir="Images/"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
            
            response=requests.get(f"https://www.google.com/search?q={query}&sxsrf=APwXEdffEyBKzPpnm71RJXCDWMjeYqfbMQ:1681196137244&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiUhbvUn6H-AhVlTmwGHfzHBegQ_AUoAnoECAEQBA&biw=1821&bih=789&dpr=0.75")
            
            soup=bs(response.content,'html.parser')
            
            images_tags=soup.find_all('img')
            
            del images_tags[0]
            
            image_data_mongo=[]
            
            image_data_mongo=[]
            for i in images_tags:
                img_url=i['src']
                img_data=requests.get(img_url).content
                mydict={'Index':img_url,'Image':img_data}
                image_data_mongo.append(mydict)
                with open(os.path.join(save_dir,f"{query}_{images_tags.index(i)}.jpg"),"wb") as f:
                    f.write(img_data)

            client = pymongo.MongoClient("mongodb+srv://abhinishad:abhinishad@mycluster.297r1oi.mongodb.net/?retryWrites=true&w=majority")
            db=client['image_scrap_db']
            collect=db['image_data']
            collect.insert_many(image_data_mongo)

            return "Image Loaded"
        except Exception as e:
            logging.info(e)
            return 'something is wrong'
    else:

        return render_template('index.html')

    #return render_template('results.html')

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080)
