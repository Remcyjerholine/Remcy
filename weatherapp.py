import sys
import requests
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt
class WeatherApp(QWidget):        #creating a class with the parent class QWidgets
    def __init__(self):
        super().__init__()
        self.city_label=QLabel("enter city name:",self)         #creating a print statement to enter the city name
        self.city_input=QLineEdit(self)                                #making the user to enter the city name with a input statement
        self.get_weather_button=QPushButton("get weather",self)   #an push button ,so that when we click it the process will start to show the weather of that particular city
        self.temperature_label=QLabel(self)            #to show the current temperature
        self.emoji_label=QLabel(self)                  #to include an emoji
        self.description_label=QLabel(self)        #to give an discription of the weather in words
        self.initUI()                                             #calling the initui function

    def initUI(self):             #initializing a user interface
        self.setWindowTitle("weather  app")    #creating a title for the window
        vbox=QVBoxLayout()                #calling the object
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button,0,Qt.AlignCenter)          #adding the alignment for the get weather here because its a button which cant be accessed there
        vbox.addWidget(self.temperature_label)                #to arrange in a colounb
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)               #center alligning every widget
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")                   #calling setobjectname and passing an id (citylabel)
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
 #setting a style sheet
        #taking the parent class (Q...) and using # to get the id passes to it to make the changes in style,font..

        self.setStyleSheet("""
        QLabel,QPushButton{      
        font-family:calibri;}
        QLabel#city_label{
        font-size:40px;
        font-style:italic;
        }
        QLineEdit#city_input{
        font-size:40px;
        }
        QPushButton#get_weather_button{
        font-size:30px;}
        QLabel#temperature_label{
        font-size:75px;}
        QLabel#emoji_label{
        font-size:100px;
        font-family:segoe UI emoji;
        }
        QLabel#description_label{
        font-size:50px;
        }
        """)
        self.get_weather_button.clicked.connect(self.get_weather)  #when the button is clicked it connects to the get weather function to do whats inside the function

    def get_weather(self):                    #connecting to the api
        api_key="c32ca0cd2cba65c4e89ed91a651c6800"
        city=self.city_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        #exception handling
        try:

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()              #converting to json

            if data["cod"]==200:    #200 means the output can be retrived from  the api,no  error occcured
                self.display_weather(data)   #if no error occured the data will be displayed in the app from the data of the api
        except requests.exceptions.HTTPError as http_error  :
            match response.status_code:
                case 400:
                    self.display_error("bad request\nplease check your city name") #putting the self.display_error so that the output will be displayed in the app rather than in the output terminal
                case 401:
                    self.display_error("unauthorized\nplease check your city name")
                case 403:
                    self.display_error("forbidden\nplease check your city name")
                case 404:
                    self.display_error("not found\nplease check your city name")
                case 500:
                    self.display_error("internal server error\nplease check your city name")
                case 502:
                    self.display_error("bad gateway\nplease check your city name")
                case 503:
                    self.display_error("service unavailable\nplease check your city name")
                case 504:
                    self.display_error("gateway timeout\nplease check your city name")
                case _:
                    print(f"HTTP error\n{http_error}")
        except requests.exceptions.connectionError:
            self.display_error("connection error\nplease check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("timeout error\nthe request took too long")
        except requests.exceptions.TooManyRedirects:
            self.display_error("too many redirects\ncheck the url")
        except requests.exceptions.RequestException:
            self.display_error(f"unexpected error\n{req_error}")


    def display_error(self,message):        #
        self.temperature_label.setStyleSheet("font-size:30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self,data):  # to display the weather
        self.temperature_label.setStyleSheet("font-size:75px;")
        temperature_k=data["main"]["temp"]
        temperature_c=temperature_k - 273.15    #for conversion
        temperature_f=(temperature_k*9/5)-459.67
        weather_id=data["weather"][0]["id"]
        weather_description=data["weather"][0]["description"]


        self.temperature_label.setText(f"{temperature_f:.0f}℉")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)
    @staticmethod
    def get_weather_emoji(weather_id):
        if 200<=weather_id<=232:
            return"⛈️"
        elif 300<=weather_id<=321:
            return "🌦️"
        elif 500<=weather_id<=531:
            return "🌧️"
        elif 600<=weather_id<=622:
            return "❄️"
        elif 701<=weather_id<=741:
            return "🌁"
        elif weather_id==762:
            return "️🔥️"
        elif weather_id==771:
            return "️️💨"
        elif weather_id==781:
            return "🌪️"
        elif weather_id==800:
            return "☀️"
        elif 801<=weather_id<=804:
            return "☁️"
        else:
            return ""


if __name__=="__main__":
    app=QApplication(sys.argv)
    weather_app=WeatherApp()                     #creating a empty window
    weather_app.show()             #commanding to show the window
    sys.exit(app.exec_())                #commanding to make the window not to close because the natural behaviour of a window is to close




