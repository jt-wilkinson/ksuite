import json
import os

DB_PATH = "data/threads.json"


class ThreadDB:

    def __init__(self):

        if not os.path.exists(DB_PATH):
            self.data = {"barcodes": {}, "threads": {}}
            self.save()
        else:
            with open(DB_PATH) as f:
                self.data = json.load(f)

    def save(self):

        with open(DB_PATH, "w") as f:
            json.dump(self.data, f, indent=4)

    def lookup_barcode(self, barcode):

        thread_id = self.data["barcodes"].get(barcode)

        if not thread_id:
            return None

        return self.data["threads"].get(thread_id)

    def add_thread(self, barcode, brand, code, name, rgb):

        thread_id = f"{brand.lower()}_{code}"

        self.data["threads"][thread_id] = {
            "brand": brand,
            "code": code,
            "name": name,
            "rgb": rgb
        }

        self.data["barcodes"][barcode] = thread_id

        self.save()