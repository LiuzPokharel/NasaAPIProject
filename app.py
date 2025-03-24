from flask import Flask, redirect, url_for, render_template, request, abort
import requests

app = Flask(__name__)

# sign up here for your own api key: https://api.nasa.gov/
api_key = "nsMLHCXa0PS7b58MnTKiwMwxz987bEaQqWGXxbcd"
nasa_api = "https://api.nasa.gov/planetary/apod"
mars_api = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
manifest_api = "https://api.nasa.gov/mars-photos/api/v1/manifests/curiosityt"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/apod")
@app.route("/apod/")
@app.route("/apod/<date>")
def apod(date="today"):
    data = get_apod(date)
    return render_template("apod.html", apod=data)


@app.route("/mars", methods=["GET", "POST"])
def mars():
    manifest = get_rover_manifest()

    if request.method == "POST":
        sol = request.form["sol"]
        camera = request.form["camera"]
    else:
        sol = 0
        camera = "fhaz"
            
    data = get_rover_photos(sol, camera)
    return render_template(
        "mars.html",
        photos=data["photos"],
        sol=sol,
        camera=camera,
        # mission=manifest["photo_manifest"]
    )



def get_apod(date):
    params = {"api_key": api_key}
    if date != "today":
        params["date"] = date

    res = requests.get(nasa_api, params)
    
    if res.status_code != 200: 
    
        error_apod = {
            "title": f"API Error - {res.status_code}",
            "explanation": "Error!",
            "url" : url_for('static', filename="file_not_found.jpg")
        }
        
        return error_apod
    
    return res.json()


def get_rover_photos(sol, camera):
    params = {"api_key": api_key, "sol": sol, "camera": camera, "page": 1}
    res = requests.get(mars_api, params)
    return res.json()


def get_rover_manifest():
    params = {"api_key": api_key}
    res = requests.get(manifest_api, params)
    
    if res.status_code != 200:
        error_mars = {
            "title": f"MARS Error - {res.status_code}",
            "explanation": "NEIN!",
            "url" : url_for('static', filename="file_not_found.jpg")
        }
    
    return res.json()


@app.errorhandler(404)
def page_not_found(err):
    return render_template("404.html"), 404
