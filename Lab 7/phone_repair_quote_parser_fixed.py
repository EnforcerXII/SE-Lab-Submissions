def mask_imei(imei):
    """
    Removes dashes and spaces, then hides all but the last four digits.
    Returns an empty string if imei is not a string or is empty after cleaning.
    """
    if not isinstance(imei, str):
        return ""
    imei = imei.replace('-', '').replace(' ', '')
    if not imei:
        return ""
    if len(imei) <= 4:
        # Too short to mask safely: hide everything rather than leak it
        return '*' * len(imei)
    return '*' * (len(imei) - 4) + imei[-4:]

def parse_parts_order(text):
    """
    Parses 'screen x1; battery x2' into a {part: quantity} dictionary.
    Malformed items (no 'x', empty part name, non-numeric or non-positive
    quantity) are skipped. Returns {} if text is not a string.
    """
    order = {}
    if not isinstance(text, str):
        return order
    for item in text.split(';'):
        if 'x' not in item:
            continue
        # rsplit so part names that contain an 'x' (e.g. 'box x2') still work
        part, qty = item.rsplit('x', 1)
        part, qty = part.strip(), qty.strip()
        if not part:
            continue
        try:
            qty = int(qty)
        except ValueError:
            continue
        if qty <= 0:
            continue
        order[part] = order.get(part, 0) + qty
    return order

def parse_model(text):
    """
    Splits 'Brand Model name' into a (brand, model) tuple.
    Returns None if text is not a string or has fewer than two words.
    """
    if not isinstance(text, str):
        return None
    parts = text.strip().split(None, 1)   # split on any whitespace
    if len(parts) < 2:
        return None
    brand, model = parts
    return brand.title(), model.strip()

def main():
    print("==== Running mask_imei ====")
    value = input("Enter an IMEI number (e.g. 35-209900-176148-1): ")
    print("Masked IMEI:", mask_imei(value))

    print("\n==== Running parse_parts_order ====")
    value = input("Enter parts and quantities as PART xQTY separated by ; (e.g. screen x1; battery x2): ")
    print("Parts order:", parse_parts_order(value))

    print("\n==== Running parse_model ====")
    value = input("Enter the phone brand and model (e.g. Samsung Galaxy S23): ")
    print("Brand and model:", parse_model(value))

if __name__ == "__main__":
    main()
