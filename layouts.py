# from kivy.context import register_context
# from kivy.core import window
# from kivy.lang import Builder
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.widget import Widget
# from kivy.graphics import Rectangle, Color
# from kivy.properties import Clock
# from kivy.core.window import Window

# from io_objects.io_polygon import Polygon
# from io_objects.io_circle import Circle
# from io_objects.kart import Kart


# from kivy.graphics.context_instructions import PushMatrix, PopMatrix, Rotate, Translate, Scale, MatrixInstruction

# # from kart_simulator_launcher import theGame






# Builder.load_file("layouts.kv")


# class MainWidget(Widget):
    
#     from user_actions import keyboard_closed, on_keyboard_down, on_touch_up, on_keyboard_up, on_touch_down

#     dict_objects = dict()
#     dict_circles = dict()

#     vertices = list()
#     indices = list()
#     step = int()

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

#         # self.obstacle_list.append(Circle(diametre=80,position=[300,50]))
#         # self.obstacle_list.append(Polygon(300,300,300,400,400,400,500,500,600,500,400,300))

#         # for obstacle in Container:
#         #     if obstacle.__name__ == "Circle" and obstacle.formID() not in self.dict_circles:
#         #         self.dict_circles[obstacle.formID()] = obstacle
#         #         with self.canvas.before:
#         #             Circle(diametre = 2*obstacle.radius(), position=[obstacle.center()[0],obstacle.center()[1]])

#         #     elif obstacle.__name__ == " Object" and obstacle.formID() not in self.dict_objects:
#         #         self.dict_objects[obstacle.formID()] = obstacle
#         #         with self.canvas.before:
#         #             # Polygon() #A compléter !!!!!!!!!!!!!!!!!!!!!!!!!!!!
#         #             pass



#         with self.canvas.after:
#             Color(1,0,0)
#             self.kart1 = Kart(x1 = 150, y1 = 150)


#         # Clock.schedule_interval(theGame.nextFrame,1/60)

            

#         self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
#         self._keyboard.bind(on_key_down=self.on_keyboard_down)
#         self._keyboard.bind(on_key_up=self.on_keyboard_up)


#     def updateObstacle(self, obstacleID = None, obstacle = None, relativeMouvement = None, absolutePosition = None):
#         if obstacleID or obstacleID == 0:
#             obs = self.dict_objects.get(obstacleID)
#         elif obstacle:
#             obs = obstacle

#         if relativeMouvement:
#             new_pos_x = relativeMouvement[0]+obs.center().get_x()
#             new_pos_y = relativeMouvement[1]+obs.center().get_x()
#             new_pos = list(new_pos_x,new_pos_y)
#         elif absolutePosition:
#             new_pos = absolutePosition

#         obs.updatePosition(new_pos)