from flask import Flask, jsonify, request
import os

app = Flask(__name__)

productos = [
    {"id": 1, "nombre": "Matrícula", "precio": 2000},
    {"id": 2, "nombre": "Arancel", "precio": 1000}
]

@app.route('/')
def inicio():
    return "Hola profe, la API está corriendo bien."

@app.route('/productos', methods=['GET'])
def obtener_productos():
    return jsonify(productos)

@app.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = next((p for p in productos if p["id"] == id), None)
    if producto:
        return jsonify(producto)
    return jsonify({"mensaje": "No se encontró el producto"}), 404

@app.route('/productos', methods=['POST'])
def agregar_producto():
    nuevo = request.get_json()
    if not nuevo.get("id") or not nuevo.get("nombre") or not nuevo.get("precio"):
        return jsonify({"mensaje": "Faltan datos: id, nombre o precio"}), 400
    productos.append(nuevo)
    return jsonify({"mensaje": "Producto agregado", "producto": nuevo}), 201

@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    global productos
    productos_actualizados = [p for p in productos if p["id"] != id]
    if len(productos_actualizados) == len(productos):
        return jsonify({"mensaje": "No se encontró el producto para eliminar"}), 404
    productos = productos_actualizados
    return jsonify({"mensaje": f"Producto con ID {id} eliminado"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))