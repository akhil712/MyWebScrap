from flask import Flask,render_template,request,jsonify,url_for
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def home():
    return render_template("index.html")

@app.route("/process", methods = ['GET','POST'])
def process():
    if request.method == 'POST':
        site = request.form['sitename']
        if site =='flipkart':
            try:
                huntstring = request.form['content']
                hunt_url="https://www.flipkart.com/search?q=" + huntstring.replace(" ","+")
                main_response=uReq(hunt_url)
                main_page = main_response.read()
                main_response.close()
                main_page=bs(main_page,'html.parser')
                product_box = main_page.findAll('div',{'class':'_1AtVbE col-12-12'})
                del(product_box[0:2])
                del(product_box[-4:])
                product_link=product_box[0].find('a',{'class':'_1fQZEK'})['href']
                product_url='https://www.flipkart.com'+product_link
                product_response=uReq(product_url)
                product_page=product_response.read()
                product_response.close()
                product_page=bs(product_page,'html.parser')
                commentboxes = product_page.find_all('div', {'class': "_16PBlm"})
                del(commentboxes[-1])

                filename = huntstring.replace(" ","_") + ".csv"
                fw = open(filename, "a+")
                headers = "Product, Customer Name, Rating, Heading, Comment \n"
                fw.write(headers)

                reviews = []
                for i in commentboxes:
                    try:
                        name = i.find('p',{"class":"_2sc7ZR _2V5EHH"}).text
                    except:
                        logging.info("name")
                    try:
                        comment = i.find('div',{"class":"t-ZTKy"}).div.div.text
                    except:
                        logging.info("comment")
                    try:
                        heading = i.find('p',{"class":"_2-N8zT"}).text
                    except:
                        logging.info("heading")
                    try:
                        rating = i.find('div',{"class":"_3LWZlK"}).text
                    except:
                        logging.info("rating")
                    try:
                        headers = str(huntstring) + ", " + str(name) + ", " + str(rating) + ", " + str(heading) + ", " + str(comment) + "\n"
                        fw.write(headers)
                    except:
                        logging.info("CSV Write Error")
                    
                    newdict = { "Product" : huntstring , "Name" : name , "Rating" : rating , "Heading" : heading , "Comment" : comment}
                    reviews.append(newdict)

                logging.info("My final result logged {}".format(reviews))

                return render_template('result.html', reviews=reviews[0:(len(reviews))])

            except:
                logging.info("Wrong")
                return 'something is wrong'
        
        
        elif site =='amazon':
            try:
                huntstring = request.form['content']
                hunt_url="https://www.amazon.in/s?k=" + huntstring.replace(" ","+")
                main_response=uReq(hunt_url)
                main_page = main_response.read()
                main_response.close()
                main_page=bs(main_page,'html.parser')
                product_box = main_page.findAll('div',{'class':'s-result-item'})
                del(product_box[0])
                product_link=product_box[0].find('a',{'class':'a-link-normal'})['href']
                product_url='https://www.amazon.in'+product_link
                product_response=uReq(product_url)
                product_page=product_response.read()
                product_response.close()
                product_page=bs(product_page,'html.parser')
                commentboxes = product_page.find_all('div', {'class': "a-section review aok-relative"})

                filename = huntstring.replace(" ","_") + ".csv"
                fw = open(filename, "a+")
                headers = "Product, Customer Name, Rating, Heading, Comment \n"
                fw.write(headers)

                reviews = []
                for i in commentboxes:
                    try:
                        name = i.find('span',{"class":"a-profile-name"}).text
                    except:
                        logging.info("name")
                        name = "N.A"
                    try:
                        comment = i.find('div',{"class":"a-expander-content reviewText review-text-content a-expander-partial-collapse-content"}).span.text
                    except:
                        logging.info("comment")
                        comment = "N.A"
                    try:
                        heading = i.find('a',{"data-hook":"review-title"}).span.text
                    except:
                        logging.info("heading")
                        heading = "N.A"
                    try:
                        rating = i.find('i',{"data-hook":"review-star-rating"}).span.text
                        rating = rating[0]
                    except:
                        logging.info("rating")
                        rating = "N.A"
                    try:
                        headers = str(huntstring) + ", " + str(name) + ", " + str(rating) + ", " + str(heading) + ", " + str(comment) + "\n"
                        fw.write(headers)
                    except:
                        logging.info("CSV Write Error")
                    
                    newdict = { "Product" : huntstring , "Name" : name , "Rating" : rating , "Heading" : heading , "Comment" : comment}
                    reviews.append(newdict)

                logging.info("My final result logged {}".format(reviews))

                return render_template('result.html', reviews=reviews[0:(len(reviews))])

            except:
                logging.info("Something Wrong")
                return 'something is wrong'







if __name__ == "__main__":
    app.run(debug=True)