from flask import Flask, jsonify, request, render_template
import time, requests, os, socket
from jose import jwt
import json
import pymysql.cursors
DEFAULT_ISSUER = "http://authentication-identity-server:8080/realms/master"

_JWKS_CACHE = {} 

def get_jwks(issuer_url):
    global _JWKS_CACHE
    now = time.time()
    
    internal_issuer_url = issuer_url
    if "localhost:8081" in internal_issuer_url:
        internal_issuer_url = internal_issuer_url.replace("localhost:8081", "authentication-identity-server:8080")


    jwks_url = f"{internal_issuer_url}/protocol/openid-connect/certs"
    
    if issuer_url not in _JWKS_CACHE or now - _JWKS_CACHE[issuer_url]['ts'] > 600:
        print(f"Dang lay JWKS tu URL noi bo: {jwks_url}") 
        try:
            jwks_data = requests.get(jwks_url, timeout=5).json()
            _JWKS_CACHE[issuer_url] = {'keys': jwks_data, 'ts': now}
        except Exception as e:
            print(f"Loi khi goi JWKS: {e}")
            return None
            
    return _JWKS_CACHE[issuer_url]['keys']

app = Flask(__name__)

@app.route('/')
def index():
    container_id = socket.gethostname()
    return render_template('index.html', hostname=container_id)

@app.get("/hello")
def hello(): return jsonify(message="Hello from App Server!")

@app.get("/secure")
def secure():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify(error="Missing Bearer token"), 401
    
    token = auth.split(" ", 1)[1]
    
    try:
        unverified_claims = jwt.get_unverified_claims(token)
        issuer_found = unverified_claims.get('iss')
        
        jwks = get_jwks(issuer_found)
        if not jwks:
             return jsonify(error=f"Cannot fetch JWKS for issuer: {issuer_found}"), 401

        payload = jwt.decode(
            token, 
            jwks, 
            algorithms=["RS256"], 
            options={"verify_aud": False}, 
            issuer=issuer_found
        )
        
        return jsonify(
            message="Secure resource OK", 
            preferred_username=payload.get("preferred_username"),
            issuer=issuer_found
        )
        
    except Exception as e:
        return jsonify(error=str(e)), 401
    

@app.get("/student")
def student():
    """
    Mở rộng 2 (phần file JSON):
    Trả về danh sách sinh viên từ file students.json trong container.
    """
    try:
        with open("students.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify(error="students.json not found"), 404
    except Exception as e:
        return jsonify(error=f"Error reading JSON file: {str(e)}"), 500


@app.get("/db/student")
def db_student():
    """
    Mở rộng 2 (phần Database):
    Trả về danh sách sinh viên từ MariaDB (relational-database-server).
    """
    HOST = os.getenv("DB_HOST", "relational-database-server")
    USER = os.getenv("DB_USER", "root")
    PASSWORD = os.getenv("DB_PASSWORD", "root")
    DATABASE = os.getenv("DB_NAME", "studentdb")

    connection = None
    try:
        connection = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            sql = "SELECT student_id, fullname, major, dob FROM students"
            cursor.execute(sql)
            result = cursor.fetchall()
            return jsonify(result)

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify(
            error=f"Database connection or query failed. Check DB server: {str(e)}"
        ), 500
    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)

