import 'package:flutter/material.dart';
import 'services/api_service.dart';
import 'models/estacion.dart';

void main() => runApp(const SMATApp());

class SMATApp extends StatelessWidget {
  const SMATApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SMAT',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const HomePage(), 
      debugShowCheckedModeBanner: false
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late Future<List<Estacion>> futureEstaciones;

  @override
  void initState() {
    super.initState();
    _cargarDatos(); // Cargamos los datos por primera vez al abrir la app
  }

  // --- SOLUCIÓN AL RETO: Lógica de Refresco ---
  void _cargarDatos() {
    setState(() {
      futureEstaciones = ApiService().fetchEstaciones();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('SMAT - Monitoreo Móvil'),
        backgroundColor: Colors.blue[800],
        foregroundColor: Colors.white,
      ),
      body: FutureBuilder<List<Estacion>>(
        future: futureEstaciones,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(
              child: Text(
                'X Error de conexión\nAsegúrate de que el backend esté corriendo en el puerto 8000',
                textAlign: TextAlign.center,
                style: const TextStyle(color: Colors.red),
              )
            );
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('No hay estaciones registradas.'));
          } else {
            return ListView.builder(
              itemCount: snapshot.data!.length,
              itemBuilder: (context, index) {
                final est = snapshot.data![index];
                return Card(
                  margin: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                  child: ListTile(
                    leading: const Icon(Icons.satellite_alt, color: Colors.blue),
                    title: Text(est.nombre, style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Text(est.ubicacion),
                  ),
                );
              },
            );
          }
        },
      ),
      // --- SOLUCIÓN AL RETO: Botón Flotante ---
      floatingActionButton: FloatingActionButton(
        onPressed: _cargarDatos,
        backgroundColor: Colors.blue[800],
        foregroundColor: Colors.white,
        tooltip: 'Actualizar',
        child: const Icon(Icons.refresh),
      ),
    );
  }
}