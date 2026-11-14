"""
Routing Service: Simulates pedestrian cool & shaded paths in Rome.
Calculates shade coverage, surface temperature delta, and thermal comfort scores.
"""

SCENARIOS = {
    "colosseo_navona": {
        "title": "Centro Storico: Colosseo ➔ Piazza Navona",
        "description": "Attraversamento del centro storico di Roma. Confronta la via trafficata e assolata con i vicoli storici e i parchi ombrosi del Rione Monti e Regola.",
        "center": [41.8945, 12.4820],
        "zoom": 15,
        "direct_route": {
            "name": "Percorso Diretto al Sole (Via dei Fori / C.so Vittorio)",
            "color": "#E43700", # Rocket Red
            "distance_km": 2.2,
            "walk_time_min": 28,
            "shade_percent": 14,
            "avg_temp_c": 39.5,
            "heat_stress": "Molto Alto (Zona Rossa UHI)",
            "surface_type": "Asfalto & Pavimentazione continua priva di chiome arboree",
            "waypoints": [
                [41.8902, 12.4922], # Colosseo
                [41.8925, 12.4880], # Fori Imperiali
                [41.8955, 12.4823], # Piazza Venezia
                [41.8962, 12.4770], # Largo di Torre Argentina
                [41.8972, 12.4740], # C.so Vittorio Emanuele
                [41.8992, 12.4731]  # Piazza Navona
            ]
        },
        "cool_route": {
            "name": "Percorso Fresco & Ombreggiato (Rione Monti / Vicoli Storici)",
            "color": "#00F0FF", # Neon Cyan / Cool Blue
            "distance_km": 2.5,
            "walk_time_min": 32,
            "shade_percent": 74,
            "avg_temp_c": 30.6,
            "heat_stress": "Basso / Moderato (Comfort Ottimale)",
            "surface_type": "Vicoli stretti ad alto rapporto H/W (ombra da edifici) + Parchi",
            "waypoints": [
                [41.8902, 12.4922], # Colosseo
                [41.8920, 12.4935], # Parco del Colle Oppio (Alberi)
                [41.8942, 12.4900], # Salita dei Borgia (Ombra edifici)
                [41.8950, 12.4870], # Via Baccina (Rione Monti ombroso)
                [41.8940, 12.4810], # Vicoli verso il Ghetto
                [41.8930, 12.4760], # Portico d'Ottavia
                [41.8955, 12.4725], # Campo de' Fiori (Vie strette)
                [41.8980, 12.4728], # Via del Governo Vecchio
                [41.8992, 12.4731]  # Piazza Navona
            ]
        }
    },
    "termini_borghese": {
        "title": "Oasi Verde: Stazione Termini ➔ Villa Borghese",
        "description": "Dalla principale stazione ferroviaria romana al polmone verde di Villa Borghese, evitando l'isola di calore dell'asfalto urbano.",
        "center": [41.9070, 12.4950],
        "zoom": 15,
        "direct_route": {
            "name": "Percorso Diretto al Sole (Via Cernaia / XX Settembre)",
            "color": "#E43700",
            "distance_km": 2.3,
            "walk_time_min": 30,
            "shade_percent": 18,
            "avg_temp_c": 40.8,
            "heat_stress": "Estremo (Canyon Stradale Esposto)",
            "surface_type": "Asfalto continuo, riverbero da facciate in travertino",
            "waypoints": [
                [41.9014, 12.5015], # Termini
                [41.9038, 12.4980], # Piazza della Repubblica
                [41.9065, 12.4935], # Via XX Settembre
                [41.9080, 12.4910], # Corso d'Italia
                [41.9125, 12.4880]  # Villa Borghese Pinciana
            ]
        },
        "cool_route": {
            "name": "Percorso Fresco (Giardini Terme ➔ Viale Alberato Veneto ➔ Parco)",
            "color": "#00F0FF",
            "distance_km": 2.6,
            "walk_time_min": 34,
            "shade_percent": 78,
            "avg_temp_c": 29.9,
            "heat_stress": "Basso (Oasi Microclimatica)",
            "surface_type": "Viali con pini marittimi e chioma continua",
            "waypoints": [
                [41.9014, 12.5015], # Termini
                [41.9030, 12.4990], # Giardini delle Terme di Diocleziano
                [41.9045, 12.4920], # Giardini Piazza Barberini
                [41.9070, 12.4890], # Via Veneto (Alberata storica)
                [41.9095, 12.4870], # Porta Pinciana
                [41.9125, 12.4880]  # Villa Borghese Interno
            ]
        }
    },
    "tor_vergata_campus": {
        "title": "Campus Universitario: Ingegneria ➔ Rettorato",
        "description": "Percorso locale presso l'Università degli Studi di Roma Tor Vergata, sede dell'hackathon locale.",
        "center": [41.8540, 12.6220],
        "zoom": 15,
        "direct_route": {
            "name": "Percorso Stradale Esposto (Via del Politecnico)",
            "color": "#E43700",
            "distance_km": 1.2,
            "walk_time_min": 15,
            "shade_percent": 8,
            "avg_temp_c": 38.2,
            "heat_stress": "Molto Alto (Piazzali Asfaltati)",
            "surface_type": "Marciapiedi aperti privi di schermature",
            "waypoints": [
                [41.8552, 12.6245], # Edificio Didattica Ingegneria
                [41.8535, 12.6210], # Viale Cambridge
                [41.8520, 12.6180]  # Rettorato
            ]
        },
        "cool_route": {
            "name": "Percorso Verde & Porticati del Campus",
            "color": "#00F0FF",
            "distance_km": 1.4,
            "walk_time_min": 18,
            "shade_percent": 65,
            "avg_temp_c": 31.4,
            "heat_stress": "Moderato",
            "surface_type": "Sentiero alberato perimetrale e pensiline ombreggianti",
            "waypoints": [
                [41.8552, 12.6245], # Ingegneria
                [41.8560, 12.6225], # Orto Botanico / Area Verde
                [41.8545, 12.6195], # Viale alberato interno
                [41.8520, 12.6180]  # Rettorato
            ]
        }
    }
}

def get_scenarios():
    return SCENARIOS
