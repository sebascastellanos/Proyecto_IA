#!/usr/bin/env python3
"""Debug script to find what's happening with agent discovery"""

import sys
import pathlib
import inspect
import importlib
from typing import Type
from connect4.policy import Policy

def debug_find_importable_classes(folder_route: str, base_class: Type) -> dict[str, Type]:
    candidates = {}
    folder_path = pathlib.Path(folder_route).resolve()
    project_root = folder_path.parents[0]
    
    print(f"Folder path: {folder_path}")
    print(f"Project root: {project_root}")

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    for py_file in folder_path.rglob("*.py"):
        rel_path = py_file.relative_to(project_root).with_suffix("")
        module_name = ".".join(rel_path.parts)
        print(f"Processing file: {py_file}")
        print(f"  Rel path: {rel_path}")
        print(f"  Module name: {module_name}")
        
        try:
            module = importlib.import_module(module_name)
            print(f"  Successfully imported module")
            
            for name, obj in inspect.getmembers(module, inspect.isclass):
                print(f"    Found class: {name}")
                print(f"    Class module: {obj.__module__}")
                print(f"    Is subclass of Policy: {issubclass(obj, base_class)}")
                print(f"    Is not base_class: {obj is not base_class}")
                
                if issubclass(obj, base_class) and obj is not base_class:
                    key = obj.__module__.split(".")[1] if len(obj.__module__.split(".")) > 1 else obj.__name__
                    print(f"    Adding to candidates with key: {key}")
                    candidates[key] = obj
        except Exception as e:
            print(f"  Failed to import: {e}")
            continue

    return candidates

if __name__ == "__main__":
    print("🔍 Debugging agent discovery...")
    agents = debug_find_importable_classes("groups", Policy)
    print(f"\nFound agents: {list(agents.keys())}")