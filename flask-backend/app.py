from flask import Flask, request, Response, jsonify, make_response
from flask_mongoengine import MongoEngine
import json
from bson import ObjectId
from sqlalchemy import true
from classes import User, Article
import jwt
from functools import wraps
import datetime
from passlib.hash import sha256_crypt
from flask_cors import CORS
import sys

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'token' in request.headers:
            token = request.headers['token']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[
                'HS256'])  # bilgileri aldik
            current_user = User.objects.get(username=data["username"])

        except:
            return ('', 204)

        return f(current_user, *args, **kwargs)

    return decorator


# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)

app = Flask(__name__)
CORS(app, supports_credentials=true)


app.config["MONGODB_HOST"] = "mongodb+srv://iremtopcam:iremtopcam@cluster0.jxdlp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
app.config["SECRET_KEY"] = "abc123"

mongo = MongoEngine()
mongo.init_app(app)


@app.route('/', methods=['GET'])
def helloworld():
    return "api Server is ready"

# register islemleri
# user işlemleri usera post request atınca registerı gerceklestirdim.
# register islemleri
# username aynı olursa hata kodunu fronta yansıt


@app.route('/Register', methods=["POST"])
def register():  # kullanıcı adı daha once alınmıs mı parola standartları
    if request.method == "POST":
        name = request.json['name']
        surname = request.json['surname']
        username = request.json['username']
        password = request.json['password']
        confirm_password = request.json['confirm_password']
        email = request.json['email']

        if confirm_password == password:
            password = sha256_crypt.encrypt(password)

            if username and password and email:
                # mongo engine dokuman classı olan Userdan istegin icindeki bilgilerden yeni bir user nesnesi olusturdumm
                user = User(name=name, surname=surname,
                            username=username, password=password, email=email)
                user.save()  # dtbkyt

            return {'message': 'successful user adding'}

        else:
            return {'message': 'passwords are not same'}


@app.route('/User', methods=["GET"])
def user():

    users = []
    for user in User.objects:  # *******************
        users.append(user)

    return make_response(jsonify(users))  # json dosyası olarak cevap döndürdüm


@app.route('/getUser', methods=["GET"])
@token_required
def getUser(current_user):
    username = current_user["username"]
    return make_response(jsonify(current_user))


@app.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    return jsonify({"message": True})


@app.route('/deleteUser', methods=['POST'])  # delete http methoduyla belirt
def deleteUser():
    if request.method == "POST":
        username = request.json['username']
        # username unique oldugu icin username gore siliyorum diger projedeki fetchone
        user = User.objects.get(username=username)
        User.delete(user)

        return {'message': 'successful user deleting'}


@app.route('/updateUser', methods=['POST'])
@token_required
def updateUser(current_user):
    if request.method == "POST":
        _id = current_user['id']  # iddiddidi

        try:
            if request.json["author"]: #sadece author updateleniyor
                author = request.json["author"]
                user = User.objects.get(id=_id)
                user.update(author=author)
            else:
                email = request.json['email']  # acıklama dondurmeli .get metodu
                password = request.json['password']  # varsa degeri ypksa none YILDIZ
                user = User.objects.get(id=_id)
                user.update(email=email, password=password)
        except:
            pass

        return {'message': 'successful user updating'}



# login işlemi
@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        username = request.json['username']
        password = request.json['password']  # password
        user = User.objects.get(username=username)

        if sha256_crypt.verify(password, user["password"]):
                token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow(
                ) + datetime.timedelta(minutes=15)}, app.config['SECRET_KEY'])
                return jsonify({'token': token})

        else:
                return {"message": "Password invalid"}

            
   

#a
# article işlemleri  add article ayır
@app.route('/Article', methods=['POST', "GET"])
@token_required
def article(current_user):
    if request.method == "POST" and current_user["author"]:
        title = request.json['title']
        author = current_user["username"]
        description = request.json['description']

        if title and description:
            article = Article(title=title, author=author,
                              description=description)
            article.save()

        return {'message': 'successful article adding'}

    if not current_user["author"]:
        return {'message': 'User is not an author'}


@app.route('/getArticle', methods=["GET"])
def getArticle():
    if request.method == "GET":
        articles = []
        for article in Article.objects:
            articles.append(article)

        articles.sort(key=lambda x:x.vote,reverse=1)
        return make_response(jsonify(articles))


@app.route('/updateArticle', methods=['POST'])
@token_required
def updateArticle(currentUser):
    if request.method == "POST":
        _id = currentUser['_id']
        title = request.json['title']
        description = request.json['description']
        vote = request.json['vote']

        article = Article.objects.get(id=_id)
        article.update(title=title, description=description, vote=vote)

        return {'message': 'successful article updating'}


@app.route('/upvote', methods=['POST'])
@token_required
def upvote(currentUser):
    if request.method == "POST":
        try:

            _id = request.json['id']
            article = Article.objects.get(id=_id)
            upvotes = article["upvotes"]
            downvotes = article["downvotes"]
            if currentUser["username"] in upvotes:
                upvotes.remove(currentUser["username"])
                vote = len(upvotes)-len(downvotes)

                article.update(vote=vote,
                               upvotes=upvotes, downvotes=downvotes)
                return {"message": "Oy kullanılmış upvote"}
            else:
                if currentUser["username"] in downvotes:
                    downvotes.remove(currentUser["username"])

                upvotes.append(currentUser["username"])

                vote = len(upvotes)-len(downvotes)

                article.update(vote=vote,
                               upvotes=upvotes, downvotes=downvotes)

                # bir kullanıcının birden fazla oy kullanmasın

                return make_response(jsonify(article.vote))

        except:
            return {'message': 'warning'}


@app.route('/downvote', methods=['POST'])
@token_required
def downvote(currentUser):
    if request.method == "POST":
        _id = request.json['id']
        article = Article.objects.get(id=_id)
        upvotes = article["upvotes"]
        downvotes = article["downvotes"]
        if currentUser["username"] in downvotes:
            downvotes.remove(currentUser["username"])
            vote = len(upvotes)-len(downvotes)

            article.update(vote=vote,
                           upvotes=upvotes, downvotes=downvotes)
            return {"message": "Oy kullanılmış downvote"}
        else:
            if currentUser["username"] in upvotes:
                upvotes.remove(currentUser["username"])

            downvotes.append(currentUser["username"])

            vote = len(upvotes)-len(downvotes)
            article.update(vote=vote,
                           upvotes=upvotes, downvotes=downvotes)

            # bir kullanıcının birden fazla oy kullanmasın

            return make_response(jsonify(article.vote))


@app.route('/deleteArticle', methods=['POST', "GET"])
def deleteArticle():
    if request.method == "POST":
        _id = request.json['_id']
        article = Article.objects.get(id=_id)
        Article.delete(article)

        return {'message': 'successful article deleting'}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

    # app.run(debug=True,host="0.0.0.0", port=5000)

    # cap
