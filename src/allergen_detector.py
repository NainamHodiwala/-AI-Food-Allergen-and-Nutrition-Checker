import json
import requests
from rapidfuzz import fuzz

# Load allergen list from JSON
with open("data/allergens_list.json", "r") as f:
    ALLERGEN_DB = json.load(f)

def get_ingredients_from_barcode(barcode: str) -> str:
    """
    Fetch ingredients text using the OpenFoodFacts API.
    Example: Nutella → 3017620422003
    """
    try:
        url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        resp = requests.get(url)
        resp.raise_for_status()

        data = resp.json()
        product = data.get("product", {})
        ingredients = product.get("ingredients_text", "")

        if not ingredients:
            print("⚠️ No ingredients found for this product.")
        return ingredients
    except Exception as e:
        print(f"❌ API Error: {e}")
        return ""

def detect_allergens(text: str, threshold: int = 80):
    """
    Detect allergens in the given text using fuzzy matching.
    """
    detected = []
    text_lower = text.lower()

    for allergen in ALLERGEN_DB.keys():
        # Exact match
        if allergen in text_lower:
            detected.append(allergen)
        else:
            # Fuzzy match each word
            for word in text_lower.split():
                if fuzz.partial_ratio(allergen, word) > threshold:
                    detected.append(allergen)
                    break

    return list(set(detected))

if __name__ == "__main__":
    print("🔍 AI Food Allergen Detector")
    choice = input("Enter 1 for barcode, 2 for manual text input: ")

    if choice == "1":
        barcode = input("Enter product barcode: ")
        ingredients = get_ingredients_from_barcode(barcode)
        if ingredients:
            allergens = detect_allergens(ingredients)
            print(f"\n🧾 Ingredients: {ingredients}")
            print(f"🚨 Detected Allergens: {', '.join(allergens) if allergens else 'None'}")

    elif choice == "2":
        text = input("Paste the ingredient text: ")
        allergens = detect_allergens(text)
        print(f"🚨 Detected Allergens: {', '.join(allergens) if allergens else 'None'}")

    else:
        print("❌ Invalid choice.")
