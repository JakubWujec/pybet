from flasky import create_app
import os 
app = create_app()

if __name__ == "__main__":
    # SET FLASK_ENV_FILE=.env.test flask --app flask_app run --host=localhost --port=5005 
    #flask --app flask_app run --host=localhost --port=5005 
    print(f"ENV_LOADED: {os.environ.get('FLASK_ENV_FILE', 'NONE')}")
    app.run(host="localhost", port=5005, debug=True)
    
