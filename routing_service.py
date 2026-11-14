"""
Routing Service: Simulates pedestrian cool & shaded paths in Rome.
Calculates shade coverage, surface temperature delta, and thermal comfort scores.
"""

SCENARIOS = {
    "colosseo_navona": {
        "title": "Historic Center: Colosseum ➔ Piazza Navona",
        "description": "Crossing Rome's historic center. Compares the busy, unshaded thoroughfares with historic shaded alleys and parks of Rione Monti and Regola.",
        "center": [41.8945, 12.4820],
        "zoom": 15,
        "direct_route": {
            "name": "Direct Sun Route (Via dei Fori / C.so Vittorio)",
            "color": "#E43700", # Rocket Red
            "distance_km": 2.2,
            "walk_time_min": 28,
            "shade_percent": 14,
            "avg_temp_c": 39.5,
            "heat_stress": "Very High (UHI Red Zone)",
            "surface_type": "Continuous asphalt and paved stone with zero tree canopy",
            "waypoints": [
                [41.8902, 12.4922], # Colosseum
                [41.8925, 12.4880], # Imperial Forums
                [41.8955, 12.4823], # Piazza Venezia
                [41.8962, 12.4770], # Largo di Torre Argentina
                [41.8972, 12.4740], # C.so Vittorio Emanuele
                [41.8992, 12.4731]  # Piazza Navona
            ]
        },
        "cool_route": {
            "name": "Cool & Shaded Route (Rione Monti / Historic Alleys)",
            "color": "#00F0FF", # Neon Cyan / Cool Blue
            "distance_km": 2.5,
            "walk_time_min": 32,
            "shade_percent": 74,
            "avg_temp_c": 30.6,
            "heat_stress": "Low / Moderate (Optimal Thermal Comfort)",
            "surface_type": "High H/W aspect ratio street canyons (building shade) + urban canopy",
            "waypoints": [
                [41.8902, 12.4922], # Colosseum
                [41.8920, 12.4935], # Colle Oppio Park (Canopy)
                [41.8942, 12.4900], # Salita dei Borgia (Deep building shade)
                [41.8950, 12.4870], # Via Baccina (Narrow Monti alleys)
                [41.8940, 12.4810], # Shaded alleys toward Jewish Ghetto
                [41.8930, 12.4760], # Portico d'Ottavia
                [41.8955, 12.4725], # Campo de' Fiori shaded lanes
                [41.8980, 12.4728], # Via del Governo Vecchio
                [41.8992, 12.4731]  # Piazza Navona
            ]
        }
    },
    "termini_borghese": {
        "title": "Green Corridor: Termini Station ➔ Villa Borghese",
        "description": "Connecting Rome's primary transit hub to the expansive canopy of Villa Borghese, circumventing severe urban heat islands.",
        "center": [41.9070, 12.4950],
        "zoom": 15,
        "direct_route": {
            "name": "Direct Sun Route (Via Cernaia / XX Settembre)",
            "color": "#E43700",
            "distance_km": 2.3,
            "walk_time_min": 30,
            "shade_percent": 18,
            "avg_temp_c": 40.8,
            "heat_stress": "Extreme (Exposed Street Canyon)",
            "surface_type": "Heavy traffic asphalt, intense travertine building reverberation",
            "waypoints": [
                [41.9014, 12.5015], # Termini
                [41.9038, 12.4980], # Piazza della Repubblica
                [41.9065, 12.4935], # Via XX Settembre
                [41.9080, 12.4910], # Corso d'Italia
                [41.9125, 12.4880]  # Villa Borghese Pinciana Gate
            ]
        },
        "cool_route": {
            "name": "Cool Route (Baths Gardens ➔ Tree-lined Via Veneto ➔ Park)",
            "color": "#00F0FF",
            "distance_km": 2.6,
            "walk_time_min": 34,
            "shade_percent": 78,
            "avg_temp_c": 29.9,
            "heat_stress": "Low (Microclimatic Oasis)",
            "surface_type": "Mature umbrella pines and continuous garden canopy",
            "waypoints": [
                [41.9014, 12.5015], # Termini
                [41.9030, 12.4990], # Diocletian Baths Gardens
                [41.9045, 12.4920], # Piazza Barberini Gardens
                [41.9070, 12.4890], # Via Veneto tree canopy
                [41.9095, 12.4870], # Porta Pinciana
                [41.9125, 12.4880]  # Villa Borghese Interior
            ]
        }
    },
    "tor_vergata_campus": {
        "title": "University Campus: Engineering Faculty ➔ Rectorate",
        "description": "Local campus pedestrian path at University of Rome Tor Vergata, host venue of the Rome Space Apps hackathon.",
        "center": [41.8540, 12.6220],
        "zoom": 15,
        "direct_route": {
            "name": "Direct Road Route (Via del Politecnico)",
            "color": "#E43700",
            "distance_km": 1.2,
            "walk_time_min": 15,
            "shade_percent": 8,
            "avg_temp_c": 38.2,
            "heat_stress": "Very High (Open Pavement)",
            "surface_type": "Unshaded concrete sidewalks with zero canopy cover",
            "waypoints": [
                [41.8552, 12.6245], # Engineering Teaching Building
                [41.8535, 12.6210], # Viale Cambridge
                [41.8520, 12.6180]  # Rectorate Building
            ]
        },
        "cool_route": {
            "name": "Green Canopy & Campus Arcades Route",
            "color": "#00F0FF",
            "distance_km": 1.4,
            "walk_time_min": 18,
            "shade_percent": 65,
            "avg_temp_c": 31.4,
            "heat_stress": "Moderate (Comfort Corridor)",
            "surface_type": "Botanical perimeter path, mature tree canopy, and shaded arcades",
            "waypoints": [
                [41.8552, 12.6245], # Engineering
                [41.8560, 12.6225], # Botanical Garden Green Corridor
                [41.8545, 12.6195], # Tree-lined internal path
                [41.8520, 12.6180]  # Rectorate Building
            ]
        }
    }
}

def get_scenarios():
    return SCENARIOS
