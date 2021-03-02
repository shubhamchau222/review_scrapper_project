# some neccessary imports
from flask import Flask, render_template, request , jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs


app = Flask(__name__)   # initialising the flask app with the name 'app'

#home page starting page
@app.route("/" , methods = ["GET"]) # route to display the home page
@cross_origin()
def homepage():
    return  render_template("index.html")

@app.route("/backEnd" , methods = ["POST" ,"GET"])
@cross_origin()
def index():
    if request.method == "POST" :
        searchString = request.form["content"].replace( " " ,"" )  # getting the user req & removing white spaces
        try:
            if "a" == "b":
                pass

            else:
                base_url = "https://www.flipkart.com/search?q="
                flipkart_url = base_url + searchString
                conn = requests.get(flipkart_url)
                flipkart_html = bs(conn.text, "html.parser")
                bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
                del bigboxes[0:3]
                box = bigboxes[0]
                productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
                link_conn = requests.get(productLink)
                new_html_data = bs(link_conn.text, "html.parser")
                main_box = new_html_data.find(class_="_1YokD2 _3Mn1Gg col-8-12")
                device_id = main_box.find(class_="B_NuCI").text
                device_price = main_box.find(class_="_30jeq3 _16Jk6d").text
                rev_subboxes = main_box.find('div', {'class': "col JOpGWq"})
                length = len(rev_subboxes.find_all("a", href=True))
                review_page_link = rev_subboxes.find_all("a", href=True)[length - 1]['href']
                new_base_url = "https://www.flipkart.com"
                review_page = requests.get(new_base_url + review_page_link)
                review_page_html = bs(review_page.text, "html.parser")
                rev_main_box = review_page_html.find(class_="_1YokD2 _3Mn1Gg col-9-12")
                rev_subboxes = rev_main_box.find_all("div", {"class": "_1AtVbE col-12-12"})
                bottom_review_pages_links = rev_subboxes[12].find_all("a", href=True)
                link_list = []
                for link in bottom_review_pages_links:
                    link_list.append(link['href'])

                reviews=[]

                # function
                def project(link , storage):
                    #global reviews
                    new_base_url = "https://www.flipkart.com"
                    #print(link)
                    conn = requests.get(new_base_url + link)
                    spicy_soup = bs(conn.text, "html.parser")
                    rev_main_box = spicy_soup.find(class_="_1YokD2 _3Mn1Gg col-9-12")
                    rev_main_box_subboxes = rev_main_box.find_all("div", {"class": "_1AtVbE col-12-12"})
                    length = len(rev_main_box_subboxes)
                    for i in range(2, length - 1):
                        try:
                            device_id = main_box.find(class_="B_NuCI").text  # or device name
                        except:
                            device_id = searchString

                        try:
                            device_price = main_box.find(class_="_30jeq3 _16Jk6d").text
                        except:
                            device_price = "Null"
                        try:
                            rating = rev_main_box_subboxes[i].find(class_="_3LWZlK _1BLPMq").text

                        except:
                            rating = "Null"
                        try:
                            comment_heading = rev_main_box_subboxes[i].find("p", {"class": "_2-N8zT"}).text

                        except:
                            comment_heading = "Null "
                        try:
                            comment_ = rev_main_box_subboxes[i].find("div", {"class": "t-ZTKy"}).text
                        except:
                            comment_ = "Null"
                        try:
                            buyer_name = rev_main_box_subboxes[i].find("div", {"class": "row _3n8db9"}).find(class_="_2sc7ZR _2V5EHH").text

                        except:
                            buyer_name = "Null"

                        data_dict = {
                            "Product": device_id, "Price": device_price,
                            "Buyer": buyer_name,
                            'Rating': rating, 'CommentHead': comment_heading,
                            "Comment": comment_
                                                }
                        try:
                            reviews.append(data_dict)
                        except:
                            print("list not found ....")



                for x in link_list[0:len(link_list)-1]:
                    project(x,reviews)

                #print(len(reviews))

                return render_template("results.html", reviews=reviews[0:len(reviews)-1])

        except :
            return  "something wrong...!"


    else:
        return render_template("index.html")



if __name__ == "__main__":
    #app.run (port=8000,debug=True) # running the app on the local machine on port 8000
    app.run(debug=True)















