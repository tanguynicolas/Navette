import requests

base_uri = "https://api.tintamarre.info/api/v1/"

"""
    CITIES creation
"""

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer i2j5eEYQpbUAN8K72fMUGnXAD'
}

cities = [
  {
      "city": { "name": "Amiens" },
      "zone": [ { "name": "Gare", "description": "Gare férovière et routière", "picture": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Amiens_Gare_d%27Amiens_1.jpg/1200px-Amiens_Gare_d%27Amiens_1.jpg" }, { "name": "Quai Bélu", "description": "Centre-ville", "picture": "https://magazine.appartcity.com/wp-content/uploads/2018/06/Amiens-StLeu-RonanLeBideau5.jpg" }, { "name": "UPJV UFR des Sciences", "description": "Université de Picardie Jules Verne, Unité de Formation et de Recherche des Sciences", "picture": "https://webtv.u-picardie.fr/files/thumbs//1610610560d907d-768x432-6.jpg" }, { "name": "Aire de Covoiturage 1", "description": "Aire de covoiturage Amiens Nord A16", "picture": "https://www.autoroutes.sanef.com/sites/default/files/styles/actu_a_la_une/public/2022-10/Parkings%20de%20covoiturage_090.jpg" } ]
  },
  {
      "city": { "name": "Saveuse" },
      "zone": [ { "name": "Place du village" } ]
  },
  {
      "city": { "name": "Poulainville" },
      "zone": [ { "name": "Place du village" } ]
  },
  {
      "city": { "name": "Allonville" },
      "zone": [ { "name": "Place du village" } ]
  },
  {
      "city": { "name": "Glisy" },
      "zone": [ { "name": "Place du village" } ]
  },
  {
      "city": { "name": "Dury" },
      "zone": [ { "name": "Place du village" } ]
  },
  {
      "city": { "name": "Cardonnette" },
      "zone": [ { "name": "Place du village" } ]
  },
  {
      "city": { "name": "Rainneville" },
      "zone": [ { "name": "Place du village" } ]
  },
  {
      "city": { "name": "Daours" },
      "zone": [ { "name": "Place du village" } ]
  },
  {
      "city": { "name": "Boves" },
      "zone": [ { "name": "Place du village" } ]
  },
  {
      "city": { "name": "Sains-en-Amiénois" },
      "zone": [ { "name": "Place du village" } ]
  },
  {
      "city": { "name": "Hébécourt" },
      "zone": [ { "name": "Place du village" } ]
  },
  {
      "city": { "name": "Guignemicourt" },
      "zone": [ { "name": "Place du village" } ]
  },
  {
      "city": { "name": "Ferrières" },
      "zone": [ { "name": "Place du village" } ]
  },
  {
      "city": { "name": "Lamotte-Brebière" },
      "zone": [ { "name": "Place du village" } ]
  }
]

count = 0
for city in cities:
    count += 1

    try:
        r = requests.post(
            f"{base_uri}city/",
            headers=headers,
            json=city["city"]
        )
        print(f"{r.status_code} City {city['city']['name']} created")
    except requests.exceptions.RequestException as e:
        print(f"{r.status_code} Failed to create city {city['city']['name']}")
        raise SystemExit(e)

    for zone in city["zone"]:
        
        try:
            print(f"\t >>>> {zone}")
            r = requests.post(
                f"{base_uri}city/{count}/zone",
                headers=headers,
                json=zone
            )
            print(f"\t{r.status_code} Zone {zone['name']} created")
            print(f"\t\t{r.json()}")
        except requests.exceptions.RequestException as e:
            print(f"\t{r.status_code} Failed to create zone {zone['name']}")
            raise SystemExit(e)
