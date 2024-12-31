import os
import importlib.util
import sys
import shutil

def import_module_from_path(module_name, module_path):
    """Import a module from a specific path"""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Error loading module {module_name} from {module_path}: {e}")
        return None

def copy_web_files(src_dir, dst_dir, submodule_name):
    """Copy web files from source to destination directory with renamed js files"""
    if os.path.exists(src_dir):
        # Create destination directory if it doesn't exist
        os.makedirs(dst_dir, exist_ok=True)
        
        # Process all files from source
        for item in os.listdir(src_dir):
            src_item = os.path.join(src_dir, item)
            
            if os.path.isfile(src_item):
                # For js files, add submodule_ prefix
                if item.endswith('.js'):
                    dst_item = os.path.join(dst_dir, f"submodule_{submodule_name}_{item}")
                else:
                    dst_item = os.path.join(dst_dir, item)
                shutil.copy2(src_item, dst_item)
            
            elif os.path.isdir(src_item):
                if item == 'js':
                    # Handle js directory specially
                    js_dst_dir = os.path.join(dst_dir, item)
                    os.makedirs(js_dst_dir, exist_ok=True)
                    for js_file in os.listdir(src_item):
                        if js_file.endswith('.js'):
                            js_src = os.path.join(src_item, js_file)
                            js_dst = os.path.join(js_dst_dir, f"submodule_{submodule_name}_{js_file}")
                            shutil.copy2(js_src, js_dst)
                else:
                    # For other directories, create them and process their contents
                    dst_subdir = os.path.join(dst_dir, item)
                    os.makedirs(dst_subdir, exist_ok=True)
                    copy_web_files(src_item, dst_subdir, submodule_name)

def add_fish_emoji(category):
    """Add fish emoji to category if it doesn't have one"""
    if not category.startswith("🐟"):
        return f"🐟{category}"
    return category

def load_submodules(base_path):
    """Load all submodules and return their node mappings"""
    submodule_nodes = {}
    submodule_display_names = {}
    
    # Setup web directory
    main_web_dir = os.path.join(base_path, "web")
    os.makedirs(main_web_dir, exist_ok=True)
    
    # Process submodules
    submodules_dir = os.path.join(base_path, "external_nodes")
    if os.path.exists(submodules_dir):
        for submodule in os.listdir(submodules_dir):
            submodule_path = os.path.join(submodules_dir, submodule)
            init_path = os.path.join(submodule_path, "__init__.py")
            if os.path.isfile(init_path):
                # Import module using a simple name to avoid conflicts
                module = import_module_from_path(f"custom_node_{submodule.replace('-', '_')}", init_path)
                if module:
                    # Handle node mappings
                    if hasattr(module, "NODE_CLASS_MAPPINGS"):
                        # Update node mappings
                        for node_name, node_class in module.NODE_CLASS_MAPPINGS.items():
                            # Add QHNodes category to the node class if it doesn't have a category
                            if not hasattr(node_class, "CATEGORY"):
                                node_class.CATEGORY = "🐟QHNodes"
                            elif not node_class.CATEGORY.startswith("QHNodes"):
                                # If it has a category, prepend QHNodes to it
                                original_category = node_class.CATEGORY
                                if "/" in original_category:
                                    # Handle nested categories
                                    categories = original_category.split("/")
                                    categories = [add_fish_emoji(cat) for cat in categories]
                                    node_class.CATEGORY = f"🐟QHNodes/{'/'.join(categories)}"
                                else:
                                    node_class.CATEGORY = f"🐟QHNodes/{add_fish_emoji(original_category)}"
                            else:
                                # If it already starts with QHNodes, just ensure it has the fish emoji
                                node_class.CATEGORY = add_fish_emoji(node_class.CATEGORY)
                            submodule_nodes[node_name] = node_class

                    if hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS"):
                        submodule_display_names.update(module.NODE_DISPLAY_NAME_MAPPINGS)

                    # Copy web files from submodule if they exist
                    if hasattr(module, "WEB_DIRECTORY"):
                        submodule_web_dir = os.path.join(submodule_path, module.WEB_DIRECTORY.replace("./", ""))
                        if os.path.exists(submodule_web_dir):
                            copy_web_files(submodule_web_dir, main_web_dir, submodule)
                    else:
                        # Check for default web directory
                        default_web_dir = os.path.join(submodule_path, "web")
                        if os.path.exists(default_web_dir):
                            copy_web_files(default_web_dir, main_web_dir, submodule)
    
    return submodule_nodes, submodule_display_names
