# Import required libraries
from datetime import datetime
from tkinter import Button, Label, PhotoImage, Tk, END
import tkinter as tk
import requests# might have to use pythom -m pip install requests, thats if pip install requests fail
import calendar
from weather_icons import icons_day, icons_night, icons_mini #These are the icons used next to the weather updates, no need to have your own images

errors = {"API_404": 'API key not valid, or not yet activated. If you recently signed up for an account or created '
                     'this key, please allow up to 30 minutes for key to activate.',
          }

# Colors
l_blue = '#3fc28e'
d_blue = '#3fc28e'


# Obtain API from https://weatherbit.io/ API KEY, first register account then get free trial API
api_key = '4f191f0702a9480991a45a0ff84a187'#Only available for 30 days.1581ef


def read_api_key():
    with open("api_key.txt") as f:
        return f.read()


def format_date_long(date):
    """Format date to weekday, day month_name (Monday, 18 May)."""
    date_object = datetime.strptime(date, '%Y-%m-%d')
    week_day = calendar.day_name[date_object.weekday()]
    month = date_object.month
    month_name = calendar.month_name[month]
    return f'{week_day[:3]}, {date_object.day} {month_name}'


def format_date_short(date):
    """ Format date to day month_name (18 May) """
    date_object = datetime.strptime(date, '%Y-%m-%d')
    month = date_object.month
    month_name = calendar.month_name[month]
    return f'{date_object.day} {month_name[:3]}'


def mtr_per_sec_to_km_per_hour(m_per_s):
    """Convert units - m/s to km/h."""
    return m_per_s * (1 / 1000) / (1 / 3600)


def get_user_location(link="https://ipinfo.io/city"):#This is used for automated weather UPDATE based on location
    """Find user location based on IP address."""
    try:
        response = requests.get(link)
        if response.status_code == 200:
            city = response.text.strip()
            country = requests.get(link[:-4]+'country').text.strip()
            return f'{city}, {country}'
        else:
            return "Unable to fetch any location data."
    except requests.exceptions.RequestException as e:
        return "404: An error occurred: " + str(e)


def world_weather():
    """Main function that creates window, and updates it with information from the API."""
    # This creates the window and sets the basics.
    root = Tk()
    root.title('World Weather App')
    root.geometry('550x820+500+460')
    root.resizable(False, False)
    root.config(bg='black')

    def get_response_code(key, location):
        """Find API response code for error handling."""
        url = f'https://api.weatherbit.io/v2.0/current?city={location}&key={key}'
        response_code = requests.get(url).status_code
        return response_code

    def get_current_weather(key, location):
        try:
            url = f'https://api.weatherbit.io/v2.0/current?city={location}&key={key}'
            current_data = requests.get(url).json()
        except requests.exceptions.JSONDecodeError:
            url = f'https://api.weatherbit.io/v2.0/current?postal_code={location}&key={key}'
            current_data = requests.get(url).json()
        return current_data

    def get_forecast_weather(key, location):
        try:
            f_url = f'https://api.weatherbit.io/v2.0/forecast/daily?city={location}&key={key}&days=4'
            forecast_data = requests.get(f_url).json()
        except requests.exceptions.JSONDecodeError:
            f_url = f'https://api.weatherbit.io/v2.0/forecast/daily?postal_code={location}&key={key}&days=4'
            forecast_data = requests.get(f_url).json()
        return forecast_data

    def update_current_weather_main_window(current_data):
        """Get data from json and update relevant labels."""
        current = current_data['data'][0]
        # Main window data
        city = current['city_name']
        country = current['country_code']
        code = current['weather']['code']
        current_temp = f"{(int(current['temp']))}"
        current_condition = current['weather']['description']
        local_time = format_date_long(current['datetime'][:-3])
        current_day_or_night = current['pod']

        # Updating the labels
        paichiwo.destroy()
        city_info.config(text=f'{city}, {country}', fg='white', font=('Noto Sans', 12), width=22)
        city_info.place(x=64, y=97)

        if current_day_or_night == 'd':
            weather_icon_image.config(file=icons_day[code])
            weather_icon.place(x=97, y=130)
        else:
            weather_icon_image.config(file=icons_night[code])
            weather_icon.place(x=97, y=130)

        temp.config(text=current_temp)

        if len(current_temp) == 1:
            temp_symbol.config(text='°')
            temp_symbol.place(x=205, y=308)
        else:
            temp_symbol.config(text='°')
            temp_symbol.place(x=238, y=308)

        condition.config(text=current_condition)
        date_info.config(text=local_time)

    def update_current_weather_bottom_row(current_data):
        """Get data from json and update relevant labels."""
        current = current_data['data'][0]
        # Bottom row data
        current_feelslike = f"{(int(current['app_temp']))}"
        current_wind_speed = f"{(int(mtr_per_sec_to_km_per_hour(current['wind_spd'])))}"
        current_humidity = current['rh']
        current_cloud_coverage = f"{(int(current['clouds']))}"
        current_pressure = f"{(int(current['slp']))}"

        # Update the labels
        feelslike.config(text=f'{current_feelslike}°')
        wind.config(text=f'{current_wind_speed} km/h')
        humidity.config(text=f'{current_humidity}%')
        cloud_coverage.config(text=f'{current_cloud_coverage}%')
        pressure.config(text=f'{current_pressure} hPa')
        textfield.delete(0, END)

    def create_forecast_data_list(forecast_data):
        """Extract data needed for the forecast window."""
        forecast_data_list = []

        for forecast_days in forecast_data['data'][1:]:
            forecast_date = format_date_short(forecast_days['datetime'])
            forecast_avg_temp = f"{(int(forecast_days['temp']))}"
            forecast_avg_humidity = f"{(int(forecast_days['rh']))}"
            forecast_max_wind = f"{(int(mtr_per_sec_to_km_per_hour(forecast_days['wind_spd'])))}"
            forecast_code = forecast_days['weather']['code']

            forecast_data_list.append([forecast_date,
                                       forecast_avg_temp,
                                       forecast_avg_humidity,
                                       forecast_max_wind,
                                       forecast_code])
        return forecast_data_list

    def update_forecast_window(forecast_data_list):
        day_1 = forecast_data_list[0]
        day_2 = forecast_data_list[1]
        day_3 = forecast_data_list[2]

        """Update relevant forecast labels."""
        day_1_date.config(text=day_1[0])
        day_1_temp.config(text=f'{day_1[1]}°')
        day_1_humidity.config(text=f'{day_1[2]}%')
        day_1_wind.config(text=f'{day_1[3]} km/h')
        day_1_icon.config(file=icons_mini[day_1[4]])

        day_2_date.config(text=day_2[0])
        day_2_temp.config(text=f'{day_2[1]}°')
        day_2_humidity.config(text=f'{day_2[2]}%')
        day_2_wind.config(text=f'{day_2[3]} km/h')
        day_2_icon.config(file=icons_mini[day_2[4]])

        day_3_date.config(text=day_3[0])
        day_3_temp.config(text=f'{day_3[1]}°')
        day_3_humidity.config(text=f'{day_3[2]}%')
        day_3_wind.config(text=f'{day_3[3]} km/h')
        day_3_icon.config(file=icons_mini[day_3[4]])

    def get_weather():
        global api_key  # maybe later we should consider classes?
        """Connect to API, get data and update tkinter labels."""
        # If textfield left empty use user current location based on IP address
        current_data = {}
        if len(textfield.get()) > 0:
            location = textfield.get()
        else:
            location = get_user_location()
        if not api_key.strip():  # just in case...
            api_key = read_api_key()  # better access
        # Weather data flow
        response = get_response_code(api_key, location)
        if response == 200:
            try:
                current_data = get_current_weather(api_key, location)
                forecast_data = get_forecast_weather(api_key, location)
                forecast_list = create_forecast_data_list(forecast_data)
                update_current_weather_main_window(current_data)
                update_current_weather_bottom_row(current_data)
                update_forecast_window(forecast_list)

            except (KeyError, requests.exceptions.JSONDecodeError):
                if current_data['error'] == errors["API_404"]:
                    city_info.config(text="Wrong or Blank API key", font=('Noto Sans', 9), fg='yellow')
                else:
                    city_info.config(text='Enter correct location', font=('Noto Sans', 9), fg='yellow')
            except requests.exceptions.ConnectionError:
                world_weather()
        elif response == 403:
            city_info.config(text='ERROR 403: Forbidden access', font=('Noto Sans', 9), fg='yellow')
        elif response == 429:
            city_info.config(text='ERROR 429: Too many requests', font=('Noto Sans', 9), fg='yellow')

    # Search box
    search_image = PhotoImage(file='img/current_window.png')
    search_label = Label(image=search_image, bg='black')
    search_label.place(x=20, y=20)
    textfield = tk.Entry(root, cursor='hand2', justify='center', width=23, font=('Noto Sans', 11, 'bold'),
                         bg=d_blue, border=0, fg='white')
    textfield.place(x=62, y=67, height=25)
    textfield.focus()
    textfield.bind('<Return>', lambda event=None: search_button.invoke())
    search_icon = PhotoImage(file='img/magnifying_glass.png')
    search_button = Button(image=search_icon, activebackground=d_blue, borderwidth=0,
                           bg=d_blue, command=get_weather)
    search_button.place(x=265, y=65)

    # Create Current Weather labels
    city_info = Label(text='enter city, postcode/ leave empty\n if to use your current location',
                      font=('Noto Sans', 8), justify='center', bg=l_blue, fg='white', width=34)
    city_info.place(x=55, y=97)
    weather_icon_image = PhotoImage(file='img/splash_icon.png')
    weather_icon = Label(root, image=weather_icon_image, bg=l_blue)
    weather_icon.place(x=105, y=157)

    temp = Label(text='', font=('Noto Sans', 85, 'bold'), justify='center', bg=l_blue, fg='white', width=2)
    temp.place(x=104, y=280, height=111)
    temp_symbol = Label(text='', font=('Noto Sans', 20, 'bold'), justify='center', bg=l_blue, fg='white', width=1)
    temp_symbol.place(x=205, y=308, height=15)
    condition = Label(text='', font=('Noto Sans', 11), justify='center', bg=l_blue, fg='white', width=27)
    condition.place(x=53, y=390, height=30)
    date_info = Label(text='', font=('Noto Sans', 8), justify='center', bg=l_blue, fg='white', width=30)
    date_info.place(x=70, y=418, height=15)
    paichiwo = Label(text='Daily updates ', font=('Noto Sans', 8), bg=l_blue, fg='white')
    paichiwo.place(x=143, y=300)

    feelslike = Label(text='', font=('Noto Sans', 8, 'bold'), justify='center', bg=l_blue, fg='white', width=3)
    feelslike.place(x=63, y=487, height=15)
    wind = Label(text='', font=('Noto Sans', 8, 'bold'), justify='center', bg=l_blue, fg='white', width=7)
    wind.place(x=100, y=487, height=15)
    humidity = Label(text='', font=('Noto Sans', 8, 'bold'), justify='center', bg=l_blue, fg='white', width=4)
    humidity.place(x=163, y=487, height=15)
    cloud_coverage = Label(text='', font=('Noto Sans', 8, 'bold'), justify='center', bg=l_blue, fg='white', width=5)
    cloud_coverage.place(x=206, y=487, height=15)
    pressure = Label(text='', font=('Noto Sans', 8, 'bold'), justify='center', bg=l_blue, fg='white', width=7)
    pressure.place(x=249, y=487, height=15)

    # Create Forecast Weather labels
    day_1_date = Label(text='', font=('Noto Sans', 9, 'bold'), justify='center', bg='black', fg='white', width=10)
    day_1_date.place(x=32, y=535, height=20)
    day_1_temp = Label(text='', font=('Noto Sans', 8, 'bold'), justify='center', bg='black', fg='white', width=10)
    day_1_temp.place(x=37, y=555, height=20)
    day_1_humidity = Label(text='', font=('Noto Sans', 8, 'bold'), justify='center', bg='black', fg='white', width=10)
    day_1_humidity.place(x=37, y=575, height=20)
    day_1_wind = Label(text='', font=('Noto Sans', 8, 'bold'), justify='center', bg='black', fg='white', width=10)
    day_1_wind.place(x=37, y=595, height=20)
    day_1_icon = PhotoImage(file='img/dummy_mini.png')
    day_1_icon_label = Label(root, image=day_1_icon, bg='black')
    day_1_icon_label.place(x=53, y=618)

    day_2_date = Label(text='', font=('Noto Sans', 9, 'bold'), justify='center', bg='black', fg='white', width=10)
    day_2_date.place(x=135, y=535, height=20)
    day_2_temp = Label(text='', font=('Noto Sans', 8, 'bold'), justify='center', bg='black', fg='white', width=10)
    day_2_temp.place(x=140, y=555, height=20)
    day_2_humidity = Label(text='', font=('Noto Sans', 8, 'bold'), justify='center', bg='black', fg='white', width=10)
    day_2_humidity.place(x=140, y=575, height=20)
    day_2_wind = Label(text='', font=('Noto Sans', 8, 'bold'), justify='center', bg='black', fg='white', width=10)
    day_2_wind.place(x=140, y=595, height=20)
    day_2_icon = PhotoImage(file='img/dummy_mini.png')
    day_2_icon_label = Label(root, image=day_2_icon, bg='black')
    day_2_icon_label.place(x=156, y=618)

    day_3_date = Label(text='', font=('Noto Sans', 9, 'bold'), justify='center', bg='black', fg='white', width=10)
    day_3_date.place(x=234, y=535, height=20)
    day_3_temp = Label(text='', font=('Noto Sans', 8, 'bold'), justify='center', bg='black', fg='white', width=10)
    day_3_temp.place(x=239, y=555, height=20)
    day_3_humidity = Label(text='', font=('Noto Sans', 8, 'bold'), justify='center', bg='black', fg='white', width=10)
    day_3_humidity.place(x=239, y=575, height=20)
    day_3_wind = Label(text='', font=('Noto Sans', 8, 'bold'), justify='center', bg='black', fg='white', width=10)
    day_3_wind.place(x=239, y=595, height=20)
    day_3_icon = PhotoImage(file='img/dummy_mini.png')
    day_3_icon_label = Label(root, image=day_3_icon, bg='black')
    day_3_icon_label.place(x=255, y=618)

    root.mainloop()


if __name__ == '__main__':
    world_weather()
