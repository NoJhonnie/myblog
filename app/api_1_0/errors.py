# coding=utf-8
from flask import request, jsonify, render_template

from app.main import main


@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        return jsonify({'error':'not found'}), 404
    return render_template('404.html'), 404

def forbidden(message):
    return jsonify({'error':'forbidden', 'message':message}), 403

def unauthorized(message):
    return jsonify({'error':'unauthorized', 'message':message}), 401
