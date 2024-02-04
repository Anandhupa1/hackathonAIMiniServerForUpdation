import os
import openai
import json
import datetime
from dotenv import load_dotenv
from flask_cors import CORS
import qdrant_client
from qdrant_client.http import models
from langchain.vectorstores import Qdrant;
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

from flask import Flask,request,jsonify

app = Flask(__name__)
CORS(app)

app.config['MONGO_URI'] = 'mongodb+srv://Anandhu:anandhu@cluster0.j8dbuza.mongodb.net'
mongo = MongoClient(app.config['MONGO_URI'])

db = mongo["AICHATBOT"]  # Replace <dbname> with the name of your database


product_function = [
    {
        "name": "get_product_id",
        "description": "Get all the mongodb _id and score of the products from given array of objects",
        "parameters": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {
                        "type" : "object",
                        "properties" : {
                            "_id": {
                                "type": "string",
                                "description": "key, e.g.only 6526dbf87e6341f9e871c0f5 from all _id's like ObjectId('6526dbf87e6341f9e871c0f5')"
                            },
                            "score": {
                                "type": "number",
                                "description": " 0.80926543 from all  score: 0.80926543"
                            },
                        },
                        "required" : ["_id","score"]
                    }
                }
            },
            "required": ["data"]    
        },
    }
]

query1 = """[Document(page_content='{"id": 2, "Name": "Cafe Delhi Heights", "Address": "Chanakya Mall, Ground Floor, Chanakyapuri, New Delhi, Delhi 110021, India", "Google_Map_Location": "https://maps.app.goo.gl/W3JqYh5gSAbiDnZ7A", "Cuisine": "Continental, American, Indian", "Ambiance": "Cozy and contemporary", "Menu": "Burgers, Sandwiches, Pasta, Salads, Desserts, Shakes", "Average Cost for Two": "\\u20b91,200 - \\u20b91,800", "Events and Activities": "Casual dining and get-togethers", "Operating Hours": "11:00 AM - 11:00 PM, hours may vary", "Facilities & Features": {"Air Conditioned": true, "Outdoor Seating": true, "Full Bar Available": true, "Table Reservation Recommended": true, "Free Wi-Fi": true}, "Rating": "4 out of 5 stars", "Best Selling Dish": "CDH Signature Burger", "Booking_Site": "https://www.dineout.co.in/delhi/cafe-delhi-heights-rk-puram-south-delhi-20189", "image": "https://im1.dineout.co.in/images/uploads/restaurant/sharpen/1/i/t/p15105-145690007356d687e9547a8.jpg?tr=tr:n-xlarge", "near": "saket"}', metadata={'seq_num': 2, 'source': '/Users/ansh/Desktop/Projects/GenAI/CafeGuide.ai/backend/db.json'}), Document(page_content='{"id": 3, "Name": "Diggin", "Address": "11, Santushti Shopping Complex, Race Course Road, Chanakyapuri, New Delhi, Delhi 110021, India", "Google_Map_Location": "https://maps.app.goo.gl/nkcnz3f4yCTqEvVu6", "Cuisine": "Italian, Continental", "Ambiance": "Charming with outdoor seating and greenery, elegant decor", "Menu": "Italian dishes, Pasta, Pizza, Salads, Sandwiches, Desserts, Coffee, Mocktails", "Average Cost for Two": "\\u20b91,200 - \\u20b91,800", "Events and Activities": "Primarily for dining and relaxation", "Operating Hours": "Lunch and dinner, hours may vary", "Facilities & Features": {"Air Conditioned": true, "Outdoor Seating": true, "Kid-Friendly": true, "Table Reservation Recommended": true, "Free Wi-Fi": true}, "Rating": "4.5 to 5 stars", "Best Selling Dish": "Lasagna or Red Velvet Cake", "Booking_Site": "https://www.dineout.co.in/delhi/diggin-chanakyapuri-south-delhi-34492", "image":', metadata={'seq_num': 3, 'source': '/Users/ansh/Desktop/Projects/GenAI/CafeGuide.ai/backend/db.json'}), Document(page_content='{"id": 1, "Name": "Hauz Khas Social", "Address": "D-88, 2nd Floor, 31st December Marg, Block D, Hauz Khas, New Delhi, Delhi 110016, India", "Google_Map_Location": "https://maps.app.goo.gl/hRtvW2R728xL7iR77", "Cuisine": "Indian, Continental, Asian", "Ambiance": "Contemporary, Industrial-style, Rooftop seating with a view of Hauz Khas Lake", "Menu": "Burgers, Sandwiches, Pasta, Cocktails, Mocktails, and more", "Average Cost for Two": "\\u20b91,500 - \\u20b92,500 or more", "Events and Activities": "Live music, social gatherings, nightlife", "Operating Hours": "Varies, check official website or contact them for current hours", "Facilities & Features": {"Air Conditioned": true, "Outdoor Seating": true, "Full Bar Available": true, "Live Music": true, "Rooftop Seating": true, "Smoking Area": true, "Free Wi-Fi": true, "Table Reservation Not Required": true}, "Rating": "4 out of 5 stars", "Best Selling Dish": "Butter Chicken Biryani", "Booking_Site":', metadata={'seq_num': 1, 'source': '/Users/ansh/Desktop/Projects/GenAI/CafeGuide.ai/backend/db.json'}), Document(page_content='"https://im1.dineout.co.in/images/uploads/restaurant/sharpen/1/i/t/p15105-145690007356d687e9547a8.jpg?tr=tr:n-xlarge", "near": "saket"}', metadata={'seq_num': 3, 'source': '/Users/ansh/Desktop/Projects/GenAI/CafeGuide.ai/backend/db.json'}), Document(page_content='"https://www.dineout.co.in/delhi/hauz-khas-social-hauz-khas-village-south-delhi-16246", "image": "https://im1.dineout.co.in/images/uploads/restaurant/sharpen/1/i/t/p15105-145690007356d687e9547a8.jpg?tr=tr:n-xlarge", "near": "Hauz Khas"}', metadata={'seq_num': 1, 'source': '/Users/ansh/Desktop/Projects/GenAI/CafeGuide.ai/backend/db.json'})]"""



@app.route('/')
def home():
    data = list(db.datas.find({}))
    print(")))))))))))))))))))))))))))))))))))))))))))))))))")
    print(data)
    strData =[]
    for x in data :strData.append(str(x["data"]))
    # creating collection
    # embeddings = OpenAIEmbeddings();
    client = qdrant_client.QdrantClient(
        url=os.getenv("QDRANT_HOST"),
        api_key= os.getenv("QDRANT_API_KEY")
    )

    from qdrant_client.models import Distance, VectorParams 
     
    client.recreate_collection( 
        collection_name="collection2", 
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE), 
    )

    vector_store = Qdrant(
     client=client,
     collection_name="collection2",
     embeddings=OpenAIEmbeddings(),
       )
    print(vector_store)
    vector_store.add_texts(strData) 
    print("successfully added")
    return strData


@app.route('/search',methods=["POST"])
def hello1():
  body = request.json
  query = body["query"] or "what can I ask to you ?";
  print(query)
  #______________________________________________________________
  embeddings = OpenAIEmbeddings();
  client = qdrant_client.QdrantClient(
    url=os.getenv("QDRANT_HOST"),
    api_key= os.getenv("QDRANT_API_KEY")
    )
  vector_store = Qdrant(
    client=client,
    collection_name="collection2",
    embeddings=OpenAIEmbeddings(),
  )
  print(vector_store)
  found_docs =vector_store.similarity_search(query)
  print(found_docs)
  #__________________________________________________________________

  llm = OpenAI(model_name="gpt-3.5-turbo",temperature=1.5)
  chain = load_qa_chain(llm=llm,chain_type="stuff");
  response = chain.run(input_documents=found_docs,question=query)
  
  print(response)



  return jsonify({"data": response})  


























if __name__ == '__main__':
    app.run(debug=True)





