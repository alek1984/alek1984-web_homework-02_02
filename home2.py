# Установите Poetry, если он еще не установлен
# pip install poetry

# Инициализация проекта в виртуальном окружении
# poetry init

# Фиксация версии Python (например, 3.11.9)
# poetry env use python3.11.9

# Добавление зависимостей, если необходимо
# poetry add some-package

import pickle
import re
from datetime import datetime
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must be exactly 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))
    
    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone.value != phone_number]
    
    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = Phone(new_number).value
                return
        raise ValueError("Phone number not found.")
    
    def add_birthday(self, date):
        self.birthday = Birthday(date)
    
    def show_birthday(self):
        if self.birthday:
            return f"Birthday of {self.name}: {self.birthday}"
        return f"No birthday set for {self.name}"
    
    def __str__(self):
        phone_list = '; '.join(p.value for p in self.phones)
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phone_list}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

# Функции для сериализации/десериализации

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

# Главная функция

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            name, phone = args
            record = book.find(name)
            if not record:
                record = Record(name)
                book.add_record(record)
            record.add_phone(phone)
            print("Contact added or updated.")

        elif command == "change":
            name, old_phone, new_phone = args
            record = book.find(name)
            if record:
                try:
                    record.edit_phone(old_phone, new_phone)
                    print("Phone number updated.")
                except ValueError as e:
                    print(e)
            else:
                print("Contact not found.")

        elif command == "phone":
            name = args[0]
            record = book.find(name)
            print(record if record else "Contact not found.")

        elif command == "all":
            print(book if book.data else "No contacts found.")

        elif command == "add-birthday":
            name, date = args
            record = book.find(name)
            if record:
                record.add_birthday(date)
                print("Birthday added.")
            else:
                print("Contact not found.")

        elif command == "show-birthday":
            name = args[0]
            record = book.find(name)
            print(record.show_birthday() if record else "Contact not found.")

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
