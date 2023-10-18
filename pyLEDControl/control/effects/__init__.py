import pkgutil
import importlib

effect_dict = {}
effect_list = []

def get_effects():
    global effect_dict, effect_list
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
    effect_list = list(effect_dict.keys())
    return effect_dict
get_effects()
