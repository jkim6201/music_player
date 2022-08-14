from flask_app import app
from flask import flash, render_template,redirect,session,request
from flask_app.models.user import User
from flask_app.models.music import Music
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import requests
import spotipy 
from spotipy import SpotifyClientCredentials
from pprint import pprint

@app.route('/dashboard')
def user_dashboard():
    if "user_id" not in session:
        return redirect('/')
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_user_by_id(user_data)
    musics = Music.get_all_music_by_user(user_data)
    return render_template('dashboard.html',user=user, musics=musics)

@app.route('/music/new')
def new_music_form():
    user_data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    return render_template('create.html', user=user)

@app.route('/search', methods=["POST"])
def search():
    search_term= request.form['search_term']
    cid = '2cf1465bafce4d5182527bc69aec513e'
    secret = 'bbfe641e3c7c44808870a2931f9ce614'
    auth_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    results= sp.search(search_term, type="track", limit=50)
    pprint(results['tracks']['items'][0],sort_dicts=False)
    return render_template("show.html", tracks=results['tracks']['items'], search_term = search_term)

@app.route('/tracks')
def tracks():
    cid = '2cf1465bafce4d5182527bc69aec513e'
    secret = 'bbfe641e3c7c44808870a2931f9ce614'
    auth_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    results= sp.search("Blackpink", type="track", limit=50)
    pprint(results)
    return render_template("show.html", tracks=results['tracks']['items'], search_term= "Blackpink")

@app.route('/music/create/form')
def music_form():
    render_template("create.html")

@app.route('/music/create',methods=['POST'])
def create_music():
    # if not Music.validate_create(request.form):
    #     return redirect('/music/new')
    Music.create(request.form)
    return redirect('/dashboard')

@app.route('/show')
def show_music(id):
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_user_by_id(user_data)
    music_data = {
        'id': id
    }
    musics = Music.get_all_music_by_user(user_data)
    return render_template('show.html',musics=musics,user=user)

@app.route('/music/<int:id>/edit')
def show_edit_form(id):
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_user_by_id(user_data)
    music_data = {
        'id' : id
    }
    music = Music.get_one(music_data)
    if(music.user_id != user.id):
        flash('Unauthorized access to edit music with id {id}')
        return redirect('/dashboard')

    return render_template('edit.html',user=user,music=music)


@app.route('/music/<int:id>/update',methods=['POST'])
def update_music(id):
    music_data = {
        'id' : id
    }
    music = Music.get_one(music_data)
    if(music.user_id !=session['user_id']):
        flash('Unauthorized access to update music with id {id}')
        return redirect('/dashboard')
    Music.update(request.form)
    return redirect('/dashboard')

@app.route('/music/delete/<int:id>')
def delete(id):
    music_data = {
        'id' : id
    }
    music = Music.get_one(music_data)
    if(music.user_id !=session['user_id']):
        flash('Unauthorized access to delete music with id {id}')
        return redirect('/dashboard')
    Music.delete(music_data)
    return redirect('/dashboard')

