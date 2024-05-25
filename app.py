from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort 

app = Flask(__name__)

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, help="name of the video required", required=True)
parser.add_argument("views", type=int, help="total views required", required=True)
parser.add_argument("likes", type=int, help="total likes required", required=True)

videos = {}

def abort_if_video_error(vid):
    if vid not in videos:
        # return a response back
        abort(404, message="could not find video...")

def abort_if_video_exist(vid):
    if vid in videos:
        abort(409, message="video already saved...")

class Videos(Resource):
    def get(self):
        return videos

# creating resource
class Video(Resource):
    def get(self, vid):
        abort_if_video_error(vid)

        return videos[vid]

    def post(self, vid):
        # likes = request.form["likes"]
        abort_if_video_exist(vid)
        args = parser.parse_args()
        videos[vid] = args

        return videos.get(vid), 201

    def delete(self, vid):
        abort_if_video_error(vid)
        del videos[vid]

        return {"message": f"video #{vid} deleted"}

api.add_resource(Videos, "/videos")
api.add_resource(Video, "/video/<int:vid>")

if __name__ == "__main__":
    app.run(debug=True)