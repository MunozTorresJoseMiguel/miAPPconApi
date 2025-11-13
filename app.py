from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")


DATAFOOD_API_URL = "https://http://127.0.0.1:5000//v1/foods/search"
DATAFOOD_API_KEY = "1cCX8y0wpTQRG1fpLyFdZHacgthjLhTdd3N127AA" 

@app.route('/buscar', methods=['POST'])
def buscar():
    comida = request.form.get('name', '').strip().lower()
    
    if not comida:
        flash('Por favor ingresa un nombre de comida válido.', 'error')
        return redirect(url_for('index'))
    

    API = "https://http://127.0.0.1:5000//v1/foods/search"

    headers = {
        "Authorization": f"Bearer {DATAFOOD_API_KEY}",
        "Accept": "application/json"
    }

    try:
     
        response = requests.get(API, params={"query": comida}, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if not data or "foods" not in data or len(data["foods"]) == 0:
                flash(f'Comida "{comida}" no encontrada.', 'error')
                return redirect(url_for('index'))

            lista_comidas = []  

            for alimento in data["foods"]:

                nutrientes = alimento.get("nutrients", {}) 

                comida_info = {
                    'name': alimento.get('name', 'Sin nombre'),
                    'marca': alimento.get('brand', 'Sin marca'),
                    'porcion': alimento.get('serving_size', 'N/A'),
                    'kcal': nutrientes.get('energy_kcal', 'N/A'),
                    'proteina': nutrientes.get('protein_g', 'N/A'),
                    'grasa': nutrientes.get('fat_g', 'N/A'),
                    'carbohidratos': nutrientes.get('carbs_g', 'N/A'),
                    'imagen': alimento.get("image", None),  
                }

                lista_comidas.append(comida_info)

            return render_template('targeta.html', comidas=lista_comidas)

        else:
            flash('Error al obtener datos de la API.', 'error')
            return redirect(url_for('index'))

    except requests.exceptions.RequestException as e:
        print("API ERROR:", e)
        flash('Error al conectar con la API. Inténtalo más tarde.', 'error')
        return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(debug=True)
