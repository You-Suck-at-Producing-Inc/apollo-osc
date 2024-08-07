try:
    import Live
except ImportError:
    print("ImportError: Unable to import Live")
from typing import Optional, Union, List
from .handler import AbletonOSCHandler
import os
import json
import tempfile

from .data_structures import LiveDeviceTree

class BrowserHandler(AbletonOSCHandler):
    def __init__(self, manager):
        super().__init__(manager)
        self.class_identifier = "browser"
        self.browser = Live.Application.get_application().browser
        self.temp_dir = tempfile.gettempdir()
        self.run_once = False

        self.properties_r = [
            "audio_effects",
            "clips",
            "drums",
            "instruments",
            "packs",
            "samples",
            "sounds",
            # "user_folders",
            # "user_library"
        ]

        temp_file_path = os.path.join(self.temp_dir, 'ableton_full_browser_tree_data.pkl')
        json_file_path = temp_file_path.replace('.pkl', '.json')

        full_tree = LiveDeviceTree()
        for category in self.properties_r:
            category_tree = LiveDeviceTree(getattr(self.browser, category))
            full_tree.merge_tree(category_tree)

        full_tree.save_tree(temp_file_path)
        
        full_tree_json = full_tree.to_json()
        with open(json_file_path, 'w') as f:
            json.dump(full_tree_json, f)

        self.run_once = True # could add a timer to refresh the tree

    def init_api(self):
        def get_browser_tree(category: str):
            device_tree = LiveDeviceTree(getattr(self.browser, category))
            temp_file_path = os.path.join(self.temp_dir, f'ableton_{category}_tree_data.pkl')
            
            device_tree.save_tree(temp_file_path)
            device_tree_json = device_tree.to_json()
            with open(temp_file_path.replace('.pkl', '.json'), 'w') as f:
                f.write(json.dumps(device_tree_json))
            return temp_file_path

        def get_full_browser_tree(_):
            temp_file_path = os.path.join(self.temp_dir, 'ableton_full_browser_tree_data.pkl')
            json_file_path = temp_file_path.replace('.pkl', '.json')

            if os.path.exists(temp_file_path) and self.run_once:
                return temp_file_path, json_file_path

            full_tree = LiveDeviceTree()
            for category in self.properties_r:
                category_tree = LiveDeviceTree(getattr(self.browser, category))
                full_tree.merge_tree(category_tree)

            full_tree.save_tree(temp_file_path)
            
            full_tree_json = full_tree.to_json()
            with open(json_file_path, 'w') as f:
                json.dump(full_tree_json, f)

            self.run_once = True # could add a timer to refresh the tree

            return temp_file_path, json_file_path

        self.osc_server.add_handler("/live/browser/get/full_tree", get_full_browser_tree)

        def load_from_browser_tree(name: str, category: Optional[Union[str, List[str]]] = None):
            full_tree = LiveDeviceTree()
            full_tree.load_tree_from_file(os.path.join(self.temp_dir, 'ableton_full_browser_tree_data.pkl'))
            
            for category in self.properties_r:
                browser_item = full_tree.find_corresponding_node(getattr(self.browser, category), name)
                if browser_item is not None:
                    self.browser.load_item(browser_item)
                    return browser_item.name
            return False

        self.osc_server.add_handler("/live/browser/set/device", lambda name: (load_from_browser_tree(name[0]),))