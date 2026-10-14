from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
# 1. Importamos CategoriaController
from views import ClienteController, CategoriaController, ProductoController, VentaController

# Se crea UN solo controlador de cada tipo.
# Categorías se pasa a Productos para validar pertenencia.
# Clientes y Productos se pasan a Ventas (flujo 1 a 1 intacto).
clientes = ClienteController()
categorias = CategoriaController()  # <--- NUEVO CONTROLADOR
productos = ProductoController(categorias)  # <--- RECIBE A CATEGORÍAS
ventas = VentaController(clientes, productos)


# =====================================================================
# AYUDAS DE PANTALLA
# =====================================================================

def pausa():
    input("\nPresione Enter para continuar...")


def pedir_entero(etiqueta):
    """Devuelve un entero o None si el usuario escribió otra cosa."""
    try:
        return int(input(etiqueta))
    except ValueError:
        return None


def mostrar_resultado(exito, mensaje):
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def mostrar_lista(objetos, vacio="No hay registros todavía."):
    """Sirve para clientes, categorías, productos y ventas: cada modelo sabe mostrarse."""
    if not objetos:
        imprimir_info(vacio)
        return
    for objeto in objetos:
        print(f"  {objeto}")
    imprimir_info(f"Total: {len(objetos)}")


def mostrar_detalle(objeto):
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")


# =====================================================================
# MENÚ DE CLIENTES
# =====================================================================

def crear_cliente():
    imprimir_titulo("CREAR CLIENTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "telefono": input("Teléfono: "),
        "ciudad": input("Ciudad: "),
    }
    mostrar_resultado(*clientes.crear(datos))
    pausa()


def listar_clientes():
    imprimir_titulo("CLIENTES")
    mostrar_lista(clientes.leer(), "Todavía no hay clientes.")
    pausa()


def buscar_cliente():
    imprimir_titulo("BUSCAR CLIENTE")
    termino = input("Nombre, email, teléfono o ciudad: ")
    encontrados = clientes.buscar(termino)
    mostrar_lista(encontrados, f"Ningún cliente coincide con '{termino}'.")
    pausa()


def ver_cliente():
    imprimir_titulo("VER CLIENTE POR ID")
    cliente = clientes.obtener(pedir_entero("Id: "))
    if cliente is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(cliente)
    pausa()


def actualizar_cliente():
    imprimir_titulo("ACTUALIZAR CLIENTE")
    id_cliente = pedir_entero("Id: ")
    cliente = clientes.obtener(id_cliente)
    if cliente is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Editando: {cliente.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "apellido", "email", "telefono", "ciudad"):
        actual = getattr(cliente, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    mostrar_resultado(*clientes.actualizar(id_cliente, cambios))
    pausa()


def eliminar_cliente():
    imprimir_titulo("ELIMINAR CLIENTE")
    id_cliente = pedir_entero("Id: ")
    cliente = clientes.obtener(id_cliente)
    if cliente is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Se eliminará: {cliente.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*clientes.eliminar(id_cliente))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ DE CATEGORÍAS (NUEVO)
# =====================================================================

def crear_categoria():
    imprimir_titulo("CREAR CATEGORÍA")
    datos = {
        "nombre": input("Nombre: "),
        "descripcion": input("Descripción (opcional): "),
    }
    mostrar_resultado(*categorias.crear(datos))
    pausa()


def listar_categorias():
    imprimir_titulo("CATEGORÍAS")
    mostrar_lista(categorias.leer(), "Todavía no hay categorías.")
    pausa()


def buscar_categoria():
    imprimir_titulo("BUSCAR CATEGORÍA")
    termino = input("Nombre o descripción: ")
    encontrados = categorias.buscar(termino)
    mostrar_lista(encontrados, f"Ninguna categoría coincide con '{termino}'.")
    pausa()


def ver_categoria():
    imprimir_titulo("VER CATEGORÍA POR ID")
    categoria = categorias.obtener(pedir_entero("Id: "))
    if categoria is None:
        imprimir_error("No encontrada")
    else:
        mostrar_detalle(categoria)
        # Mostrar qué productos pertenecen a esta categoría
        prods = productos.por_categoria(categoria.id)
        print(f"\n  Productos en esta categoría ({len(prods)}):")
        for p in prods:
            print(f"    - {p.nombre} (${p.precio:.2f})")
    pausa()


def actualizar_categoria():
    imprimir_titulo("ACTUALIZAR CATEGORÍA")
    id_cat = pedir_entero("Id: ")
    categoria = categorias.obtener(id_cat)
    if categoria is None:
        imprimir_error("No encontrada")
        return pausa()

    imprimir_info(f"Editando: {categoria.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "descripcion"):
        actual = getattr(categoria, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    mostrar_resultado(*categorias.actualizar(id_cat, cambios))
    pausa()


def eliminar_categoria():
    imprimir_titulo("ELIMINAR CATEGORÍA")
    id_cat = pedir_entero("Id: ")
    categoria = categorias.obtener(id_cat)
    if categoria is None:
        imprimir_error("No encontrada")
        return pausa()

    # Aviso si hay productos que la usan
    asociados = productos.por_categoria(id_cat)
    if asociados:
        imprimir_info(f"Aviso: Hay {len(asociados)} producto(s) asignado(s) a esta categoría.")

    imprimir_info(f"Se eliminará: {categoria.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*categorias.eliminar(id_cat))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ DE PRODUCTOS
# =====================================================================

def crear_producto():
    imprimir_titulo("CREAR PRODUCTO")
    
    # Mostramos categorías existentes para facilitar la selección
    imprimir_info("Categorías disponibles:")
    mostrar_lista(categorias.leer(), "No hay categorías registradas (se creará sin categoría).")

    datos = {
        "nombre": input("\nNombre: "),
        "precio": input("Precio: "),
        "stock": input("Stock: "),
        "categoria_id": pedir_entero("Id de categoría (dejar 0 o vacío si no tiene): ") or 0,
    }
    mostrar_resultado(*productos.crear(datos))
    pausa()


def listar_productos():
    imprimir_titulo("PRODUCTOS")
    mostrar_lista(productos.leer(), "Todavía no hay productos.")
    pausa()


def buscar_producto():
    imprimir_titulo("BUSCAR PRODUCTO")
    termino = input("Nombre: ")
    mostrar_lista(productos.buscar(termino), "Sin coincidencias.")
    pausa()


def ver_producto():
    imprimir_titulo("VER PRODUCTO POR ID")
    producto = productos.obtener(pedir_entero("Id: "))
    if producto is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(producto)
        # Mostrar el nombre real de la categoría asociada
        cat = categorias.obtener(producto.categoria_id) if producto.categoria_id else None
        print(f"  Categoría       : {cat.nombre if cat else 'Sin categoría'}")
        imprimir_info(f"Precio con IVA: ${producto.con_iva(producto.precio):.2f}")
    pausa()


def actualizar_producto():
    imprimir_titulo("ACTUALIZAR PRODUCTO")
    id_producto = pedir_entero("Id: ")
    producto = productos.obtener(id_producto)
    if producto is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Editando: {producto.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "precio", "stock"):
        actual = getattr(producto, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    # Opción para actualizar categoría
    cambiar_cat = input(f"Categoria ID [{producto.categoria_id}]: ").strip()
    if cambiar_cat:
        try:
            cambios["categoria_id"] = int(cambiar_cat)
        except ValueError:
            imprimir_error("El ID de categoría debe ser numérico")
            return pausa()

    mostrar_resultado(*productos.actualizar(id_producto, cambios))
    pausa()


def eliminar_producto():
    imprimir_titulo("ELIMINAR PRODUCTO")
    id_producto = pedir_entero("Id: ")
    producto = productos.obtener(id_producto)
    if producto is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Se eliminará: {producto.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*productos.eliminar(id_producto))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ DE VENTAS (1 A 1 INTACTO)
# =====================================================================

def registrar_venta():
    imprimir_titulo("REGISTRAR VENTA")
    imprimir_info("Clientes:")
    mostrar_lista(clientes.leer())
    imprimir_info("Productos:")
    mostrar_lista(productos.leer())

    datos = {
        "cliente_id": pedir_entero("\nId del cliente: "),
        "producto_id": pedir_entero("Id del producto: "),
        "cantidad": pedir_entero("Cantidad: "),
    }
    if None in datos.values():
        imprimir_error("Todos los datos deben ser números enteros")
        return pausa()

    mostrar_resultado(*ventas.crear(datos))
    pausa()


def listar_ventas():
    imprimir_titulo("VENTAS")
    mostrar_lista(ventas.leer(), "Todavía no hay ventas.")
    pausa()


def ver_comprobante():
    imprimir_titulo("COMPROBANTE")
    texto = ventas.comprobante(pedir_entero("Id de la venta: "))
    if texto is None:
        imprimir_error("No existe esa venta")
    else:
        print(texto)
    pausa()


def anular_venta():
    imprimir_titulo("ANULAR VENTA")
    id_venta = pedir_entero("Id de la venta: ")
    if id_venta and confirmar("Se devolverá el stock. ¿Confirma?"):
        mostrar_resultado(*ventas.eliminar(id_venta))
    else:
        imprimir_info("Operación cancelada")
    pausa()


def resumen():
    imprimir_titulo("RESUMEN")
    print(f"  Clientes   : {len(clientes.leer())}")
    print(f"  Ciudades   : {', '.join(clientes.ciudades()) or '-'}")
    print(f"  Categorías : {len(categorias.leer())}")
    print(f"  Productos  : {len(productos.leer())}")
    bajos = productos.con_stock_bajo()
    print(f"  Stock bajo : {', '.join(p.nombre for p in bajos) or 'ninguno'}")
    print(f"  Ventas     : {len(ventas.leer())}")
    print(f"  Vendido    : ${ventas.total_vendido():.2f}")
    pausa()


# =====================================================================
# MENÚS: DICCIONARIOS tecla -> (texto, función)
# =====================================================================

MENU_CLIENTES = {
    "1": ("Crear cliente", crear_cliente),
    "2": ("Ver todos", listar_clientes),
    "3": ("Buscar", buscar_cliente),
    "4": ("Ver por id", ver_cliente),
    "5": ("Actualizar", actualizar_cliente),
    "6": ("Eliminar", eliminar_cliente),
    "0": ("Volver", None),
}

MENU_CATEGORIAS = {
    "1": ("Crear categoría", crear_categoria),
    "2": ("Ver todas", listar_categorias),
    "3": ("Buscar", buscar_categoria),
    "4": ("Ver por id", ver_categoria),
    "5": ("Actualizar", actualizar_categoria),
    "6": ("Eliminar", eliminar_categoria),
    "0": ("Volver", None),
}

MENU_PRODUCTOS = {
    "1": ("Crear producto", crear_producto),
    "2": ("Ver todos", listar_productos),
    "3": ("Buscar", buscar_producto),
    "4": ("Ver por id", ver_producto),
    "5": ("Actualizar", actualizar_producto),
    "6": ("Eliminar", eliminar_producto),
    "0": ("Volver", None),
}

MENU_VENTAS = {
    "1": ("Registrar venta", registrar_venta),
    "2": ("Ver todas", listar_ventas),
    "3": ("Ver comprobante", ver_comprobante),
    "4": ("Anular venta", anular_venta),
    "0": ("Volver", None),
}


def ejecutar_menu(titulo, opciones):
    while True:
        imprimir_titulo(titulo)
        for tecla, (texto, _funcion) in opciones.items():
            print(f"  {tecla}. {texto}")
        print()

        tecla = input("Opción: ").strip()
        if tecla not in opciones:
            imprimir_error("Opción no válida")
            pausa()
            continue

        _texto, funcion = opciones[tecla]
        if funcion is None:
            break
        funcion()


def main():
    while True:
        imprimir_titulo("SISTEMA DE VENTAS")
        print("  1. Clientes")
        print("  2. Categorías")     # <--- NUEVA OPCIÓN
        print("  3. Productos")
        print("  4. Ventas")
        print("  5. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1":
            ejecutar_menu("CLIENTES", MENU_CLIENTES)
        elif tecla == "2":
            ejecutar_menu("CATEGORÍAS", MENU_CATEGORIAS)
        elif tecla == "3":
            ejecutar_menu("PRODUCTOS", MENU_PRODUCTOS)
        elif tecla == "4":
            ejecutar_menu("VENTAS", MENU_VENTAS)
        elif tecla == "5":
            resumen()
        elif tecla == "0":
            imprimir_info("¡Hasta luego! 👋")
            break
        else:
            imprimir_error("Opción no válida")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")