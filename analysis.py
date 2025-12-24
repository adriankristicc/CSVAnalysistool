import csv


def is_number(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def analyze_csv(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            raise ValueError("CSV nema header")

        headers = reader.fieldnames
        numeric_values = {h: [] for h in headers}
        rows_count = 0

        for row in reader:
            rows_count += 1
            for h in headers:
                value = row[h].replace(",", ".")
                if is_number(value):
                    numeric_values[h].append(float(value))

    stats = {}
    for h, values in numeric_values.items():
        if values:
            stats[h] = {
                "min": min(values),
                "max": max(values),
                "avg": sum(values) / len(values),
                "count": len(values),
            }

    return {
        "file_path": file_path,
        "rows": rows_count,
        "columns": len(headers),
        "headers": headers,
        "numeric_stats": stats,
    }