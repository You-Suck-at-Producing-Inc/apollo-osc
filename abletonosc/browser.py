try:
    import Live
except ImportError:
    print("ImportError: Unable to import Live")
# from typing import Tuple, Any, Callable, Optional
# from functools import partial
from .handler import AbletonOSCHandler
import os

from .data_structures import LiveDeviceTree # TODO: reload this properly so you don't have to restart OSC ahhh

class BrowserHandler(AbletonOSCHandler):
    def __init__(self, manager):
        super().__init__(manager)
        self.class_identifier = "browser"

    def init_api(self):
        temp_dir = '/tmp'
        self.browser = Live.Application.get_application().browser
        # self.chain = Live.Application.get_application().chain

        methods = [
            "load_item",
            "preview_item",
            "stop_preview"
        ]
        properties_r = [
            #"audio_effects",
            #"clips",
            #"drums",
            "instruments",
            #"packs",
            #"samples",
            #"sounds",
            #"user_folders",
            #"user_library"
        ]

        # for method in methods:
        #     self.osc_server.add_handler(f"/live/browser/{method}", partial(self._call_method, self.browser, method))

        def get_browser_tree(category: str):
            device_tree = LiveDeviceTree(getattr(self.browser, category))
            temp_file_path = os.path.join(temp_dir, f'ableton_{category}_tree_data.pkl')

            # def traverse(node):
            #     uris = []
            #     if len(node.children) == 0:
            #         uris.append(node.uri)
            #     else:
            #         for child in node.children:
            #             uris.extend(traverse(child))
            #     return uris
            
            device_tree.save_tree(temp_file_path)
            return temp_file_path
        
            result = [i.uri for i in self.browser.instruments.children]
            # for i in self.browser.instruments.children:
            #     print(i)
            #     print(i.uri)
            #     print(i.__module__)
            #     print(i.__dict__)
            #     print(dir(i))
            #     print("\n\n\n")
            return str(result) # iterate over self.browser.instruments.children --> <Browser.BrowserItemVector object at 0x10e4d57e8>
        
        def load_from_browser_tree(category: str, name: str):
            # if name == "":
            #     self.chain.delete_device(-1)
            #     return True
            live_tree = getattr(self.browser, category)
            device_tree = LiveDeviceTree(live_tree)
            browser_item = device_tree.find_corresponding_node(live_tree, name)
            if browser_item is not None:
                self.browser.load_item(browser_item)
                return browser_item.name
            return False # str((category, name, browser_item, str(device_tree)[:1000]))
        
        def get_drum_tree():
            category = "drums"
            device_tree = LiveDeviceTree(getattr(self.browser, category))
            temp_file_path = os.path.join(temp_dir, f'ableton_{category}_tree_data.pkl')

            # def traverse(node):
            #     uris = []
            #     if len(node.children) == 0:
            #         uris.append(node.uri)
            #     else:
            #         for child in node.children:
            #             uris.extend(traverse(child))
            #     return uris
            
            device_tree.save_tree(temp_file_path)
            return temp_file_path

        def load_from_drum_tree(name: str):
            live_tree = self.browser.drums
            device_tree = LiveDeviceTree(live_tree)
            browser_item = device_tree.find_corresponding_node(live_tree, name)
            if browser_item is not None:
                self.browser.load_item(browser_item)
                return browser_item.name
            return False # str((category, name, browser_item, str(device_tree)[:1000]))
        
        #assert 1 == 2, f"{device_tree.__class__}\n\n{device_tree.get_leaf_nodes()}"
        #assert 1 == 2, f"{device_tree}\n\n{device_tree.get_leaf_nodes()}\n\n{device_tree.get_nodes_by_parent(['Electric'])}\n\n{device_tree.get_nodes_by_type('instrument')}"
        
        #self.browser.preview_item(self.browser.instruments.children[0].children[1].children[0])
        #assert 1 == 2, f"{dir(self.browser)}\n\n{self.browser.instruments.children[0].children[0].children[0]}\n\n{self.browser.instruments.__module__}\n\n{self.browser.instruments}\n\n{self.browser.instruments.__dict__}\n\n{self.browser.instruments.__dir__()}"
        #self.osc_server.add_handler("/live/browser/get/instruments", lambda _: ("47",))
        for prop in properties_r:
            self.osc_server.add_handler(f"/live/browser/get/{prop}", lambda _: (get_browser_tree(prop),))
        self.osc_server.add_handler(f"/live/browser/get/audio_effects", lambda _: (get_browser_tree("audio_effects"),))
        self.osc_server.add_handler(f"/live/browser/get/drums", lambda _: (get_browser_tree("drums"),))
        # self.osc_server.add_handler("/live/browser/get/%s" % prop, lambda _: (get_browser_tree,))
        for prop in properties_r:
            self.osc_server.add_handler("/live/browser/set/%s" % prop, lambda name: (load_from_browser_tree(prop, name[0]),))
        self.osc_server.add_handler("/live/browser/set/audio_effects", lambda name: (load_from_browser_tree("audio_effects", name[0]),))
        self.osc_server.add_handler("/live/browser/set/drums", lambda name: (load_from_browser_tree("drums", name[0]),))
        # self.osc_server.add_handler("/live/browser/set/instruments", lambda _: (get_instruments(),))
        # for prop in properties_r:
        #     self.osc_server.add_handler("/live/browser/get/%s" % prop, partial(self._get_property, self.browser, prop))