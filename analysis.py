import csv


def is_number(x: str) -> bool:
    try:
        float(x)
        return True
    except Exception:
        return False


def analyze_csv(file_path: str) -> dict:

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return {"error": "CSV nema header (prvi red mora biti nazivi kolona)"}

        headers = reader.fieldnames
        numeric_values = {h: [] for h in headers}
        rows_count = 0

        for row in reader:
            rows_count += 1
            for h in headers:
                value = (row.get(h) or "").strip().replace(",", ".")
                if value != "" and is_number(value):
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