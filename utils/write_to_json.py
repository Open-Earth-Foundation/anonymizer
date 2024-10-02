import json


def write_output_to_file(data, filename="output.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Output successfully written to {filename}")
    except Exception as e:
        print(f"Error writing output to file: {str(e)}")
