try:
    import Live
except ImportError:
    print("ImportError: Unable to import Live")
from typing import Tuple, Any, Callable, Optional, Union, List
# from functools import partial
from .handler import AbletonOSCHandler
import os
import json

from .data_structures import LiveDeviceTree # TODO: reload this properly so you don't have to restart OSC ahhh

class BrowserHandler(AbletonOSCHandler):
    def __init__(self, manager):
        super().__init__(manager)
        self.class_identifier = "browser"

    def init_api(self):
        temp_dir = '/tmp'
        self.browser = Live.Application.get_application().browser

        # methods: load_item, preview_item, stop_preview
        properties_r = [
            "audio_effects",
            "clips",
            "drums",
            "instruments",
            "packs",
            "samples",
            "sounds",
            "user_folders",
            "user_library"
        ]

        def get_browser_tree(category: str):
            device_tree = LiveDeviceTree(getattr(self.browser, category))
            temp_file_path = os.path.join(temp_dir, f'ableton_{category}_tree_data.pkl')
            
            device_tree.save_tree(temp_file_path)
            device_tree_json = device_tree.to_json()
            with open(temp_file_path.replace('.pkl', '.json'), 'w') as f:
                f.write(json.dumps(device_tree_json))
            return temp_file_path
        
        def load_from_browser_tree(name: str, category: Optional[Union[str, List[str]]] = None):
            # if name == "":
            #     self.chain.delete_device(-1)
            #     return True
            categories = []
            if category is None:
                categories = properties_r
            for cat in categories:
                live_tree = getattr(self.browser, cat)
                device_tree = LiveDeviceTree(live_tree)
                browser_item = device_tree.find_corresponding_node(live_tree, name)
                if browser_item is not None:
                    self.browser.load_item(browser_item)
                    return browser_item.name
            return False # str((category, name, browser_item, str(device_tree)[:1000]))

        # DO NOT CHANGE THIS INTO A FOR LOOP - IT WILL BREAK
        self.osc_server.add_handler(f"/live/browser/get/instruments", lambda _: (get_browser_tree("instruments"),))
        self.osc_server.add_handler(f"/live/browser/get/audio_effects", lambda _: (get_browser_tree("audio_effects"),))
        self.osc_server.add_handler(f"/live/browser/get/clips", lambda _: (get_browser_tree("clips"),))
        self.osc_server.add_handler(f"/live/browser/get/drums", lambda _: (get_browser_tree("drums"),))
        self.osc_server.add_handler(f"/live/browser/get/packs", lambda _: (get_browser_tree("packs"),))
        self.osc_server.add_handler(f"/live/browser/get/samples", lambda _: (get_browser_tree("samples"),))
        self.osc_server.add_handler(f"/live/browser/get/sounds", lambda _: (get_browser_tree("sounds"),))
        self.osc_server.add_handler(f"/live/browser/get/user_folders", lambda _: (get_browser_tree("user_folders"),))
        self.osc_server.add_handler(f"/live/browser/get/user_library", lambda _: (get_browser_tree("user_library"),))
        self.osc_server.add_handler("/live/browser/set/device", lambda name: (load_from_browser_tree(name[0]),)) # general loading TODO: add specified optimized loading (even allowing tree branch passing)