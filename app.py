from flask import Flask, render_template, request,flash, redirect, url_for
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")
USDA_API_KEY = "1cCX8y0wpTQRG1fpLyFdZHacgthjLhTdd3N127AA"

@app.route('/lista', methods=['GET'])
def lista_alimentos():
    pagina = request.args.get('page', 1, type=int)

    url = "https://api.nal.usda.gov/fdc/v1/foods/list"
    params = {
        "api_key": USDA_API_KEY,
        "pageNumber": pagina,
        "pageSize": 12,
        "dataType": "Survey (FNDDS),Branded"
    }

    alimentos = []
    error = None

    try:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            error = f"Error al consultar la API: {response.status_code}"
        else:
            data = response.json()      

            for food in data:
                alimentos.append({
                    "fdc_id": food.get("fdcId"),
                    "descripcion": food.get("description", "Sin descripción"),
                    "data_type": food.get("dataType"),
                    "publicacion": food.get("publicationDate", "N/D"),
                })

    except Exception as e:
        error = f"Ocurrió un error: {e}"

    return render_template(
        "lista.html",
        alimentos=alimentos,
        pagina=pagina,
        error=error
    )





if __name__ == '__main__':
    app.run(debug=True)
