from flask import Flask, render_template, request, redirect, url_for
import requests, os

app = Flask(__name__)
API_URL = os.getenv("API_URL", "http://api:8080")

@app.route('/')
def index():
    try:
        resp = requests.get(f"{API_URL}/barang", timeout=5)
        barang_list = resp.json()
    except Exception as e:
        barang_list = []
        print(f"Error fetching data: {e}")
    return render_template('index.html', barang_list=barang_list)

@app.route('/tambah', methods=['POST'])
def tambah():
    nama = request.form.get('nama')
    harga = request.form.get('harga')
    try:
        requests.post(f"{API_URL}/barang",
                      json={"nama": nama, "harga": int(harga)},
                      timeout=5)
    except Exception as e:
        print(f"Error adding item: {e}")
    return redirect(url_for('index'))

@app.route('/hapus/<int:barang_id>', methods=['POST'])
def hapus(barang_id):
    try:
        requests.delete(f"{API_URL}/barang/{barang_id}", timeout=5)
    except Exception as e:
        print(f"Error deleting item: {e}")
    return redirect(url_for('index'))

# Proxy API untuk akses dari luar (digunakan curl test)
@app.route('/api/barang', methods=['GET', 'POST'])
def proxy_barang():
    if request.method == 'GET':
        resp = requests.get(f"{API_URL}/barang", timeout=5)
        return resp.json()
    else:
        data = request.get_json()
        resp = requests.post(f"{API_URL}/barang", json=data, timeout=5)
        return resp.json(), resp.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
