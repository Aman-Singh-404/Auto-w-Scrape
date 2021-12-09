import json
import os
import re
from typing import Any

class Deserialize:
    def __deserialDictionary(self, inputValue: dict) -> dict:
        '''
        Deserialize dict to a JSON formatted dict.
        '''
        # If inputValue is not of 'dict' type, raise TypeError
        if not isinstance(inputValue, dict):
            raise TypeError(f"<class 'dict'> required, given {type(inputValue)}");
        
        # Serialize every value in key-value pair
        for key, value in inputValue.items():
            inputValue[key] = self.load(value);
        
        return inputValue;
    
    def __deserialList(self, inputValue: list) -> list:
        '''
        Deserialize JSON formatted list to a list.
        '''
        # If inputValue is not of 'list' type, raise TypeError
        if not isinstance(inputValue, list):
            raise TypeError(f"<class 'list'> required, given {type(inputValue)}");
        
        # Serialize every value and add to new list
        outputValue: list = [];
        for value in inputValue:
            outputValue.append(self.load(value));
        
        return outputValue;

    def __deserialObject(self, inputValue: dict) -> object:
        '''
        Deserialize object to a JSON formatted dict.
        '''
        # If inputValue is not of 'dict' type, raise TypeError
        if not isinstance(inputValue, dict) and '__class__' not in inputValue:
            raise TypeError(f"<class 'dict'> required, given {type(inputValue)}");
        
        # Creating class instance
        module_path = inputValue.pop("__class__");
        class_ = __import__(module_path.pop(0));
        
        for module_name in module_path:
            class_ = getattr(class_, module_name);
        
        obj = class_();

        # Serialize every variable of object and add to dict
        outputDict: dict = self.__deserialDictionary(inputValue);
        obj.__dict__.update(outputDict);

        return obj;

    def load(self, inputValue: Any) -> Any:
        '''
        Decide how to serialize inputValue, and return the converted value
        '''
        if isPrimitive(inputValue):
            # If inputValue is a primitive value, return back
            return inputValue;
        elif isinstance(inputValue, dict) and inputValue.__contains__("__class__"):
            # If inputValue is a object, return deserialObject
            return self.__deserialObject(inputValue);
        elif isinstance(inputValue, dict):
            # If inputValue is a dict, return deserialDictionary
            return self.__deserialDictionary(inputValue);
        else:
            # If inputValue is a list, return deserialList
            return self.__deserialList(list(inputValue));

class Serialize:
    def __serialDictionary(self, inputValue: dict) -> dict:
        '''
        Serialize dict to a JSON formatted dict.
        '''
        # If inputValue is not of 'dict' type, raise TypeError
        if not isinstance(inputValue, dict):
            raise TypeError(f"<class 'dict'> required, given {type(inputValue)}");
        
        # Serialize every value in key-value pair
        for key, value in inputValue.items():
            inputValue[key] = self.dump(value);
        
        return inputValue;
    
    def __serialList(self, inputValue: list) -> list:
        '''
        Serialize list to a JSON formatted list.
        '''
        # If inputValue is not of 'list' type, raise TypeError
        if not isinstance(inputValue, list):
            raise TypeError(f"<class 'list'> required, given {type(inputValue)}");
        
        # Serialize every value and add to new list
        outputValue: list = []
        for value in inputValue:
            outputValue.append(self.dump(value));
        
        return outputValue;

    def __serialObject(self, inputValue: object) -> dict:
        '''
        Serialize object to a JSON formatted dict.
        '''
        # If inputValue is not an object, raise TypeError
        if not isinstance(inputValue, object):
            raise TypeError(f"<class 'object'> required, given {type(inputValue)}");
        
        # Add Class with Module metadata for object
        module_path: str = re.findall(r"\'(.*)\'", str(type(inputValue)))[0].split(".");
        class_name = f"_{module_path[-1]}";
        outputValue: dict = { "__class__": module_path };

        # Serialize every variable of object and add to dict
        outputValue.update(self.__serialDictionary(inputValue.__dict__));
        # for key, value in inputValue.__dict__.items():
        #     outputValue[key.replace(class_name, "")] = self.dump(value);

        return outputValue;

    def dump(self, inputValue: Any) -> Any:
        '''
        Decide how to serialize inputValue, and return the converted value
        '''
        if isPrimitive(inputValue):
            # If inputValue is a primitive value, return back
            return inputValue;
        elif isinstance(inputValue, dict):
            # If inputValue is a dict, return serialDictionary
            return self.__serialDictionary(inputValue);
        elif hasattr(inputValue, "__iter__") and not isinstance(inputValue, str):
            # If inputValue is a list, return serialList
            return self.__serialList(list(inputValue));
        else:
            # If inputValue is a object, return serialObject
            return self.__serialObject(inputValue);

def isPrimitive(value: Any) -> bool:
    '''
    Check whether given value is int, string, float or boolean type
    '''
    return (isinstance(value, int) or isinstance(value, str) or value == None 
    or isinstance(value, float) or isinstance(value, bool));
    
def serialize(inputValue: Any, indentation: int = None) -> str:
    '''
    Serialize object to a JSON formatted string.
    '''
    # Serialize inout and returns JSON String
    outputValue = Serialize().dump(inputValue);
    return json.dumps(outputValue, sort_keys=True, indent=indentation);

def deserialize(inputValue: str) -> Any:
    '''
    Deserialize JSON formatted string to an object.
    '''
    # If inputValue is not of 'str' type, raise TypeError
    if not isinstance(inputValue, str):
        raise TypeError(f"<class 'str'> required, given {type(inputValue)}");
    
    # Serialize inout and returns JSON String
    outputValue = json.loads(inputValue);
    return Deserialize().load(outputValue);

def readObject(file: str) -> Any:
    if not os.path.isfile(file):
        raise FileNotFoundError(f"No such file: '{file}'");
    
    data = None;
    with open(file, 'r', encoding='utf-8') as f:
        data = f.read();
    return deserialize(data);

def writeObject(file: str, inputObject: object) -> None:
    parent: str = os.path.split(file)[0];
    if parent != '' and not os.path.isdir(parent):
        os.makedirs(parent);
    
    data: str = serialize(inputObject, 4);
    with open(file, 'w', encoding='utf-8') as f:
        data = f.write(data);

def validHTMLTag(htmlTag: str) -> bool:
    return re.match(r"^<(\"[^\"]*\"|'[^']*'|[^'\">])*>$", htmlTag.strip()) != None