import json


class LoginScraperPipeline:

    def open_spider(self, spider):
        self.seen_texts = set()
        self.file = open("quotes_clean.json", "w", encoding="utf-8")
        self.file.write("[\n")
        self.first_item = True
        print("Pipeline opened!")

    def process_item(self, item):
        item["text"] = item["text"].strip()
        item["author"] = item["author"].strip()

        if item["text"] in self.seen_texts:
            return item

        if not item["author"]:
            return item

        if not self.first_item:
            self.file.write(",\n")

        json.dump(dict(item), self.file, ensure_ascii=False, indent=2)
        self.seen_texts.add(item["text"])
        self.first_item = False
        return item

    def close_spider(self, spider):
        self.file.write("\n]")
        self.file.close()
        print(f"Done! {len(self.seen_texts)} quotes saved.")