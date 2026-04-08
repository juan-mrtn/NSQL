from redis import Redis
from flask import Flask, render_template, request, redirect, url_for, flash


r = Redis(host='localhost', port=6379, decode_responses=True)

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def inicializar_db():
    """Carga los capítulos en listas de Redis si no existen [cite: 19, 23]"""
    # Temporada 1
    if r.llen("temporada:1") == 0:
        r.lpush("temporada:1", 
                "Capitulo 8: Redencion", "Capitulo 7: El ajuste de cuentas", 
                "Capitulo 6: El prisionero", "Capitulo 5: El pistolero", 
                "Capitulo 4: Santuario", "Capitulo 3: El pecado", 
                "Capitulo 2: El niño", "Capitulo 1: El mandaloriano")

    # Temporada 2
    if r.llen("temporada:2") == 0:
        r.lpush("temporada:2", 
                "Capitulo 16: El rescate", "Capitulo 15: El creyente", 
                "Capitulo 14: La tragedia", "Capitulo 13: La Jedi", 
                "Capitulo 12: El asedio", "Capitulo 11: La heredera", 
                "Capitulo 10: La pasajera", "Capitulo 9: El mariscal")

    # Temporada 3
    if r.llen("temporada:3") == 0:
        r.lpush("temporada:3", 
                "Capitulo 24: El regreso", "Capitulo 23: Los espias", 
                "Capitulo 22: Pistoleros a sueldo", "Capitulo 21: El pirata", 
                "Capitulo 20: El huerfano", "Capitulo 19: El converso", 
                "Capitulo 18: Las minas de Mandalore", "Capitulo 17: El apostata")

@app.route('/')
def index():
    catalogo_visual = {}
    temporadas = {
        "Temporada 1 (2019)": "temporada:1",
        "Temporada 2 (2020)": "temporada:2",
        "Temporada 3 (2023)": "temporada:3"
    }
    
    for nombre, redis_key in temporadas.items():
        titulos = r.lrange(redis_key, 0, -1)
        catalogo_visual[nombre] = []

        for titulo in titulos:
            estado = r.get(f"estado:{titulo}") or "Disponible"
            catalogo_visual[nombre].append({
                "titulo": titulo,
                "estado": estado
            })
            
    return render_template('index.html', catalogo=catalogo_visual)

@app.route('/reservar', methods=['POST'])
def reservar():
    titulo = request.form.get('titulo')
    if not r.exists(f"estado:{titulo}"):
        r.setex(f"estado:{titulo}", 240, "Reservado (Pendiente de Pago)")
        flash(f"'{titulo}' reservado por 4 min.", "warning")
    else:
        flash("Capítulo no disponible.", "danger")
    return redirect(url_for('index'))

@app.route('/pagar', methods=['POST'])
def pagar():
    titulo = request.form.get('titulo')
    precio = request.form.get('precio')
    r.setex(f"mando:estado:{titulo}", 86400, "Alquilado")
    flash(f"Pago de ${precio} recibido. '{titulo}' alquilado por 24hs.", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    inicializar_db()
    app.run(host='0.0.0.0', port=5000, debug=True)