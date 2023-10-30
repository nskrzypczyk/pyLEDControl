import ast
import importlib
import os
import pkgutil

effect_dict = {}

def extract_class_names(module_path):
    class_names = []

    def visit_node(node):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "AbstractEffect":
                    if node.name not in class_names:
                        class_names.append(node.name)
                    break
        for child_node in ast.iter_child_nodes(node):
            visit_node(child_node)

    with open(module_path, 'r') as source_file:
        tree = ast.parse(source_file.read())
        for node in ast.walk(tree):
            visit_node(node)

    return class_names


def scan_module_directory(module_directory):
    module_classes = {}
    for root, _, files in os.walk(module_directory):
        for file in files:
            if file.endswith(".py"):
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(module_path.replace(
                    module_directory, "").lstrip(os.path.sep).replace(os.path.sep, "."))[0]
                classes = extract_class_names(module_path)
                module_classes[module_name] = classes[0] if len(
                    classes) > 0 else None
    return module_classes

def get_effect_list():
    return list(filter(lambda x: x is not None, scan_module_directory(os.getcwd()+"/control/effects").values()))

def get_effects():
    global effect_dict
    if len(effect_dict) == 0:
        AbstractEffect = None
        package_name = 'control.effects'
        abstract_class_module_name = package_name + ".abstract_effect"
        package = importlib.import_module(package_name)
        packages = pkgutil.walk_packages(package.__path__, prefix=package_name + '.')
        for importer, modname, ispkg in packages:
            module = importlib.import_module(modname)
            if modname==abstract_class_module_name:
                AbstractEffect = getattr(module, "AbstractEffect")
            for name, obj in module.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, AbstractEffect) and obj is not AbstractEffect:
                    effect_dict[name] = obj
    return effect_dict
get_effects()
