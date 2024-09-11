from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', data=[])

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    results = []

    if query:
        try:
            url = f'https://search.naver.com/search.naver?query={query}'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extracting relevant information
            cm_info_box = soup.find('div', class_='cm_info_box')
            if cm_info_box:
                # Extract title
                title = cm_info_box.find('h3', class_='title')
                if title:
                    results.append(f"Title: {title.get_text()}")

                # Extract details
                detail_info = cm_info_box.find('div', class_='detail_info')
                if detail_info:
                    info_dict = {}
                    for info_group in detail_info.find_all('div', class_='info_group'):
                        dt = info_group.find('dt')
                        dd = info_group.find('dd')
                        if dt and dd:
                            info_dict[dt.get_text(strip=True)] = dd.get_text(strip=True)
                    results.append('Details:')
                    for key, value in info_dict.items():
                        results.append(f"{key}: {value}")

        except Exception as e:
            results.append(f'Error: {str(e)}')

    return render_template('index.html', data=results)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
