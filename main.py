from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDRoundFlatIconButton, MDRoundFlatButton, \
    MDFloatingActionButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.taptargetview import MDTapTargetView
from layoutmargin import AddMargin


class MyLabel(MDLabel, AddMargin):
    pass

class MySwitch(Switch, ButtonBehavior):
    def __init__(self, **kwargs):
        super(MySwitch, self).__init__(**kwargs)


class CardArray(MDBoxLayout):
    def __init__(self, **kwargs):
        super(CardArray, self).__init__(**kwargs)
        self.popup_container = MDBoxLayout(orientation='vertical', spacing=2, padding=2)
        container = MDBoxLayout(orientation='vertical', spacing=2, padding=2)
        popup_close_button = MDRoundFlatButton(text='Exit Panel', size_hint_x=.5, on_press=self.close_popup,
                                          pos_hint={"center_x": .5, "center_y": .5},
                                          md_bg_color= (1, 0, 0, 1),
                                          text_color=(1,0,1,1),
                                          font_size='18sp')
        container.add_widget(self.popup_container)
        container.add_widget(popup_close_button)
        container.add_widget(MDLabel(text=''))
        self.popup = Popup(size_hint=(.4, .3), content=container)

    def close_popup(self, *args):
        self.popup.dismiss()

    def open_popup(self, title='', label_text='', app=None, *args):
        self.popup.title = title
        if label_text in ('OFF', 'ON'):
            self.create_switch_control(app=app, text=label_text)
        else:
            self.create_numeric_control(app=app, text=label_text)
        self.popup.open()

    def create_numeric_control(self, app, text=''):
        grid = MDGridLayout(spacing=3, padding=3, cols=3)
        decrease_number_btn = MDFloatingActionButton(
            icon="minus",
            md_bg_color=app.theme_cls.primary_color,
            on_release= self.numeric_decrement
        )
        self.parameter_label = LabelButton(
            text= text,
            font_size = 40,
            halign= 'center',
            theme_text_color= "Custom",
            text_color=(1, .2, 1, 1),
            on_release= self.commit_parameter_value
        )
        increase_number_btn = MDFloatingActionButton(
            icon="plus",
            md_bg_color=app.theme_cls.primary_color,
            on_release=self.numeric_increment
        )
        self.popup_container.clear_widgets()
        grid.add_widget(decrease_number_btn)
        grid.add_widget(self.parameter_label)
        grid.add_widget(increase_number_btn)
        self.popup_container.add_widget(grid)


    def create_switch_control(self, text, app):
        self.switch_state = True if text == 'ON' else False
        grid = MDGridLayout(spacing=3, padding=3, cols=3)
        self.switch = MySwitch(
            width= dp(64),
            active=self.switch_state
        )
        self.switch.bind(on_press=self.switch_callback)

        self.parameter_label = LabelButton(
            text=text,
            font_size=40,
            halign='center',
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1) if not self.switch.active else (0, 1, 0, 1),
            on_release=self.commit_parameter_value
        )
        commit_btn = MDRoundFlatIconButton(
            text="Commit",
            md_bg_color=app.theme_cls.primary_color,
            on_release=self.commit_parameter_value
        )
        self.popup_container.clear_widgets()
        grid.add_widget(self.parameter_label)
        grid.add_widget(self.switch)
        grid.add_widget(commit_btn)
        self.popup_container.add_widget(grid)

    def _numeric_buttons_callback(self, *args):
        widget = self.parameter_label
        value_char = ''
        if widget.text.isdigit():
            value_digit = eval(widget.text)
        else:
            values = widget.text.split(':')
            value_char = values[0] + ':'
            value_digit = eval(values[-1])
        return value_digit, value_char

    def numeric_decrement(self, *args):
        widget = self.parameter_label
        value_digit, value_char = self._numeric_buttons_callback()
        value_digit -= 1
        widget.text = value_char + str(value_digit)

    def numeric_increment(self, *args):
        widget = self.parameter_label
        value_digit, value_char = self._numeric_buttons_callback()
        value_digit += 1
        widget.text = value_char + str(value_digit)

    def commit_parameter_value(self, *args):
        print('value sent to the backend')

    def switch_callback(self, *args):
        print('switch function is called')
        self.switch_state = self.switch.active
        self.parameter_label.text = 'ON' if self.switch_state else 'OFF'
        self.parameter_label.text_color = (1, 0, 0, 1) if not self.switch_state else (0, 1, 0, 1)

class LabelButton(ButtonBehavior, MDLabel):
    def __init__(self, **kwargs):
        super(LabelButton, self).__init__(**kwargs)


class MonitorScreen(ScrollView):
    nav_drawer = ObjectProperty()
    def __init__(self, **kwargs):
        super(MonitorScreen, self).__init__(**kwargs)



class ContentNavigationDrawer(BoxLayout):
    def __init__(self, **kwargs):
        super(ContentNavigationDrawer, self).__init__(**kwargs)
        self.tap_target_view = None


    def tap_target_start(self):
        if self.tap_target_view is None:
            self.tap_target_view = MDTapTargetView(
                widget=self.ids.commitTipsButton,
                widget_position="right_bottom",
                title_text="Tips for You",
                title_text_size="20sp",
                description_text="After selecting a numeric values in\nthe above controls using the\nincrement or decrement " +
                                 "buttons,\nclick on the new number to\ncommit to the ventilator",
                description_text_color=[1, 1, .5, 1]
            )
        if self.tap_target_view.state == "close":
            self.tap_target_view.start()
        else:
            self.tap_target_view.stop()

    def numeric_buttons_callback(self, button_type=None, widget=None):
        """
        This method is called by the increment and decrement buttons in the bottom sheet of the Control Screen
        :param button_type: str value, its either 'decrement' or 'increment'
        :param widget: The widget whose text is to be updated
        :return: None
        """
        value_char = ''
        if widget.text.isdigit():
            value_digit = eval(widget.text)
        else:
            values = widget.text.split(':')
            value_char = values[0] + ':'
            value_digit = eval(values[-1])
        if button_type == 'decrement':
            value_digit -= 1
        else:
            value_digit += 1
        widget.text = value_char + str(value_digit)


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        '''Called when tap on a menu item.'''

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class VentilatorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"


if __name__ == '__main__':
    VentilatorApp().run()