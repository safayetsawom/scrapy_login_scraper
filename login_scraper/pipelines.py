import json
import sqlite3

class LoginScraperPipeline:

    def open_spider(self, spider):
        self.seen_texts = set()

        # --- Database setup ---
        self.connection = sqlite3.connect("quotes.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                author TEXT NOT NULL,
                tags TEXT
            )
        """)
        self.connection.commit()

        # --- JSON setup ---
        self.file = open("quotes_clean.json", "w", encoding="utf-8")
        self.file.write("[\n")
        self.first_item = True

        spider.logger.info("🚀 Pipeline opened! Database and JSON ready.")

    def process_item(self, item, spider):
        # Clean
        item["text"] = item["text"].strip()
        item["author"] = item["author"].strip()

        # Duplicate check
        if item["text"] in self.seen_texts:
            spider.logger.warning(f"⚠️ Duplicate skipped: {item['text'][:30]}")
            return item

        # Validate
        if not item["author"]:
            spider.logger.warning("⚠️ Missing author, skipping.")
            return item

        tags_string = ", ".join(item.get("tags", []))

        # --- Save to database ---
        self.cursor.execute("""
            INSERT INTO quotes (text, author, tags)
            VALUES (?, ?, ?)
        """, (item["text"], item["author"], tags_string))
        self.connection.commit()

        # --- Save to JSON ---
        if not self.first_item:
            self.file.write(",\n")
        json.dump(dict(item), self.file, ensure_ascii=False, indent=2)
        self.first_item = False

        self.seen_texts.add(item["text"])
        return item

    def close_spider(self, spider):
        # Close database
        self.connection.close()

        # Close JSON
        self.file.write("\n]")
        self.file.close()

        spider.logger.info(f"✅ Done! {len(self.seen_texts)} quotes saved to both quotes.db and quotes_clean.json")