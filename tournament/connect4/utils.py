import sys
import pathlib
import inspect
import importlib
import importlib.util
from typing import Type


def find_importable_classes(folder_route: str, base_class: Type) -> dict[str, Type]:
    candidates = {}
    folder_path = pathlib.Path(folder_route).resolve()

    for py_file in folder_path.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
            
        try:
            # Load module using spec for files with spaces in path
            spec = importlib.util.spec_from_file_location(
                f"policy_{py_file.parent.name.replace(' ', '_')}", py_file
            )
            if spec is None or spec.loader is None:
                continue
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, base_class) and 
                    obj is not base_class and 
                    obj.__module__ == module.__name__):
                    # Use folder name as agent name (remove "Group " prefix if present)
                    agent_name = py_file.parent.name
                    candidates[agent_name] = obj
        except Exception as e:
            print(f"⚠️ Error cargando {py_file}: {e}")
            continue

    return candidates
