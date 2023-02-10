import csv
from weather_connector import get_weather, select_from_weather, drop_table

def start():
    drop_table()

    def get_weather_app(city_name):
        if city_name == "":
            city_name = 'Wroclaw'
        s = get_weather(city_name)
        if s == "error":
            return "No matching location found."
        return select_from_weather(city_name)

    def csv_weather(city_name):
        if city_name == "":
            city_name = 'Wroclaw'
        with open(f'{(city_name).replace(" ","_")}.csv', 'w', encoding='UTF8') as f:
            city_name_to_save =  select_from_weather(city_name)
            writer = csv.writer(f, delimiter=',')
            writer.writerow([city_name_to_save])
            return "Saved!!!"

    get_city_name = input("""
        Welcome in weather app:
        \n1. By default app check weather in city Wroclaw just press Enter
        \n2. If You want change city write e.g. 'Warszawa' you are looking for
        """)

    print(get_weather_app(get_city_name))

    save_to_csv = input(f"Do you want save to CSV?\nJust write 'save' or press Enter to close ")

    if save_to_csv.lower() == "save":
        csv_weather(get_city_name)

if __name__ == "__main__":
    start()