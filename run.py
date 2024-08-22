from app.main import app
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "host":
        host = "0.0.0.0"
    else:
        host = ""
    app.run(debug=True, host=host)
