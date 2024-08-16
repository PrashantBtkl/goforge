import json
import re

def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def get_go_type(value):
    if isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float64"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, list):
        if len(value) > 0:
            return f"[]" + get_go_type(value[0])
        else:
            return "[]interface{}"
    elif isinstance(value, dict):
        return "struct"
    else:
        return "interface{}"

def json_to_go_struct(name, data, indent=""):
    result = f"{indent}type {name} struct {{\n"
    
    for key, value in data.items():
        go_type = get_go_type(value)
        field_name = to_camel_case(key)
        
        if go_type == "struct":
            result += f"{indent}    {field_name} {json_to_go_struct(field_name, value, indent + '   ')}"
        else:
            result += f"{indent}    {field_name} {go_type} `json:\"{key}\"`\n"
    
    result += f"{indent}}}"
    return result

def convert_json_to_go(json_string):
    try:
        data = json.loads(json_string)
        return json_to_go_struct("RootType", data)
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON - {str(e)}"

# Example usage
json_input = '''
{
    "name": "John Doe",
    "age": 30,
    "is_student": false,
    "grades": [85, 90, 78],
    "address": {
        "street": "123 Main St",
        "city": "Anytown",
        "zip_code": "12345"
    },
    "courses": [
        {
            "name": "Math",
            "credit_hours": 3
        },
        {
            "name": "Science",
            "credit_hours": 4
        }
    ]
}
'''

go_struct = convert_json_to_go(json_input)
print(go_struct)
