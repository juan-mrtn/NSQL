from redis import Redis
from flask import Flask, render_template, request, redirect, url_for, flash


r = Redis(host='localhost', port=6379, decode_responses=True)

app = Flask(__name__)
app.secret_key = 'supersecretkey'


TEMPORADAS = {
    "Temporada 1 (2019)": {
        1: "Capítulo 1: El mandaloriano", 2: "Capítulo 2: El niño", 3: "Capítulo 3: El pecado",
        4: "Capítulo 4: Santuario", 5: "Capítulo 5: El pistolero", 6: "Capítulo 6: El prisionero",
        7: "Capítulo 7: El ajuste de cuentas", 8: "Capítulo 8: Redención"
    },
    "Temporada 2 (2020)": {
        9: "Capítulo 9: El mariscal", 10: "Capítulo 10: La pasajera", 11: "Capítulo 11: La heredera",
        12: "Capítulo 12: El asedio", 13: "Capítulo 13: La Jedi", 14: "Capítulo 14: La tragedia",
        15: "Capítulo 15: El creyente", 16: "Capítulo 16: El rescate"
    },
    "Temporada 3 (2023)": {
        17: "Capítulo 17: El apóstata", 18: "Capítulo 18: Las minas de Mandalore", 19: "Capítulo 19: El converso",
        20: "Capítulo 20: El huérfano", 21: "Capítulo 21: El pirata", 22: "Capítulo 22: Pistoleros a sueldo",
        23: "Capítulo 23: Los espías", 24: "Capítulo 24: El regreso"
    }
}

@app.route('/')
def index():
    # 1. Ruta para listar los capítulos e indicar su estado agrupado por temporada [cite: 64]
    catalogo = {}
    
    for nombre_temp, capitulos in TEMPORADAS.items():
        catalogo[nombre_temp] = [] # Inicializamos la lista para esta temporada
        
        for cap_id, titulo in capitulos.items():
            # Consultamos el estado en Redis
            estado = r.get(f"mando:cap:{cap_id}:estado")
            
            if not estado:
                estado = "Disponible"
                
            catalogo[nombre_temp].append({
                "id": cap_id,
                "titulo": titulo,
                "estado": estado
            })
            
    return render_template('index.html', catalogo=catalogo)

@app.route('/reservar/<int:cap_id>', methods=['POST'])
def reservar(cap_id):
    # 2. Alquilar deja reservado por 4 minutos [cite: 65]
    estado_actual = r.get(f"mando:cap:{cap_id}:estado")
    if not estado_actual:
        r.setex(f"mando:cap:{cap_id}:estado", 240, "Reservado (Pendiente de Pago)")
        flash(f"Capítulo {cap_id} reservado por 4 minutos.", "warning")
    else:
        flash("El capítulo no está disponible.", "danger")
    return redirect(url_for('index'))

@app.route('/pagar', methods=['POST'])
def pagar():
    # 3. Ruta para confirmar pago y registrar alquiler por 24 hs [cite: 66]
    cap_id = request.form.get('cap_id')
    precio = request.form.get('precio')
    
    estado_actual = r.get(f"mando:cap:{cap_id}:estado")
    
    if estado_actual != "Alquilado":
        r.setex(f"mando:cap:{cap_id}:estado", 86400, "Alquilado")
        flash(f"Pago de ${precio} confirmado. Capítulo {cap_id} alquilado por 24hs.", "success")
    else:
        flash("El capítulo ya se encuentra alquilado.", "danger")
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)