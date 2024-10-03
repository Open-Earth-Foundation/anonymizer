import json


def export_to_json(data, filename):

    path = f"./output/{filename}"
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Output successfully written to {path}")
    except Exception as e:
        print(f"Error writing output to file: {str(e)}")
