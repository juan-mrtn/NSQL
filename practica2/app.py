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
                "Capítulo 8: Redención", "Capítulo 7: El ajuste de cuentas", 
                "Capítulo 6: El prisionero", "Capítulo 5: El pistolero", 
                "Capítulo 4: Santuario", "Capítulo 3: El pecado", 
                "Capítulo 2: El niño", "Capítulo 1: El mandaloriano")

    # Temporada 2
    if r.llen("temporada:2") == 0:
        r.lpush("temporada:2", 
                "Capítulo 16: El rescate", "Capítulo 15: El creyente", 
                "Capítulo 14: La tragedia", "Capítulo 13: La Jedi", 
                "Capítulo 12: El asedio", "Capítulo 11: La heredera", 
                "Capítulo 10: La pasajera", "Capítulo 9: El mariscal")

    # Temporada 3
    if r.llen("temporada:3") == 0:
        r.lpush("temporada:3", 
                "Capítulo 24: El regreso", "Capítulo 23: Los espías", 
                "Capítulo 22: Pistoleros a sueldo", "Capítulo 21: El pirata", 
                "Capítulo 20: El huérfano", "Capítulo 19: El converso", 
                "Capítulo 18: Las minas de Mandalore", "Capítulo 17: El apóstata")

@app.route('/')
def index():
    catalogo_visual = {}
    temporadas = {
        "Temporada 1 (2019)": "temporada:1",
        "Temporada 2 (2020)": "temporada:2",
        "Temporada 3 (2023)": "temporada:3"
    }
    
    for nombre, redis_key in temporadas.items():
        # Obtenemos la lista completa con LRANGE 
        titulos = r.lrange(redis_key, 0, -1)
        catalogo_visual[nombre] = []

        for titulo in titulos:
            # Consultamos el estado temporal (SETEX)
            estado = r.get(f"estado:{titulo}") or "Disponible"
            catalogo_visual[nombre].append({
                "titulo": titulo,
                "estado": estado
            })
            
    return render_template('index.html', catalogo=catalogo_visual)

@app.route('/reservar', methods=['POST'])
def reservar():
    titulo = request.form.get('titulo')
    # 2. Reserva por 4 minutos (240 segundos) si no está ocupado [cite: 65]
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
    # 3. Confirmar pago y registrar alquiler por 24 hs (86400 segundos) [cite: 66]
    r.setex(f"mando:estado:{titulo}", 86400, "Alquilado")
    flash(f"Pago de ${precio} recibido. '{titulo}' alquilado por 24hs.", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    inicializar_db()
    app.run(host='0.0.0.0', port=5000, debug=True)