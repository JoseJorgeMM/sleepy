from kivy.config import Config
Config.set('kivy', 'camera', 'opencv')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.textinput import TextInput
import cv2



class FaceDetectionApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.app_name_input = TextInput(
            hint_text=' Face detector',
            font_size=35,
            size_hint=(None, None),
            size=(250, 300),
            pos_hint={'center_x': 0.5, 'y': 0.59},
            background_color=(0, 0, 0, 1),
            foreground_color=(1, 1, 1, 1)
        )
        self.layout.add_widget(self.app_name_input)
        self.start_button = Button(text='Iniciar nuevo monitoreo',
            background_color=(0,1,0,1),
            font_size=20,
            color=(1, 1, 1, 1),
            size_hint=(None, None), 
            size=(250, 50),  
            pos_hint={'center_x': 0.5, 'y': 0.05}  
        )  
        self.layout.add_widget(self.start_button)
        self.start_button.bind(on_press=self.advertirusuario)
        return self.layout
    
    def advertirusuario(self,instance):
          content = BoxLayout(orientation='vertical', spacing=10)
          popup_message = "* No obstruir la vista de la cámara\n* Proporcione la iluminación necesaria\n* No usar gafas oscuras"
          popup_label = Label(text=popup_message, size_hint_y=None, height=100, markup=True)
          self.accept_button = Button(text="Aceptar", size_hint_y=None, height=50)
          content.add_widget(popup_label)
          content.add_widget(self.accept_button)
          self.popup = Popup(title='Tenga en cuenta las siguientes indicaciones', content=content, size_hint=(None, None), size=(400, 200))
          self.popup.open()
          self.accept_button.bind(on_press=self.cerrarabvertencia)
          self.accept_button.bind(on_press=self.empezardeteccion)
          
    def cerrarabvertencia (self, instance):
        self.popup.dismiss()
        self.layout.remove_widget(self.start_button)
        self.layout.remove_widget(self.app_name_input)
    
    def empezardeteccion(self,instance):
        
        self.image_widget = Image()
        self.layout.add_widget(self.image_widget)
        self.stop_button = Button(text='Detener monitoreo',
            background_color=(1, 0, 0, 1),
            font_size=20,
            color=(1, 1, 1, 1),
            size_hint=(None, None),  
            size=(300, 50), 
            pos_hint={'center_x': 0.5, 'y': 0.05}  
        )  
        #Aquí empieza el modelo
        self.layout.add_widget(self.stop_button)
        self.capture = cv2.VideoCapture(0)
        self.stop_button.bind(on_press=self.detener_deteccion)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)  # Actualizar 
    
    def detener_deteccion(self,instance):
        Clock.unschedule(self.update_frame)
        self.capture.release()
        self.layout.remove_widget(self.image_widget)
        self.layout.remove_widget(self.stop_button)
        self.layout.add_widget(self.app_name_input)
        self.layout.add_widget(self.start_button)
        
        
     
     #Función del modelo       
    def update_frame(self, dt):
        ret, frame = self.capture.read()

        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            buf = cv2.flip(frame, 0).tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.image_widget.texture = texture

    def on_stop(self):
        self.capture.release()
        
    
    
    
if __name__ == '__main__':
    FaceDetectionApp().run()