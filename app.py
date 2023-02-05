from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import requests

class app(Tk):
    def __init__(self):
        Tk.__init__(self)
        def close():
            weather_app.quit()

        def enable():
            yes_button.config(state=DISABLED)
            no_button.config(state=DISABLED)
            text.config(state=DISABLED)
            search_string.config(state=NORMAL)
            search_button.config(state=NORMAL)

        def get_weater(event=None):
            api = "57921f19e2a4997ba1168afac370eeb5"
            city = search_string.get()
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric&lang=ru"
            response = requests.get(url).json()
            try: 
                temp = response['main']['temp']
                information_temperature.config(text=f'{temp}°C')

                description = response['weather'][0]['description']
                information_description.config(text=description.title())

                information_city.config(text=city.title())
            except:
                messagebox.showerror('Ошибка!', 'Проверьте название города!')

            feels = response['main']['feels_like']
            information_temperature1.config(text=f'{feels}°C')
            information_temperature2.configure(text="По ощущению")

            humidity = response['main']['humidity']
            information_humidity.config(text=f"Влажность {humidity}%")

            visibility = response['visibility']
            information_visibility.config(text=f"Видимость {visibility} м")

            wind = response['wind']['speed']
            information_wind.config(text=f"Скорость ветра {wind}м/с")

            try:
                wind1 = response['wind']["gust"]
                information_wind2.config(text=f"Порыв ветра {wind1}м/с")
            except:
                information_wind2.config(text=f"В данное время нет информации о порыве ветра")

            try:
                sea_press = response['main']['sea_level']
                ground_press = response['main']['grnd_level']
                information_pressure.config(text=f"Давление над уровнем моря/земли {sea_press}/{ground_press} мм.рт.ст.") 
            except:
                information_pressure.config(text=f"В данное время нет информаии о давлении над уровнем моря/земли")
            
            yes_button.config(state=NORMAL)
            no_button.config(state=NORMAL)
            text.config(state=NORMAL)
            search_string.config(state=DISABLED)
            search_button.config(state=DISABLED)
            

        self.geometry(f"{1130}x{500}+{400}+{200}")
        self.title("Погода")
        title_img = PhotoImage(file = 'images/title.jpg')
        self.iconphoto(False, title_img)

        self.grid()
        
        search_box = Label(self, bg='skyblue3', width=200, height=1)
        search_box.grid(row=0, column=0, sticky='NSEW', rowspan=1)
        
        search_string = Entry(search_box, width=50, font=("poppins", 15), justify="center", bg='blue', fg='white')
        search_string.bind('<Return>', get_weater)
        search_string.insert(0, 'Город')
        search_string.configure(state=DISABLED)
        search_string.grid(row=0, column=1)

        search_button = Button(search_box, text='Поиск', bg='yellow', cursor="hand2")
        search_button.grid(row=0, column=2)

        search_box.grid_rowconfigure(0,weight=1)
        search_box.grid_columnconfigure(0,weight=1)
        search_box.grid_columnconfigure(1,weight=1)
        search_box.grid_columnconfigure(2,weight=1)
        
        information_box = Frame(self, bg='blue', width=200)
        information_box.grid(row=1, column=0, sticky='NSEW')

        information_city = Label(information_box, font=("Poppins", 35), bg='blue', fg='white')
        information_city.grid(row=0, column=0, padx=10, pady=10)

        information_temperature = Label(information_box, font=("Poppins", 40), bg='blue', fg='white')
        information_temperature.grid(row=0, column=1,padx=10, pady=15)

        information_temperature1 = Label(information_box, font=("Poppins", 20), bg='blue', fg='white')
        information_temperature1.grid(row=1, column=2)

        information_description = Label(information_box, font=("Poppins", 30), bg='blue', fg='white')
        information_description.grid(row=1, column=1)

        information_temperature2 = Label(information_box, font=("Poppins", 20), bg='blue', fg='white')
        information_temperature2.grid(row=0, column=2)

        information_wind = Label(information_box, font=("Poppins", 15), bg='blue', fg='white')
        information_wind.grid(row=2, column=0, padx=10)
        
        information_wind2 = Label(information_box, font=("Poppins", 15), bg='blue', fg='white')
        information_wind2.grid(row=2, column=1)

        information_humidity = Label(information_box, font=("Poppins", 15), bg='blue', fg='white')
        information_humidity.grid(row=2, column=2)

        information_visibility = Label(information_box, font=("Poppins", 15), bg='blue', fg='white')
        information_visibility.grid(row=4, column=0)

        information_pressure = Label(information_box,font=("Poppins", 15),bg='blue', fg='white')
        information_pressure.grid(row=4, column=1, columnspan=2)
        
        information_box.grid_columnconfigure(0, weight=1)
        information_box.grid_columnconfigure(1, weight=1)
        information_box.grid_columnconfigure(2, weight=1)
        information_box.grid_rowconfigure(0, weight=1)
        information_box.grid_rowconfigure(1, weight=1)
        information_box.grid_rowconfigure(2, weight=1)
        information_box.grid_rowconfigure(3, weight=1)
        information_box.grid_rowconfigure(4, weight=1)

        bottom_box = Label(self, bg='green', width=200)
        bottom_box.grid(row=2, column=0, sticky='NSEW')

        text = Label(bottom_box, text='Узнать погоду в другом городе?', bg='green', font=("Poppins", 15))
        text.grid(row=0,column=4)
        text.configure(state=DISABLED)

        yes_button = Button(bottom_box, text='Да', bg='green', command=enable)
        yes_button.grid(row=0,column=5, padx=5)
        yes_button.configure(state=DISABLED)

        no_button = Button(bottom_box, text='Нет', bg='green', command=close)
        no_button.grid(row=0,column=6, padx=5)
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
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=25)
        self.grid_rowconfigure(2,weight=1)

        def search_string_click(event):
            search_string.config(state=NORMAL)
            search_string.delete("0", END)
            search_button.bind('<Button-1>', get_weater)
            search_string.unbind('<Button-1>', search_string_click)
        search_string.bind('<Button-1>', search_string_click)
                
if __name__=="__main__":
    weather_app = app()
    weather_app.mainloop()