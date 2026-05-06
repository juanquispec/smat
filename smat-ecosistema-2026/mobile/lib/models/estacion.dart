class Estacion {
  final int id;
  final String nombre;
  final String ubicacion;

  Estacion({required this.id, required this.nombre, required this.ubicacion});

  // Factory para convertir el JSON que viene del Backend a un objeto Dart
  factory Estacion.fromJson(Map<String, dynamic> json) {
    return Estacion(
      id: json['id'],
      nombre: json['nombre'],
      ubicacion: json['ubicacion'],
    );
  }
}