import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from neo4j import GraphDatabase

def poblar_base_de_datos(uri, user, password):
    # Conectarse a Neo4j
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    with driver.session() as session:
        print("🧹 Borrando base de datos anterior (Limpiando grafo)...")
        session.run("MATCH (n) DETACH DELETE n")
        
        print("🌱 Creando los Nodos (Usuarios, Artistas, Géneros, Canciones)...")
        print("🔗 Construyendo las Relaciones (El Historial y ADN de Recomendación)...")
        
        create_query = """
        CREATE 
          // Usuarios
          (marco:Usuario {nombre: "Marco Soloj"}),
          
          // Artistas
          (weeknd:Artista {nombre: "The Weeknd"}),
          (metro:Artista {nombre: "Metro Boomin"}),
          (dua:Artista {nombre: "Dua Lipa"}),
          (ariana:Artista {nombre: "Ariana Grande"}),
          
          // Géneros
          (pop:Genero {nombre: "Pop"}),
          (rnb:Genero {nombre: "R&B"}),
          (synth:Genero {nombre: "Synthpop"}),
          
          // Canciones (Historial)
          (starboy:Cancion {titulo: "Starboy"}),
          (die:Cancion {titulo: "Die For You"}),
          (save:Cancion {titulo: "Save Your Tears"}),
          
          // Canciones (Catálogo para recomendar)
          (blinding:Cancion {titulo: "Blinding Lights"}),
          (creepin:Cancion {titulo: "Creepin'"}),
          (levitating:Cancion {titulo: "Levitating"}),
          (dieremix:Cancion {titulo: "Die For You (Remix)"}),
          
          // RELACIONES
          // Historial de Escuchas de Marco
          (marco)-[:ESCUCHA]->(starboy),
          (marco)-[:ESCUCHA]->(die),
          (marco)-[:ESCUCHA]->(save),
          
          // Conexiones de las canciones escuchadas
          (starboy)-[:COMPUESTA_POR]->(weeknd),
          (starboy)-[:PERTENECE_A]->(rnb),
          (starboy)-[:PERTENECE_A]->(pop),
          
          (die)-[:COMPUESTA_POR]->(weeknd),
          (die)-[:PERTENECE_A]->(rnb),
          
          (save)-[:COMPUESTA_POR]->(weeknd),
          (save)-[:PERTENECE_A]->(synth),
          
          // Conexiones del Catálogo a recomendar
          (blinding)-[:COMPUESTA_POR]->(weeknd),
          (blinding)-[:PERTENECE_A]->(synth),
          
          (creepin)-[:COMPUESTA_POR]->(metro),
          (creepin)-[:COMPUESTA_POR]->(weeknd),
          (creepin)-[:PERTENECE_A]->(rnb),
          
          (levitating)-[:COMPUESTA_POR]->(dua),
          (levitating)-[:PERTENECE_A]->(pop),
          (levitating)-[:PERTENECE_A]->(synth),
          
          (dieremix)-[:COMPUESTA_POR]->(weeknd),
          (dieremix)-[:COMPUESTA_POR]->(ariana),
          (dieremix)-[:PERTENECE_A]->(rnb)
        """
        
        session.run(create_query)
        print("✅ ¡Base de datos VIBES creada con éxito! El sistema de recomendación ya tiene datos.")
        
    driver.close()

if __name__ == "__main__":
    print("🚀 Script de Inicialización de VIBES")
    
    # === CONEXIÓN A NEO4J (100% PORTABLE) ===
    # Para que funcione en la PC de todos tus compañeros sin instalar absolutamente nada,
    # la mejor práctica es usar la nube gratuita de Neo4j (AuraDB).
    # Obtén estas credenciales gratis en: https://console.neo4j.io
    URI = "neo4j+s://d544acc5.databases.neo4j.io"
    URI = "neo4j+s://d544acc5.databases.neo4j.io"
    USER = "d544acc5"
    PASSWORD = "3JdyXlKfIxftHD0U9-jMTni7_DWovV10M2TNscwVU1k" 
    
    try:
        poblar_base_de_datos(URI, USER, PASSWORD)
    except Exception as e:
        print(f"\n❌ Error al intentar crear la base de datos: {e}")
        print("💡 Verifica que Neo4j esté corriendo y la contraseña sea correcta.")
