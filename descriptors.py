import json
import datetime


class ReadOnlyDescriptor:
    def __init__(self, initial_value=None):
        self._value = initial_value

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        raise AttributeError("Can't set attribute")

    def __delete__(self, instance):
        raise AttributeError("Can't delete attribute")


class ReadOnlyClass:
    field1 = ReadOnlyDescriptor(100)
    field2 = ReadOnlyDescriptor("Hello, world!")


obj = ReadOnlyClass()


# print(obj.field1)
# obj.field1 = 10
# print(obj.field1)
# print(obj.field2)


class IntegerDescriptor:
    def __init__(self, initial_value=None):
        self.value = initial_value

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        self.value = value


class IntegerOnlyClass:
    field1 = IntegerDescriptor(10)
    field2 = IntegerDescriptor()


obj = IntegerOnlyClass()

# obj.field1 = 100
# print(obj.field1)
# obj.field1 = "string"


class TimeStampedAttribute:
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename
        self.value_attr = f"_{name}_value"

    def __get__(self, instance, owner):
        return getattr(instance, self.value_attr)

    def __set__(self, instance, value):
        setattr(instance, self.value_attr, value)
        data = {
            'time': str(datetime.datetime.now()),
            'value': value
        }
        with open(self.filename, 'a') as f:
            f.write(json.dumps(data) + '\n')

    def __set_name__(self, owner, name):
        self.name = name
        self.value_attr = f"_{name}_value"


class TimeSaver:
    attribute = TimeStampedAttribute('attribute', 'data.json')


timer = TimeSaver()
# timer.attribute = 0
