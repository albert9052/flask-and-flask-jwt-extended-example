from flask import (
    Flask,
    jsonify,
    request,
    render_template
)
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies
)
from datetime import timedelta

app = Flask(__name__)

# This might be needed later for working with Vue. 
#app = Flask(__name__,
#            static_folder="",
#            template_folder="")

JWT_LOGOUT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=3)
JWT_LOGOUT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=3)

app.config["JWT_SECRET_KEY"] = "cliNIC_super_super_super_secret_key"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = True # Should be True in production. 
app.config["JWT_COOKIE_SAMESITE"] = "Strict" # It can be Strict, Lax, and None (default). However, most browsers nowaday see None as Lax. 
app.config["JWT_REFRESH_COOKIE_PATH"] = "/refresh" # Only path containing "/refresh" can send refresh token to the backend. 
app.config["JWT_COOKIE_CSRF_PROTECT"] = False # Should be True in production. 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

jwt = JWTManager(app)

@app.route("/", methods=["GET"])
def default():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username != "test" or password != "test":
        return jsonify({"msg": "Incorrect username or password"}), 401

    access_token = create_access_token(identity=username, fresh=True)
    refresh_token = create_refresh_token(identity=username)
    resp = jsonify(access_token=access_token, refresh_token=refresh_token)
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp

@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user, expires_delta=JWT_LOGOUT_ACCESS_TOKEN_EXPIRES)
    refresh_token = create_access_token(identity=current_user, expires_delta=JWT_LOGOUT_REFRESH_TOKEN_EXPIRES)
    resp = jsonify(access_token=access_token, refresh_token=refresh_token)
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp

# This is for refreshing access token using the refresh token if the previous token has expired. 
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user, fresh=False)
    resp = jsonify(access_token=access_token)
    set_access_cookies(resp, access_token)
    return resp

# Using "@jwt_required()" can only allow this api be called with valid fresh access token no matter it's fresh or not.  
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(foo="bar")

# Using "@jwt_required(fresh=True)" can only allow this api be called with fresh access token, which is the token created after logging in. 
# If the access token is refreshed before, then it's not fresh anymore. 
@app.route("/more-protected", methods=["GET"])
@jwt_required(fresh=True)
def more_protected():
    return jsonify(foo="barbar")

if __name__ == "__main__":
    app.debug = True
    app.run()
