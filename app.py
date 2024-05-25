from flask import Flask, request
from flask_restful import Api, Resource, marshal_with, reqparse, abort, fields 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# app.config['SQLALCHEMY_TRACK_NOTIFICATION'] = False

db = SQLAlchemy(app)

class MyVideos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"vid: {self.id}, name: {self.name}, created: {self.created}"

# comes after Models are created - for production
# with app.app_context():
#     db.create_all()


parser = reqparse.RequestParser()
parser.add_argument("name", type=str, help="name of the video required", required=True)
parser.add_argument("views", type=int, help="total views required", required=True)
parser.add_argument("likes", type=int, help="total likes required", required=True)

# videos = {}

# def abort_if_video_error(vid):
#     if vid not in videos:
#         # return a response back
#         abort(404, message="could not find video...")

# def abort_if_video_exist(vid):
#     if vid in videos:
#         abort(409, message="video already saved...")

# serialize data to be displayed
resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer
}

class Videos(Resource):
    @marshal_with(resource_fields)
    def get(self):
        videos = MyVideos.query.order_by(MyVideos.created).all()
        return videos

# creating resource
class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, vid):
        # abort_if_video_error(vid)
        video = MyVideos.query.get(vid)

        if not video: abort(404, message="video not found")

        return video
        
    @marshal_with(resource_fields)
    def post(self, vid):
         # abort_if_video_exist(vid)
        args = parser.parse_args()

        existing_video = MyVideos.query.filter_by(id=vid).first()

        if existing_video: abort(409, message='video already saved')

        new_video = MyVideos(id=vid, **args)

        try:
            db.session.add(new_video)
            db.session.commit()
            return new_video, 201
        except Exception as err:
            return {"ERR:", err}

    def delete(self, vid):
        video = MyVideos.query.get(vid)

        if not video: abort(404, message="video not found")

        try:
            db.session.delete(video)
            db.session.commit()
            return {"message": f"video #{vid} deleted"}
        except Exception as err:
            return {"ERR": err}

api.add_resource(Videos, "/videos")
api.add_resource(Video, "/video/<int:vid>")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)