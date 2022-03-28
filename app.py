from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["get","post"])
def reply():
    clusters = MongoClient("mongodb+srv://aamirsabri:aamirsabri@cluster0.5aiso.mongodb.net/bakery?retryWrites=true&w=majority")
    db = clusters.bakery
    # db = clusters["bakery"]
    users = db["users"]
    orders = db["orders"]
    print("call")
    res = MessagingResponse()
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:","")
    user = users.find_one({"number": number})
    if bool(user) == False:
        res.message("Thanks for contacting Kasiri Group! \n choose one the option from below !\n 1️⃣ To Contact us \n 2️⃣ To *order snacks* \n 3️⃣ To know * working hours * \n4️⃣ To get our *address*")
        users.insert_one({"number": number,"status":"main","messeges":[]})
    elif user['status'] == "main":
        try:
            option = int(text)
        except:
            res.message("invalid input! please try valid input")
            return str(res)
        if option == 1:
            res.message("contact us on aamir.kashiri@gmail.com or +91 98247 47764")
        elif option == 2:
            res.message("You are entered in Order mode")
            users.update_one({"number":number},{"$set":{"status":"ordering"}})
            res.message("You can order following items \n 1️⃣ Red Forest \n 2️⃣ Black Forest \n 3️⃣ Strawberry \n 4️⃣ Blueberry \n\n Select your choice \n")
        elif option == 3:
            res.message("Working hours Mon-Son 9:00 AM to 9:00 PM")
        elif option == 4:
            res.message("Our Head office : Old Powerhouse Compound \n Azad Chawk \n Junagadh 362001")
        else:
            res.message("Sorry i could not understand")
            return str(res)
    elif user['status'] == "ordering":
        try:
            option = int(text)
        except:
            res.message("invalid input ! please try valid input")
            return str(res)
        if option == 0:
            users.update_one({"number":number},{"$set":{"status":"main"}})
            res.message(" \n 1️⃣ Red Forest \n 2️⃣ Black Forest \n 3️⃣ Strawberry \n 4️⃣ Blueberry \n\n Select your choice \n")
        elif 0 > option <= 4:
            cakes = ["Red Forest","Black Forest","Strawberry","Blueberry"]
            selected  = cakes[option]
            users.update_one({"number":number},{"$set":{"status":"address"}})
            users.update_one({"number":number},{"$set":{"item": selected}})
            res.message("Please enter your address to confirm the order")
        else:
            res.message("Please enter valid input")
            

    users.update_one({"number":number},{"$push":{"messeges":{"text":text,"date":datetime.now()}}})
    return str(res)


if __name__ == "__main__":
    app.run()
