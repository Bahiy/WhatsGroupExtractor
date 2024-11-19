from flask import Flask, request, jsonify
import group_scrapper

app = Flask(__name__)

@app.route('/run-script', methods=['POST'])
def run_script():
    group_scrapper.main()
    result = {"message": "Script executado com sucesso!"}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
