// ==========================================
// Script Cypher: Creación de Nodos y Relaciones para el Proyecto VIBES
// ==========================================

// 1. Limpiar base de datos (Ejecutar solo si quieres borrar todo lo existente antes de crear)
MATCH (n) DETACH DELETE n;

// 2. Crear Nodos
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
  (dieremix:Cancion {titulo: "Die For You (Remix)"})

// 3. Crear Relaciones (El ADN del grafo)
CREATE
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
  (dieremix)-[:PERTENECE_A]->(rnb);
