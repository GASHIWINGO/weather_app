from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import requests
import time
from datetime import datetime, timedelta

class app(Tk):
    def __init__(self):
        Tk.__init__(self)

        #удаление placeholder-текста и вызов bind-метода для кнопки поиска
        #для вызова используется лямбда-функция, т.к. она вызывает get_weather() с передачей ему аргумента search_string
        #без использования лямбда-функции мы не смогли бы передать аргументы в get_weather() и получили бы ошибку при ее вызове
        def delete_placeholder(entry):
         if entry.cget('state') == 'disabled':
            entry.configure(state='normal')
            entry.delete(0, 'end')
            entry.unbind('<Button-1>')
            search_button.bind('<Button-1>', get_weater)
        
        def close():
            weather_app.quit()

        #при нажатии на кнопку "да" после первого ввода
        #элементы нижнего фрейма становятся неактивны, элементы верхнего - наоборот
        def enable():
            yes_button.config(state=DISABLED, cursor="arrow")
            no_button.config(state=DISABLED, cursor="arrow")
            text.config(state=DISABLED)
            search_string.config(state=NORMAL)
            search_string.delete(0, END)
            search_button.config(state=NORMAL)

        #поиск и вывод информации
        def get_weater(event=None):
        #если api-запрос не отправлен, то выводится сообщение об ошибке
            try:
                api_wa = "28e1d8b4a11945de91e53815231803"
                city_get = search_string.get()
                city = city_get.strip()
                url_wa = f"http://api.weatherapi.com/v1/forecast.json?key={api_wa}&q={city}&days=2&aqi=yes&alerts=yes&lang=ru"
                response_wa = requests.get(url_wa).json()
                #если не удается получить информацию, то выводится сообщение об ошибке
                try:
                    temp = response_wa['current']['temp_c']
                    cur_temp.config(text=f'{temp}°C')

                    city_name = response_wa['location']['name']
                    cur_title.config(text=f"Погода {city_name}")
                except:
                    messagebox.showerror('Ошибка!', 'Проверьте название города!')
            except:
                messagebox.showerror('Ошибка!', 'Проверьте подключение к интернету!')

            #получение и вывод информации о погоде в настоящее время
            feels = response_wa['current']['feelslike_c']
            cur_feels.config(text=f'По ощущению {feels}°C')
            humidity = response_wa['current']['humidity']
            cur_hum.config(text=f"Влажность {humidity}%")
            visibility = response_wa["current"]["vis_km"]
            cur_vis.config(text=f"Видимость {visibility:.0f} км")
            pressure = response_wa['current']['pressure_mb']
            cur_pres.config(text=f"Давление {pressure} мм.рт.ст.")
            wind = response_wa['current']['wind_kph']
            cur_windsp.config(text=f"Скорость ветра {wind:.0f} км/ч")
            windgust = response_wa['current']['gust_kph']
            cur_windgust.config(text=f"Порыв ветра {windgust} км/ч")
            aq = response_wa['current']["air_quality"]["pm2_5"]
            cur_aq.config(text=f"Качество воздуха {aq:.1f} мкг/м³")
            snow = response_wa["forecast"]["forecastday"][0]["day"]["totalsnow_cm"]
            cur_snow.config(text=f"Объем выпавшего снега {snow} см")

            #получение и вывод прогноза погоды через 3 часа
            #прибавляем к настоящему времени 3 часа и сравниваем в цикле с временем из api-ответа
            #если разница меньше получаса, то выводим инфомарцию
            cur_time = int(time.time())
            target_time = cur_time + 10800
            forecast_3h = response_wa['forecast']['forecastday'][0]['hour']
            found = False

            windsp_3h.config(text='')

            #если не входим в цикл, то выводим сообщение об отсутствии информации
            for forecast in forecast_3h:
                hour_time = int(forecast['time_epoch'])
                if abs(hour_time - target_time) <= 1800:
                    found = True
                    if found:
                        title_3h.config(text="Погода через 3 часа")
                        temp3h = forecast["temp_c"]
                        temp_3h.config(text=f"{temp3h}°C")
                        feels3h = forecast["feelslike_c"]
                        feels_3h.config(text=f"По ощущению {feels3h}°C")
                        descr3h = forecast["condition"]["text"]
                        descr_3h.config(text=f"{descr3h}")
                        windspeed = forecast["wind_kph"]
                        windsp_3h.config(text=f"Скорость ветра {windspeed} км/ч", font=("Poppins",20))
                        windgust3h = forecast["gust_kph"]
                        windgust_3h.config(text=f"Порыв ветра {windgust3h} км/ч")
                        pressure3h = forecast["pressure_mb"]
                        pres_3h.config(text=f"Давление {pressure3h} мм.рт.ст.")
                        visibility = forecast["vis_km"]
                        vis_3h.config(text=f"Видимость {visibility:.0f} км")
                        humidity = forecast["humidity"]
                        hum_3h.config(text=f"Влажность {humidity}%")
                        rainch_3h = forecast["chance_of_rain"]
                        rain_3h.config(text=f"Вероятность дождя {rainch_3h}%")
                        dewpoint = forecast["dewpoint_c"]
                        dewpoint_3h.config(text=f"Точка росы {dewpoint}°C")
                        break               
            if not found:
                title_3h.config(text="")
                temp_3h.config(text="")
                feels_3h.config(text="")
                descr_3h.config(text="")
                windsp_3h.config(text="Нет информации о погоде через 3 часа", font=("Poppins", 30))
                windgust_3h.config(text="")
                pres_3h.config(text="")
                vis_3h.config(text="")
                hum_3h.config(text="")
                rain_3h.config(text="")
                dewpoint_3h.config(text="")

            #получение и вывод прогноза погоды на завтрашний день
            tomorrow = response_wa["forecast"]["forecastday"][1]

            title_tomorrow.config(text="Погода завтра")
            temp3d = tomorrow["day"]["avgtemp_c"]
            temp_tomorrow.config(text=f"{temp3d}°C")
            descr3d = tomorrow["day"]["condition"]["text"]
            descr_tomorrow.config(text=f"{descr3d}")
            windspeed = tomorrow["day"]["maxwind_kph"]
            windsp_tomorrow.config(text=f"Скорость ветра {windspeed} км/ч")
            visibility = tomorrow["day"]["avgvis_km"]
            vis_tomorrow.config(text=f"Видимость {visibility:.0f} км")
            humidity = tomorrow["day"]["avghumidity"]
            hum_tomorrow.config(text=f"Влажность {humidity}%")
            rainch_tom = tomorrow["day"]["daily_chance_of_rain"]
            rain.config(text=f"Вероятность дождя {rainch_tom}%")
            mintemp = tomorrow["day"]["mintemp_c"]
            min_temp.config(text=f"Температура ночью {mintemp}°C")   
            maxtemp = tomorrow["day"]["maxtemp_c"]
            max_temp.config(text=f"Максимальная температура {maxtemp}°C")

            #элементы верхнего фрейма становится неактивнымы, элементы нижнего - наоборот
            yes_button.config(state=NORMAL, cursor="hand2")
            no_button.config(state=NORMAL, cursor="hand2")
            text.config(state=NORMAL)
            search_string.config(state=DISABLED)
            search_button.config(state=DISABLED)

            #элементы нижнего фрейма становятся видимы
            text.grid()
            yes_button.grid()
            no_button.grid()

            w = self.winfo_screenwidth() // 2 - 720
            h = self.winfo_screenheight() // 2 - 400
            self.geometry(f"{1450}x{700}+{w}+{h}")
            self.minsize(1450,700)

        w = self.winfo_screenwidth() // 2 - 500
        h = self.winfo_screenheight() // 2 - 250
        self.geometry(f"{1000}x{500}+{w}+{h}")
        self.minsize(1000,500)
        self.title("Прогноз погоды")
        title_img = PhotoImage(file = 'images/title.jpg')
        self.iconphoto(False, title_img)
        
        #цвета, использующиеся для фонов фреймов и элементов внутри них
        search_cl = '#ADD8E6'
        current_weather_cl = '#D3D3D3'
        weather_3h_cl = 'white'
        weather_tomorrow_cl = current_weather_cl

        #создаем фрейм, в котором находятся строка поиска и кнопка поиска
        search_box = Frame(self,bg = search_cl, width=200, height=1)
        search_box.grid(row=0, column=0, sticky='NSEW', rowspan=1)
        
        search_string = Entry(search_box, width=50, font=("poppins", 15), justify="center", bg=current_weather_cl, fg='black')
        #добавляем в строку поиска placeholder-текст
        search_string.insert(0, 'Город')
        search_string.configure(state=DISABLED)
        search_string.grid(row=0, column=1)
        #удаляем placeholder
        search_string_ph_del = search_string.bind('<Button-1>', lambda x: delete_placeholder(search_string))
        search_string.bind('<Return>', get_weater)

        search_button = Button(search_box, text='Поиск', bg=current_weather_cl,fg='black', cursor="hand2")
        search_button.grid(row=0, column=2)    

        search_box.grid_rowconfigure(0,weight=1)
        search_box.grid_columnconfigure(0,weight=1)
        search_box.grid_columnconfigure(1,weight=1)
        search_box.grid_columnconfigure(2,weight=1)        
        
        #создаем фрейм, в котором будет информация о погоде в настоящее время
        current_weather = Frame(self, bg=current_weather_cl, width=200)
        current_weather.grid(row=1, column=0, sticky='NSEW')

        cur_title = Label(current_weather,bg=current_weather_cl, font=("Poppins", 30))
        cur_title.grid(column=0, row=0)

        cur_temp = Label(current_weather,bg=current_weather_cl, font=("Poppins", 30))
        cur_temp.grid(column=0, row=1)

        cur_descr = Label(current_weather,bg=current_weather_cl, font=("Poppins", 30))
        cur_descr.grid(column=0, row=2)

        cur_feels = Label(current_weather,bg=current_weather_cl, font=("Poppins", 20))
        cur_feels.grid(column=1, row=0)

        cur_pres = Label(current_weather,bg=current_weather_cl, font=("Poppins", 20))
        cur_pres.grid(column=2, row=0)

        cur_windsp = Label(current_weather,bg=current_weather_cl, font=("Poppins", 20))
        cur_windsp.grid(column=1, row=1)

        cur_windgust = Label(current_weather,bg=current_weather_cl, font=("Poppins", 20))
        cur_windgust.grid(column=2, row=1)

        cur_vis = Label(current_weather,bg=current_weather_cl, font=("Poppins", 20))
        cur_vis.grid(column=1, row=2)

        cur_hum = Label(current_weather,bg=current_weather_cl, font=("Poppins", 20))
        cur_hum.grid(column=2, row=2)

        cur_aq = Label(current_weather,bg=current_weather_cl, font=("Poppins", 20))
        cur_aq.grid(column=1, row=3)

        cur_snow = Label(current_weather,bg=current_weather_cl, font=("Poppins", 20))
        cur_snow.grid(column=2, row=3)

        current_weather.columnconfigure(0, weight=1)
        current_weather.columnconfigure(1, weight=1)
        current_weather.columnconfigure(2, weight=1)
        current_weather.rowconfigure(0, weight=0)
        current_weather.rowconfigure(1, weight=0)
        current_weather.rowconfigure(2, weight=0)
        current_weather.rowconfigure(3, weight=0)

        #создаем фрейм, в котором будет прогноз погоды через 3 часа
        weather_3h = Frame(self, bg=weather_3h_cl, width=200)
        weather_3h.grid(row=2, column=0, sticky='NSEW')

        title_3h = Label(weather_3h,bg=weather_3h_cl, font=("Poppins", 30))
        title_3h.grid(column=0, row=0)

        temp_3h = Label(weather_3h,bg=weather_3h_cl, font=("Poppins", 30))
        temp_3h.grid(column=0, row=1)

        descr_3h = Label(weather_3h,bg=weather_3h_cl, font=("Poppins", 30))
        descr_3h.grid(column=0, row=2)

        feels_3h = Label(weather_3h,bg=weather_3h_cl, font=("Poppins", 20))
        feels_3h.grid(column=1, row=0)

        pres_3h = Label(weather_3h,bg=weather_3h_cl, font=("Poppins", 20))
        pres_3h.grid(column=2, row=0)

        #надпись на стартовом экране 
        windsp_3h = Label(weather_3h, text="Введите название города", bg=weather_3h_cl, font=("Poppins", 50))
        windsp_3h.grid(column=1, row=1)

        windgust_3h = Label(weather_3h,bg=weather_3h_cl, font=("Poppins", 20))
        windgust_3h.grid(column=2, row=1)

        vis_3h = Label(weather_3h,bg=weather_3h_cl, font=("Poppins", 20))
        vis_3h .grid(column=1, row=2)

        hum_3h = Label(weather_3h,bg=weather_3h_cl, font=("Poppins", 20))
        hum_3h.grid(column=2, row=2)

        rain_3h = Label(weather_3h,bg=weather_3h_cl, font=("Poppins", 20))
        rain_3h.grid(column=1, row=3)

        dewpoint_3h = Label(weather_3h,bg=weather_3h_cl, font=("Poppins", 20))
        dewpoint_3h.grid(column=2, row=3)

        weather_3h.columnconfigure(0, weight=1)
        weather_3h.columnconfigure(1, weight=1)
        weather_3h.columnconfigure(2, weight=1)
        weather_3h.rowconfigure(0, weight=0)
        weather_3h.rowconfigure(1, weight=0)
        weather_3h.rowconfigure(2, weight=0)
        weather_3h.rowconfigure(3, weight=0)

        #создаем фрейм, в котором будет прогноз погоды на завтрашний день
        weather_tomorrow = Frame(self, bg=weather_tomorrow_cl, width=200)
        weather_tomorrow.grid(row=3, column=0, sticky='NSEW')

        title_tomorrow = Label(weather_tomorrow,bg=weather_tomorrow_cl,font=("Poppins", 30))
        title_tomorrow.grid(row=0, column=0)

        temp_tomorrow = Label(weather_tomorrow,bg=weather_tomorrow_cl, font=("Poppins", 30))
        temp_tomorrow.grid(column=0, row=1)

        descr_tomorrow = Label(weather_tomorrow,bg=weather_tomorrow_cl, font=("Poppins", 30))
        descr_tomorrow.grid(column=0, row=2)

        windsp_tomorrow = Label(weather_tomorrow,bg=weather_tomorrow_cl, font=("Poppins", 20))
        windsp_tomorrow.grid(column=1, row=2)

        vis_tomorrow = Label(weather_tomorrow,bg=weather_tomorrow_cl, font=("Poppins", 20))
        vis_tomorrow .grid(column=2, row=1)

        hum_tomorrow = Label(weather_tomorrow,bg=weather_tomorrow_cl, font=("Poppins", 20))
        hum_tomorrow.grid(column=2, row=0)

        rain = Label(weather_tomorrow,bg=weather_tomorrow_cl, font=("Poppins", 20))
        rain.grid(column=2, row=2)

        min_temp = Label(weather_tomorrow,bg=weather_tomorrow_cl, font=("Poppins", 20))
        min_temp.grid(column=1, row=1)

        max_temp = Label(weather_tomorrow,bg=weather_tomorrow_cl, font=("Poppins", 20))
        max_temp.grid(column=1, row=0)
        
        weather_tomorrow.columnconfigure(0, weight=1)
        weather_tomorrow.columnconfigure(1, weight=1)
        weather_tomorrow.columnconfigure(2, weight=1)
        weather_tomorrow.rowconfigure(0, weight=0)
        weather_tomorrow.rowconfigure(1, weight=0)
        weather_tomorrow.rowconfigure(2, weight=0)
        weather_tomorrow.rowconfigure(3, weight=0)

        #создаем фрейм, в котором будет реализована возможность выбора пользователем, узнать погоду в другом городе или закрыть приложение
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

        #элементы фрейма невидимы на стартовом экране
        text.grid_remove()
        yes_button.grid_remove()
        no_button.grid_remove()

        #для удобного изменения размеров окна
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

if __name__=="__main__":
    weather_app = app()
    weather_app.mainloop()
