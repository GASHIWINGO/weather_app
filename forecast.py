from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import requests
import time
from datetime import datetime, timedelta

class app(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        def close():
            weather_app.quit()

        def enable():
            yes_button.config(state=DISABLED, cursor="arrow")
            no_button.config(state=DISABLED, cursor="arrow")
            text.config(state=DISABLED)
            search_string.config(state=NORMAL)
            search_string.delete(0, END)
            search_button.config(state=NORMAL)

        def get_weater(event=None):
            api_owm = "57921f19e2a4997ba1168afac370eeb5"
            api_wa = "124d091ba0a847098ea93852231202"
            city = search_string.get()
            try:
                url_owm = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_owm}&units=metric&lang=ru"            
                response_owm = requests.get(url_owm).json()

                url_wa = f"http://api.weatherapi.com/v1/forecast.json?key={api_wa}&q={city}&days=3&aqi=yes&alerts=yes&lang=ru"
                response_wa = requests.get(url_wa).json()

                try: 
                    temp = response_owm['main']['temp']
                    cur_temp.config(text=f'{temp}°C')

                    city_name = response_owm['name']
                    cur_title.config(text=f"Погода {city_name}")

                    description = response_owm['weather'][0]['description']
                    cur_descr.config(text=description.title())
                except:
                    messagebox.showerror('Ошибка!', 'Проверьте название города!')
            except:
                messagebox.showerror('Ошибка!', 'Проверьте подключение к интернету!')

            feels = response_owm['main']['feels_like']
            cur_feels.config(text=f'По ощущению {feels}°C')
            humidity = response_owm['main']['humidity']
            cur_hum.config(text=f"Влажность {humidity}%")
            visibility = response_wa["current"]["vis_km"]
            cur_vis.config(text=f"Видимость {visibility:.0f} км")
            pressure = response_owm['main']['pressure']
            cur_pres.config(text=f"Давление {pressure} мм.рт.ст.")
            wind = response_wa['current']['wind_kph']
            cur_windsp.config(text=f"Скорость ветра {wind:.0f} км/ч")
            try:
                gust = response_wa['current']["gust_kph"]
                cur_windgust.config(text=f"Порыв ветра {gust:.0f} км/ч")
            except:
                cur_windgust.config(text=f"В данное время нет информации о порыве ветра")
            aq = response_wa['current']["air_quality"]["pm2_5"]
            cur_aq.config(text=f"Качество воздуха {aq:.1f} мкг/м³")
            snow = response_wa["forecast"]["forecastday"][0]["day"]["totalsnow_cm"]
            cur_snow.config(text=f"Объем выпавшего снега {snow} см")
            snow_3h.config(text=f"Объем выпавшего снега {snow} см")

            cur_time = int(time.time())
            target_time = cur_time + 10800

            forecast_3h = response_wa['forecast']['forecastday'][0]['hour']

            found = False
            for forecast in forecast_3h:
                hour_time = int(forecast['time_epoch'])
                if abs(hour_time - target_time) <= 1800:
                    found = True
                    temp3h = forecast["temp_c"]
                    temp_3h.config(text=f"{temp3h}°C")
                    feels3h = forecast["feelslike_c"]
                    feels_3h.config(text=f"По ощущению {feels3h}°C")
                    descr3h = forecast["condition"]["text"]
                    descr_3h.config(text=f"{descr3h}")
                    windspeed = forecast["wind_kph"]
                    windsp_3h.config(text=f"Скорость ветра {windspeed} км/ч")
                    windgust = forecast["gust_kph"]
                    windgust_3h.config(text=f"Порыв ветра {windgust} км/ч")
                    pressure = forecast["pressure_mb"]
                    pres_3h.config(text=f"Давление {pressure} мм.рт.ст.")
                    visibility = forecast["vis_km"]
                    vis_3h.config(text=f"Видимость {visibility:.0f} км")
                    humidity = forecast["humidity"]
                    hum_3h.config(text=f"Влажность {humidity}%")
                    aq = forecast["air_quality"]["pm2_5"]
                    aq_3h.config(text=f"Качество воздуха {aq:.1f} мкг/м³")
                    break

            if not found:
                title_3h.config(text="Нет информации о погоде через 3 часа в данное время")

            tomorrow = response_wa["forecast"]["forecastday"][1]

            temp3d = tomorrow["day"]["avgtemp_c"]
            temp_3d.config(text=f"{temp3d}°C")
            descr3d = tomorrow["day"]["condition"]["text"]
            descr_3d.config(text=f"{descr3d}")
            windspeed = tomorrow["day"]["maxwind_kph"]
            windsp_3d.config(text=f"Скорость ветра {windspeed} км/ч")
            pressure = forecast["pressure_mb"]
            pres_3h.config(text=f"Давление {pressure} мм.рт.ст.")
            visibility = tomorrow["day"]["avgvis_km"]
            vis_3d.config(text=f"Видимость {visibility:.0f} км")
            humidity = tomorrow["day"]["avghumidity"]
            hum_3d.config(text=f"Влажность {humidity}%")
            aq = tomorrow["day"]["air_quality"]["pm2_5"]
            aq_3d.config(text=f"Качество воздуха {aq:.1f} мкг/м³")
            snow1 = tomorrow["day"]["totalsnow_cm"]
            snow_3d.config(text=f"Объем выпавшего снега {snow1} см")
            rainch = tomorrow["day"]["daily_chance_of_rain"]
            rain.config(text=f"Вероятность дождя {rainch}%")

            yes_button.config(state=NORMAL, cursor="hand2")
            no_button.config(state=NORMAL, cursor="hand2")
            text.config(state=NORMAL)
            search_string.config(state=DISABLED)
            search_button.config(state=DISABLED)

        self.geometry(f"{1450}x{700}+{50}+{50}")
        self.title("Погода")
        title_img = PhotoImage(file = 'images/title.jpg')
        self.iconphoto(False, title_img)

        self.grid()
        
        search_cl = '#ADD8E6'
        current_weather_cl = '#D3D3D3'
        weather_3h_cl = 'white'
        weather_3d_cl = current_weather_cl

        search_box = Frame(self,bg = search_cl, width=200, height=1)
        search_box.grid(row=0, column=0, sticky='NSEW', rowspan=1)
        
        search_string = Entry(search_box, width=50, font=("poppins", 15), justify="center", bg=current_weather_cl, fg='black')
        search_string.bind('<Return>', get_weater)
        search_string.insert(0, 'Город')
        search_string.configure(state=DISABLED)
        search_string.grid(row=0, column=1)

        search_button = Button(search_box, text='Поиск', bg=current_weather_cl,fg='black', cursor="hand2")
        search_button.grid(row=0, column=2)

        search_box.grid_rowconfigure(0,weight=1)
        search_box.grid_columnconfigure(0,weight=1)
        search_box.grid_columnconfigure(1,weight=1)
        search_box.grid_columnconfigure(2,weight=1)
        
        current_weather = Frame(self, bg=current_weather_cl, width=200)
        current_weather.grid(row=1, column=0, sticky='NSEW')

        cur_title = Label(current_weather, text="Погода", bg=current_weather_cl, font=("Poppins", 30))
        cur_title.grid(column=0, row=0)

        cur_temp = Label(current_weather, text="100°C", bg=current_weather_cl, font=("Poppins", 30))
        cur_temp.grid(column=0, row=1)

        cur_descr = Label(current_weather, text="Пасмурно", bg=current_weather_cl, font=("Poppins", 30))
        cur_descr.grid(column=0, row=2)

        cur_feels = Label(current_weather, text="По ощущению: 100°C", bg=current_weather_cl, font=("Poppins", 20))
        cur_feels.grid(column=1, row=0)

        cur_pres = Label(current_weather, text="Давление: 1000 мм.рт.ст.", bg=current_weather_cl, font=("Poppins", 20))
        cur_pres.grid(column=2, row=0)

        cur_windsp = Label(current_weather, text="Скорость ветра: 100 км/ч", bg=current_weather_cl, font=("Poppins", 20))
        cur_windsp.grid(column=1, row=1)

        cur_windgust = Label(current_weather, text="Порыв ветра: 100 км/ч", bg=current_weather_cl, font=("Poppins", 20))
        cur_windgust.grid(column=2, row=1)

        cur_vis = Label(current_weather, text="Видимость: 10000 км", bg=current_weather_cl, font=("Poppins", 20))
        cur_vis.grid(column=1, row=2)

        cur_hum = Label(current_weather, text="Влажность: 100%", bg=current_weather_cl, font=("Poppins", 20))
        cur_hum.grid(column=2, row=2)

        cur_aq = Label(current_weather, text="Качество воздуха: 100 мкг/м³", bg=current_weather_cl, font=("Poppins", 20))
        cur_aq.grid(column=1, row=3)

        cur_snow = Label(current_weather, text="Объем выпавшего снега: 100 см", bg=current_weather_cl, font=("Poppins", 20))
        cur_snow.grid(column=2, row=3)

        current_weather.columnconfigure(0, weight=1)
        current_weather.columnconfigure(1, weight=1)
        current_weather.columnconfigure(2, weight=1)
        current_weather.rowconfigure(0, weight=0)
        current_weather.rowconfigure(1, weight=0)
        current_weather.rowconfigure(2, weight=0)
        current_weather.rowconfigure(3, weight=0)

        weather_3h = Frame(self, bg=weather_3h_cl, width=200)
        weather_3h.grid(row=2, column=0, sticky='NSEW')

        title_3h = Label(weather_3h, text="Погода через 3 часа", bg=weather_3h_cl, font=("Poppins", 30))
        title_3h.grid(column=0, row=0)

        temp_3h = Label(weather_3h, text="100°C", bg=weather_3h_cl, font=("Poppins", 30))
        temp_3h.grid(column=0, row=1)

        descr_3h = Label(weather_3h, text="Пасмурно", bg=weather_3h_cl, font=("Poppins", 30))
        descr_3h.grid(column=0, row=2)

        feels_3h = Label(weather_3h, text="По ощущению: 100°C", bg=weather_3h_cl, font=("Poppins", 20))
        feels_3h.grid(column=1, row=0)

        pres_3h = Label(weather_3h, text="Давление: 1000 мм.рт.ст.", bg=weather_3h_cl, font=("Poppins", 20))
        pres_3h.grid(column=2, row=0)

        windsp_3h = Label(weather_3h, text="Скорость ветра: 100 км/ч", bg=weather_3h_cl, font=("Poppins", 20))
        windsp_3h.grid(column=1, row=1)

        windgust_3h = Label(weather_3h, text="Порыв ветра: 100 км/ч", bg=weather_3h_cl, font=("Poppins", 20))
        windgust_3h.grid(column=2, row=1)

        vis_3h = Label(weather_3h, text="Видимость: 10000 м", bg=weather_3h_cl, font=("Poppins", 20))
        vis_3h .grid(column=1, row=2)

        hum_3h = Label(weather_3h, text="Влажность: 100%", bg=weather_3h_cl, font=("Poppins", 20))
        hum_3h.grid(column=2, row=2)

        aq_3h = Label(weather_3h, text="Качество воздуха: 100 мкг/м³", bg=weather_3h_cl, font=("Poppins", 20))
        aq_3h.grid(column=1, row=3)

        snow_3h = Label(weather_3h, text="Объем выпавшего снега: 100 см", bg=weather_3h_cl, font=("Poppins", 20))
        snow_3h.grid(column=2, row=3)

        weather_3h.columnconfigure(0, weight=1)
        weather_3h.columnconfigure(1, weight=1)
        weather_3h.columnconfigure(2, weight=1)
        weather_3h.rowconfigure(0, weight=0)
        weather_3h.rowconfigure(1, weight=0)
        weather_3h.rowconfigure(2, weight=0)
        weather_3h.rowconfigure(3, weight=0)

        weather_3d = Frame(self, bg=weather_3d_cl, width=200)
        weather_3d.grid(row=3, column=0, sticky='NSEW')

        title_3d = Label(weather_3d,bg=weather_3d_cl, text="Прогноз погоды на завтра", font=("Poppins", 30))
        title_3d.grid(row=0, column=0)

        temp_3d = Label(weather_3d, text="100°C", bg=weather_3d_cl, font=("Poppins", 30))
        temp_3d.grid(column=0, row=1)

        descr_3d = Label(weather_3d, text="Пасмурно", bg=weather_3d_cl, font=("Poppins", 30))
        descr_3d.grid(column=0, row=2)

        windsp_3d = Label(weather_3d, text="Скорость ветра: 100 км/ч", bg=weather_3d_cl, font=("Poppins", 20))
        windsp_3d.grid(column=1, row=0)

        vis_3d = Label(weather_3d, text="Видимость: 10000 м", bg=weather_3d_cl, font=("Poppins", 20))
        vis_3d .grid(column=1, row=1)

        hum_3d = Label(weather_3d, text="Влажность: 100%", bg=weather_3d_cl, font=("Poppins", 20))
        hum_3d.grid(column=2, row=0)

        aq_3d = Label(weather_3d, text="Качество воздуха: 100 мкг/м³", bg=weather_3d_cl, font=("Poppins", 20))
        aq_3d.grid(column=1, row=2)

        snow_3d = Label(weather_3d, text="Объем выпавшего снега: 100 см", bg=weather_3d_cl, font=("Poppins", 20))
        snow_3d.grid(column=2, row=1)

        rain = Label(weather_3d, text="Вероятность дождя 100%", bg=weather_3d_cl, font=("Poppins", 20))
        rain.grid(column=2, row=2)
        
        weather_3d.columnconfigure(0, weight=1)
        weather_3d.columnconfigure(1, weight=1)
        weather_3d.columnconfigure(2, weight=1)
        weather_3d.rowconfigure(0, weight=0)
        weather_3d.rowconfigure(1, weight=0)
        weather_3d.rowconfigure(2, weight=0)
        weather_3d.rowconfigure(3, weight=0)

        bottom_box = Frame(self, bg='#ADD8E6', width=200)
        bottom_box.grid(row=4, column=0, sticky='NSEW')

        text = Label(bottom_box, text='Узнать погоду в другом городе?', bg='#ADD8E6', font=("Poppins", 15))
        text.grid(row=0,column=4)
        text.configure(state=DISABLED)

        yes_button = Button(bottom_box, text='Да', bg='#ADD8E6', command=enable)
        yes_button.grid(row=0,column=5, padx=5)
        yes_button.configure(state=DISABLED)

        no_button = Button(bottom_box, text='Нет', bg='#ADD8E6', command=close)
        no_button.grid(row=0,column=6)
        no_button.configure(state=DISABLED)

        sg = ttk.Sizegrip(bottom_box)
        sg.grid(column=9)

        bottom_box.grid_rowconfigure(0,weight=1)
        bottom_box.grid_columnconfigure(0,weight=1)
        bottom_box.grid_columnconfigure(1,weight=1)
        bottom_box.grid_columnconfigure(2,weight=1)
        bottom_box.grid_columnconfigure(3,weight=1)
        bottom_box.grid_columnconfigure(4,weight=1)
        bottom_box.grid_columnconfigure(5,weight=1)
        bottom_box.grid_columnconfigure(6,weight=1)
        bottom_box.grid_columnconfigure(7,weight=1)
        bottom_box.grid_columnconfigure(8,weight=1)
        bottom_box.grid_columnconfigure(8,weight=1)

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=0)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=1)
        self.grid_rowconfigure(3,weight=1)
        self.grid_rowconfigure(4,weight=0)

        def search_string_click(event):
            search_string.config(state=NORMAL)
            search_string.delete("0", END)
            search_button.bind('<Button-1>', get_weater)
            search_string.unbind('<Button-1>', search_string_click)
        search_string.bind('<Button-1>', search_string_click)
        

if __name__=="__main__":
    weather_app = app()
    weather_app.mainloop()