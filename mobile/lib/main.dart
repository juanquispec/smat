import 'package:flutter/material.dart';
import 'services/api_service.dart';
import 'models/estacion.dart';

void main() => runApp(const SMATApp());

class SMATApp extends StatelessWidget {
  const SMATApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: const HomePage(),
      debugShowCheckedModeBanner: false,
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
    futureEstaciones = ApiService().fetchEstaciones();
  }

  // 🔁 Reto: refrescar datos
  void _refreshEstaciones() {
    setState(() {
      futureEstaciones = ApiService().fetchEstaciones();
    });
  }

  // ✏️ Editar estación
  void _mostrarDialogoEdicion(Estacion est) {
    final nombreCtrl = TextEditingController(text: est.nombre);
    final ubicacionCtrl = TextEditingController(text: est.ubicacion);

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text("Editar Estación"),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: nombreCtrl,
              decoration: const InputDecoration(labelText: "Nombre"),
            ),
            TextField(
              controller: ubicacionCtrl,
              decoration: const InputDecoration(labelText: "Ubicación"),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text("Cancelar"),
          ),
          ElevatedButton(
            onPressed: () async {
              bool ok = await ApiService().editarEstacion(
                est.id,
                nombreCtrl.text,
                ubicacionCtrl.text,
              );
              if (ok) {
                Navigator.pop(context);
                _refreshEstaciones();
              }
            },
            child: const Text("Guardar"),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('SMAT - Monitoreo Móvil')),

      body: FutureBuilder<List<Estacion>>(
        future: futureEstaciones,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            // ⏳ Indicador de carga (reto)
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return const Center(child: Text('❌ Error de conexión'));
          } else {
            return RefreshIndicator(
              onRefresh: () async => _refreshEstaciones(),
              child: ListView.builder(
                itemCount: snapshot.data!.length,
                itemBuilder: (context, index) {
                  final est = snapshot.data![index];

                  return Dismissible(
                    key: Key(est.id.toString()),
                    direction: DismissDirection.endToStart,
                    background: Container(
                      color: Colors.red,
                      alignment: Alignment.centerRight,
                      padding: const EdgeInsets.only(right: 20),
                      child: const Icon(Icons.delete, color: Colors.white),
                    ),
                    onDismissed: (_) async {
                      bool ok =
                          await ApiService().eliminarEstacion(est.id);
                      if (ok) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content:
                                Text("${est.nombre} eliminada"),
                          ),
                        );
                        _refreshEstaciones();
                      }
                    },
                    child: ListTile(
                      leading: Icon(
                        Icons.satellite_alt,
                        color:
                            est.valor < 50 ? Colors.green : Colors.red,
                      ),
                      title: Text(est.nombre),
                      subtitle: Text(est.ubicacion),
                      onTap: () => _mostrarDialogoEdicion(est),
                    ),
                  );
                },
              ),
            );
          }
        },
      ),

      // 🔘 Botón flotante (reto)
      floatingActionButton: FloatingActionButton(
        onPressed: _refreshEstaciones,
        child: const Icon(Icons.refresh),
      ),
    );
  }
}