from flask import Flask, jsonify
import bs4
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# Instancia de Flask
app = Flask(__name__)

# URL a consultar
url = 'https://www.bcv.org.ve/estadisticas/graficos/precios-petro'


@app.route('/')
def main():
    return 'Saludos desde la API!!'


@app.route('/tasasPetroJson', methods=['GET'])
def getTasasJson():
    try:
        # La siguiente línea se debe colocar para omitir errores con certificados SSL
        urllib3.disable_warnings(InsecureRequestWarning)

        # Se debe enviar verify=False si se utiliza la instrucción anterior
        resultado = requests.get(url, verify=False)

        # Formatear HTML en XML
        soup = bs4.BeautifulSoup(resultado.text, 'lxml')

        # Lista de tasas
        lista_tasas = []

        # Se procesan las etiquetas
        for tag_fecha in soup.find_all('td', class_='views-field views-field-field-fecha'):
            # Se ubica el nodo padre de la línea de la tabla en revisión
            tag_tr_padre = tag_fecha.find_previous('tr')

            # Se ubica el nodo de tasa de Dólar
            tag_td_dolar = tag_tr_padre.find_next(class_='views-field views-field-field-dolar-bl')

            # Se ubica el nodo de tasa de Euro
            tag_td_euro = tag_tr_padre.find_next(class_='views-field views-field-field-euro-bl')

            # Se construye el diccionario con los datos por fecha
            datos_tasas = {'fecha': tag_fecha.text.strip(),
                           'tasaDolar': tag_td_dolar.text.strip(),
                           'tasaEuro': tag_td_euro.text.strip()}

            # Se agrega a la lista de salida
            lista_tasas.append(datos_tasas)

        # json_output = json.dumps({'dataTasas:': lista_tasas})
        # return json_output

        return jsonify({'dataTasas:': lista_tasas})

    except Exception as error:
        msg_err = 'Mensaje de error: ' + error.__str__()

        return msg_err
