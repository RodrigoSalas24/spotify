import pandas as pd
import re
from datetime import datetime
from collections import Counter


# Lista de enlaces a Google Sheets
google_sheets_links = [
    "https://docs.google.com/spreadsheets/d/1AzKngvmxchamVLvRV1FUiwq1keyApOKg_j4682lPFYY/edit?gid=0#gid=0",
    "https://docs.google.com/spreadsheets/d/1GECFsbWNN4LomGp8xOnNwnFT_UqnbWI0BLgKsKrURHs/edit?gid=0#gid=0",
    "https://docs.google.com/spreadsheets/d/1uSLd3TO4CjEafeMSeU0jt7NkpjbCSNRa68p1mvYM700/edit?gid=0#gid=0"
    # Agrega más enlaces aquí
]


def convert_google_sheet_url(url):
    pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'
    replacement = lambda m: (f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' +
                             (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv')
    return re.sub(pattern, replacement, url)


# Combinar todos los CSVs exportados desde los enlaces
all_dfs = []
for link in google_sheets_links:
    try:
        pandas_url = convert_google_sheet_url(link)
        df_temp = pd.read_csv(pandas_url)  # Cargar cada hoja como DataFrame
        all_dfs.append(df_temp)  # Agregar a la lista de DataFrames
    except Exception as e:
        print(f"Error al leer el enlace {link}: {e}")

# Concatenar todos los DataFrames
df = pd.concat(all_dfs, ignore_index=True)

# Eliminar duplicados (si es necesario)
df = df.drop_duplicates()

# Verifica que el DataFrame combinado no esté vacío
if df.empty:
    print("El DataFrame combinado está vacío. Verifica los enlaces o los permisos de los archivos.")
    exit()

# Verifica si las columnas esperadas existen
expected_columns = ['date', 'artist', 'song']
if not all(col in df.columns for col in expected_columns):
    print(f"Las columnas esperadas no están presentes en el DataFrame. Columnas actuales: {df.columns}")
    exit()

counts = Counter(df.artist)

current_datetime = datetime.now()
current_month = current_datetime.strftime("%B")  # Dejar este para resumir mes
current_month = "2024"

print("\n")
if df.date.str.contains(f'{current_month}').any():
    wrapped = (df[df.date.str.contains(f'{current_month}')])
    print(f"Canciones escuchadas en diciembre de 2024: {len(df[df.date.str.contains('December' and '2024')])} "
          f"(Más o menos {3 * len(df[df.date.str.contains('December')]) / 60} horas)")
    print(f"Canciones escuchadas en enero de 2025: {len(df[df.date.str.contains('January' and '2025')])} "
          f"(Más o menos {3 * len(df[df.date.str.contains('January')]) / 60} horas)")
    print("\n")

counts_1 = Counter(wrapped.artist)
counts_2 = Counter(wrapped.song)

most_popular_artist = dict()
most_popular_song = dict()


print(f"Escuché {len(counts_1.items())} artistas diferentes en", current_month, "\n")

print(f"Escuché {len(wrapped)} canciones en", current_month, " (Más o menos", 3*len(wrapped), "minutos o "
      f"{3*len(wrapped) / 60} horas o {round(3*len(wrapped) / 60 / 24, 2)} dias) \n")

print(f"Escuché {len(counts_2.items())} canciones diferentes en", current_month, "\n")

print("_________________________________________________________\n")

for key, value in counts_1.items():
    if value >= 10:  # Looks at how many artists you've listened to more than ten times
        most_popular_artist[key] = value

for key, value in counts_2.items():
    if value >= 2:  # Looks at how many songs you've listened to more than fifteen times
        most_popular_song[key] = value


most_popular_artist = (dict(sorted(most_popular_artist.items(), key=lambda x: x[1], reverse=True)))
most_popular_song = (dict(sorted(most_popular_song.items(), key=lambda x: x[1], reverse=True)))

keys_list_artist = list(most_popular_artist.keys())
values_list_artist = list(most_popular_artist.values())

# print(f"ARTISTS WITH MORE THAN 10 PLAYS IN {current_month}:\n")

print("TOP 10 ARTISTAS", current_month)

# range(len(keys_list_artist)): # Provides your top ten artists, if you want all artists more >= 10, change range to
# commented
top_artists = min(10, len(keys_list_artist))  # Limita el rango al número de artistas disponibles
cont = 0
for i in range(top_artists):
    cont += 1
    print("{:3}".format(str(cont) + "."), values_list_artist[i], keys_list_artist[i])


keys_list_song = list(most_popular_song.keys())
values_list_song = list(most_popular_song.values())

print("_________________________________________________________\n")

# print(f"SONGS WITH MORE THAN 5 PLAYS IN {current_month}:\n")
print("TOP 10 CANCIONES", current_month)

# range(len(keys_list_song)): # Provides top ten songs, if you want all songs >= 15, change range to commented
top_songs = min(10, len(keys_list_song))  # Limita el rango al número de canciones disponibles
cont = 0
for i in range(top_songs):
    cont += 1
    print("{:3}".format(str(cont) + "."), values_list_song[i], keys_list_song[i])


for key, value in counts_1.items():
    if value == 1:  # Counts artists you've only played one time
        most_popular_artist[key] = value

for key, value in counts_2.items():
    if value == 1:  # Counts number of songs only played one time
        most_popular_song[key] = value


most_popular_artist = (dict(sorted(most_popular_artist.items(), key=lambda x: x[1], reverse=True)))
most_popular_song = (dict(sorted(most_popular_song.items(), key=lambda x: x[1], reverse=True)))

keys_list_artist = list(most_popular_artist.keys())
values_list_artist = list(most_popular_artist.values())

keys_list_song = list(most_popular_song.keys())
values_list_song = list(most_popular_song.values())

print("_________________________________________________________\n")
print(f"Escuché {len(keys_list_artist)} artistas una sola vez", current_month)
print("\n")
print(f"Escuché {len(keys_list_song)} canciones una sola vez", current_month)

if not wrapped.empty:
    cont = len(wrapped[wrapped['artist'].str.contains("dillom", case=False, na=False)])
else:
    cont = 0

print("\n")
print(f"Escuché a  {cont} veces e", current_month)
print("\n")
