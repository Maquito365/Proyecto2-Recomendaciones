import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from neo4j import GraphDatabase

class VibesRecommender:
    def __init__(self, uri, user, password):
        # Inicializa la conexión con la base de datos de Neo4j
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Cierra la conexión
        self.driver.close()

    def get_content_based_recommendations(self, id_usuario):
        """
        Algoritmo VIBES - Filtrado por Contenido con Ponderación de Pesos.
        """
        query = """
        // 1. Obtener el historial del usuario
        MATCH (u:Usuario {nombre: $usuario})-[:ESCUCHA]->(escuchada:Cancion)
        
        // 2 y 3. Extraer características y buscar candidatas simultáneamente
        MATCH (escuchada)-[:COMPUESTA_POR|PERTENECE_A]->(caracteristica)<-[:COMPUESTA_POR|PERTENECE_A]-(candidata:Cancion)
        
        // 4. Filtrar canciones que el usuario YA escuchó
        WHERE NOT (u)-[:ESCUCHA]->(candidata)
        
        // Asignar PESOS según el tipo de coincidencia (Design Thinking)
        // Decisión Arquitectónica: Un artista idéntico tiene más peso que un género idéntico.
        WITH candidata, caracteristica,
          CASE 
            WHEN "Artista" IN labels(caracteristica) THEN 3 // Coincidir en artista vale 3 puntos
            WHEN "Genero" IN labels(caracteristica) THEN 1  // Coincidir en género vale 1 punto
            ELSE 0
          END AS peso
          
        // 5. Sumar el score total por candidata y retornar
        RETURN candidata.titulo AS CancionRecomendada, sum(peso) AS PuntuacionRelevancia
        ORDER BY PuntuacionRelevancia DESC
        LIMIT 10
        """

        with self.driver.session() as session:
            result = session.run(query, usuario=id_usuario)
            records = list(result)
            
            # Manejo del "Cold Start" a nivel de lógica de aplicación
            # Si la lista de records está vacía, el usuario no existe o no ha escuchado nada
            if not records:
                 return {"status": "Cold Start", "mensaje": "Usuario sin historial. Mostrando Top 50 Global (Fallback)."}
                 
            recomendaciones = []
            for record in records:
                recomendaciones.append({
                    "cancion": record["CancionRecomendada"],
                    "score": record["PuntuacionRelevancia"]
                })
                
            return {"status": "Success", "recomendaciones": recomendaciones}

# ==========================================
# Zona de Pruebas (Ejecución local)
# ==========================================
if __name__ == "__main__":
    print("🎵 Iniciando Motor de Recomendaciones VIBES...")
    
    # === CONEXIÓN A NEO4J (100% PORTABLE) ===
    # Para que funcione en la PC de todos tus compañeros sin instalar absolutamente nada,
    # la mejor práctica es usar la nube gratuita de Neo4j (AuraDB).
    # Obtén estas credenciales gratis en: https://console.neo4j.io
    URI = "neo4j+s://d544acc5.databases.neo4j.io"
    USER = "d544acc5"
    PASSWORD = "3JdyXlKfIxftHD0U9-jMTni7_DWovV10M2TNscwVU1k" 
    
    try:
        app = VibesRecommender(URI, USER, PASSWORD)
        
        usuario_prueba = "Marco Soloj"
        print(f"\n🔍 Buscando recomendaciones para: {usuario_prueba}...")
        
        resultados = app.get_content_based_recommendations(usuario_prueba)
        
        import json
        print(json.dumps(resultados, indent=2, ensure_ascii=False))
        
        app.close()
    except Exception as e:
        print(f"\n❌ Error al conectar con Neo4j.")
        print("Asegúrate de que la base de datos esté iniciada y las credenciales sean correctas.")
        print(f"Detalle técnico: {e}")
