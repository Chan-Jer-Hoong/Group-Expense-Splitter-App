# KivyMD imports
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import (MDListItem, MDListItemLeadingIcon,
                             MDListItemHeadlineText, MDListItemSupportingText,
                             MDListItemTertiaryText, MDListItemTrailingIcon,
                             )

# Kivy imports
from kivy.lang import Builder

# Custom imports
from expense import Expense
from database import Database
from user import User

# Password hashing
import bcrypt

class LoginScreen(MDScreen):

    def log_in_user(self):
        # Getting email
        email = self.ids.email.text

        # Getting password
        pw = self.ids.password.text

        pwbytes = pw.encode("utf-8")

        if Database.is_email_exist(email):
            string_pass = Database.get_hashed_password(email)
            byte_pass = string_pass.encode("utf-8")

            valid_password = bcrypt.checkpw(pwbytes, byte_pass)
            
            if valid_password:
                self.manager.current = "main_page"
            else:
                self.ids.email.text = ""
                self.ids.password.text = ""

class SignupScreen(MDScreen):
    
    def register_user(self):
        # Getting username
        name = self.ids.username.text

        # Getting email
        email = self.ids.email.text

        # Getting password and hashing it
        pw = self.ids.password.text

        pwbytes = pw.encode("utf-8")

        pwhash = bcrypt.hashpw(pwbytes, bcrypt.gensalt())

        store_password = pwhash.decode("utf-8")

        if not Database.is_email_exist(email):
            Database.insert_user(self, name, email, store_password)
            self.manager.current = "login"
        else:
            self.ids.username.text = ""
            self.ids.email.text = ""
            self.ids.password.text = ""

class GroupScreen(MDScreen):
    
    def go_back_to_main(self):
        self.manager.current = "main_page"

    def create_new_group(self, group_name):
        Database.insert_group_data(self, MainApp().cur_user.uid, group_name)

class MainScreen(MDScreen):

    def log_out(self):
        self.manager.current = "login"

    def go_to_group_page(self):
        self.manager.current = "group"
    
    def add_list_item(self):

        new_list_item = MDListItem(

            MDListItemLeadingIcon(
                icon="account",
            ),
            MDListItemHeadlineText(
                text="Group 1",
            ),
            MDListItemTertiaryText(
                text="Created by:",
            ),
            MDListItemTrailingIcon(
                icon="arrow-right",
            ),
            on_release = self.go_to_group
        )

        self.ids.group_joined_list.add_widget(new_list_item)
    
    def go_to_group(self, *args):
        self.manager.current = "group"

class MakeExpenseScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.member_amount = 0

    def on_enter(self):
        self.group_members_available()

    def radio_button_select(self, instance, value, selected_button):
        if value == True:
            if selected_button == "auto":
                new_expense = Expense()
                new_expense.set_auto_split_amount(new_expense.auto_split(self.member_amount))
            elif selected_button == "manual":
                print("manual")
        else:
            print(selected_button)

    def confirm_expense_amount(self):
        expense_instance = Expense()

        money = self.ids.input_money_expense.text
        cent = self.ids.input_cent_expense.text

        if money == None or money == "" or "-" in money:
            money = "00"
            
        if cent == None or cent == "" or "-" in cent:
            cent = "00"

        self.ids.expense_amount.text = f"{money}.{cent}"
        expense_instance.set_total_expense(float(self.ids.expense_amount.text))

        self.ids.manual_button.disabled = False
        self.ids.auto_button.disabled = False

    def disable_confirm_button(self, instance, value):
        if value == True:
            self.ids.confirm_expense_button.disabled = True
        else:
            self.ids.confirm_expense_button.disabled = False
    
    def group_members_available(self):

        member_1 = MDListItem(

            MDListItemLeadingIcon(
                icon="account",
            ),
            MDListItemHeadlineText(
                text="Halley",
            ),
            MDListItemTrailingIcon(
                icon="plus",
            ),
            on_release = self.count_members
        )

        member_2 = MDListItem(

            MDListItemLeadingIcon(
                icon="account",
            ),
            MDListItemHeadlineText(
                text="John",
            ),
            MDListItemTrailingIcon(
                icon="plus",
            ),
            on_release = self.count_members
        )

        self.ids.group_member_list.add_widget(member_1)
        self.ids.group_member_list.add_widget(member_2)
    
    def count_members(self, *args):
        self.member_amount += 1

    def go_to_group(self):
        self.manager.current = "group"

class MakeGroupScreen(MDScreen):
    pass

class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cur_user = User()
        Database.create_user_table()
        Database.create_group_table()
        Database.create_expense_table()
        Database.create_member_expense_table()
        Database.create_group_member_table()
        Database.create_pending_invite_table()

    def build(self):
        Builder.load_file("kivy_files\LoginPage.kv")
        Builder.load_file("kivy_files\SignupPage.kv")
        Builder.load_file("kivy_files\GroupPage.kv")
        Builder.load_file("kivy_files\MainPage.kv")
        Builder.load_file("kivy_files\CreateGroupPage.kv")
        Builder.load_file("kivy_files\CreateExpensePage.kv")

        return Builder.load_file("kivy_files\PageManager.kv")

if __name__ == "__main__":
    MainApp().run()