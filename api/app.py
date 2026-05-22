from flask import Flask, request, jsonify
import psycopg2, os, time

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "barangdb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "pass123")
    )

def init_db():
    retries = 5
    while retries > 0:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS barang (
                    id SERIAL PRIMARY KEY,
                    nama VARCHAR(100) NOT NULL,
                    harga INT NOT NULL
                );
            """)
            # Seed data awal jika tabel kosong
            cur.execute("SELECT COUNT(*) FROM barang;")
            count = cur.fetchone()[0]
            if count == 0:
                cur.execute("""
                    INSERT INTO barang (nama, harga) VALUES
                    ('Tas', 150000),
                    ('Sepatu', 250000),
                    ('Topi', 85000);
                """)
            conn.commit()
            cur.close()
            conn.close()
            print("Database initialized successfully.")
            break
        except Exception as e:
            print(f"DB not ready, retrying... ({e})")
            retries -= 1
            time.sleep(3)

@app.route('/barang', methods=['GET'])
def list_barang():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nama, harga FROM barang ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "nama": r[1], "harga": r[2]} for r in rows])

@app.route('/barang', methods=['POST'])
def add_barang():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO barang(nama, harga) VALUES(%s, %s) RETURNING id;",
        (data['nama'], data['harga'])
    )
    id_baru = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": id_baru, "nama": data['nama'], "harga": data['harga']}), 201

@app.route('/barang/<int:barang_id>', methods=['DELETE'])
def delete_barang(barang_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM barang WHERE id = %s;", (barang_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Barang dihapus"}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)
