import json
from pathlib import Path


class StudentRecord:
    def __init__(self, name, score):
        name = name.strip()
        score = float(score)
        if not name:
            raise ValueError("Name cannot be empty.")
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100.")
        self.name = name
        self.score = score

    def as_dict(self):
        return {"name": self.name, "score": self.score}


class StudentStore:
    def __init__(self, path):
        self.path = Path(path)

    def save(self, records):
        with self.path.open("w", encoding="utf-8") as file:
            json.dump([record.as_dict() for record in records], file, indent=2)

    def load(self):
        try:
            with self.path.open(encoding="utf-8") as file:
                data = json.load(file)
            return [StudentRecord(item["name"], item["score"]) for item in data]
        except FileNotFoundError:
            print("No saved file yet; starting with an empty list.")
            return []
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            print(f"Could not read saved records: {error}")
            return []


def main():
    store = StudentStore(Path(__file__).with_name("students.json"))
    records = store.load()
    try:
        name = input("Student name: ")
        score = input("Score (0–100): ")
        records.append(StudentRecord(name, score))
        store.save(records)
        print("Saved records:")
        for record in records:
            print(f"- {record.name}: {record.score:g}")
    except (ValueError, OSError) as error:
        print(f"Unable to add/save record: {error}")


if __name__ == "__main__":
    main()
