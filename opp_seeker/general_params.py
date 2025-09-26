import os

## this is stupidiest thing that i ever coded


# BASE_DIR is the absolute path to the project root (where config.py lives)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODE = 'DEBUG'


KEYWORDS_PATH = os.path.join(BASE_DIR, 'data_warehouse', 'keywords', 'search_keywords.json')


#DB_DSN = "dbname=job_student_db user=postgres password=root host=localhost port=5432"
DB_DSN = "dbname=job-student-db user=postgres password=root host=postgres port=5432"

CHROME_API= "http://chrome:4444/wd/hub"

# from https://simplemaps.com/data/ma-cities
MOROCCAN_CITIES = ['Casablanca', 'Fès', 'Marrakech', 'Tangier','Tanger', 'Sale', 'Rabat', 'Meknès', 'Oujda-Angad','Oujda', 'Kenitra', 'Agadir', 'Tétouan', 'Taourirt', 'Temara', 'Safi', 'Khénifra', 'El Jadid', 'Laâyoune', 'Mohammedia', 'Kouribga', 'Béni Mellal', 'Ait Melloul', 'Nador', 'Taza', 'Settat', 'Barrechid', 'Al Khmissat', 'Inezgane', 'Ksar El Kebir', 'My Drarga', 'Larache', 'Guelmim', 'Berkane', 'Ad Dakhla', 'Bouskoura', 'Al Fqih Ben Çalah', 'Oued Zem', 'Sidi Slimane', 'Errachidia', 'Guercif', 'Oulad Teïma', 'Ben Guerir', 'Sefrou', 'Fnidq', 'Sidi Qacem', 'Tiznit', 'Moulay Abdallah', 'Youssoufia', 'Martil', 'Aïn Harrouda', 'Souq Sebt Oulad Nemma', 'Skhirate', 'Ouezzane', 'Sidi Yahya Zaer', 'Al Hoceïma', 'M’diq', 'Midalt', 'Azrou', 'El Kelaa des Srarhna', 'Ain El Aouda', 'Beni Yakhlef', 'Ad Darwa', 'Al Aaroui', 'Qasbat Tadla', 'Boujad', 'Jerada', 'Mrirt', 'El Aïoun', 'Azemmour', 'Temsia', 'Zagora', 'Ait Ourir', 'Aziylal', 'Sidi Yahia El Gharb', 'Biougra', 'Zaïo', 'Aguelmous', 'El Hajeb', 'Zeghanghane', 'Imzouren', 'Tit Mellil', 'Mechraa Bel Ksiri', 'Al ’Attawia', 'Demnat', 'Arfoud', 'Tameslouht', 'Bou Arfa', 'Sidi Smai’il', 'Souk et Tnine Jorf el Mellah', 'Mehdya', 'Aïn Taoujdat', 'Chichaoua', 'Tahla', 'Oulad Yaïch', 'Moulay Bousselham', 'Iheddadene', 'Missour', 'Zawyat ech Cheïkh', 'Bouknadel', 'Oulad Tayeb', 'Oulad Barhil', 'Bir Jdid', 'Tifariti']

