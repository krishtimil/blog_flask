from flask import jsonify
from flask_restful import Resource, reqparse, abort, Api
from .models import Post, db
from flask_login import login_required, current_user

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, help='Title of the post')
parser.add_argument('content', type=str, help='Content of the post')


class PostAPI(Resource):
    # Require authentication for PUT, POST, and DELETE operations
    @login_required
    def post(self):
        args = parser.parse_args()
        post = Post(title=args['title'],
                    content=args['content'], author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return {'id': post.id, 'title': post.title, 'content': post.title, 'date_created': post.date_created.isoformat(), 'author': post.author}

    def get(self, post_id=None):
        if post_id == None:
            args = parser.parse_args()
            page = args['page']
            posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=5)
            response = [{'id': post.id, 'title': post.title, 'content': post.title, 'date_created': post.date_created.isoformat(), 'author': post.author} for post in posts.items]
            result = {'total_number': len(Post.query.all()), 'page': page, 'showing': 5, 'posts': response} 
            return jsonify(result)       
        post = Post.query.get(post_id)
        if not post:
            abort(404, message="Post not found")
        return {'id': post.id, 'title': post.title, 'content': post.title, 'date_created': post.date_created.isoformat(), 'author': post.author}

    @login_required
    def put(self, post_id):
        args = parser.parse_args()
        post = Post.query.get(post_id)
        if not post:
            abort(404, message="Post not found")
        if current_user.id != post.author_id:
            abort(401, message="Unauthorized access")
        post.title = args['title']
        post.content = args['content']
        db.session.commit()
        return {'id': post.id, 'title': post.title, 'content': post.content, 'date_created': post.date_created.isoformat(), 'author': post.author.username}

    @login_required
    def delete(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            abort(404, message="Post not found")
        if current_user.id != post.author_id:
            abort(401, message="Unauthorized access")
        db.session.delete(post)
        db.session.commit()
        return {'message': 'Post deleted successfully'}

