import ast

def extract_fields_and_types(file_path):
    with open(file_path, 'r', encoding='utf-16') as file:
        tree = ast.parse(file.read())

    fields_and_types = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            fields_and_types[class_name] = {}
            for child in node.body:
                if isinstance(child, ast.Assign) and isinstance(child.targets[0], ast.Name) and isinstance(child.value, ast.Call):
                    field_name = child.targets[0].id
                    field_type = None
                    if isinstance(child.value.func, ast.Attribute):
                        field_type = child.value.func.attr
                    elif isinstance(child.value.func, ast.Name):
                        field_type = child.value.func.id
                    fields_and_types[class_name][field_name] = field_type

    return fields_and_types

if __name__ == "__main__":
    models_file_path = "models.py"
    fields_and_types = extract_fields_and_types(models_file_path)
    for class_name, fields in fields_and_types.items():
        print(f"Class: {class_name}")
        for field_name, field_type in fields.items():
            print(f"\tField: {field_name}, Type: {field_type}")
