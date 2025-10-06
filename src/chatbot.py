import requests

def get_nutrition_data(barcode: str):
    try:
        url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        resp = requests.get(url)
        resp.raise_for_status()
        product = resp.json().get("product", {})
        nutrition = product.get("nutriments", {})
        return {
            "name": product.get("product_name", "Unknown"),
            "energy_kcal": nutrition.get("energy-kcal_100g"),
            "fat": nutrition.get("fat_100g"),
            "saturated_fat": nutrition.get("saturated-fat_100g"),
            "carbohydrates": nutrition.get("carbohydrates_100g"),
            "sugars": nutrition.get("sugars_100g"),
            "proteins": nutrition.get("proteins_100g"),
            "salt": nutrition.get("salt_100g"),
            "vegan": "vegan" in product.get("labels_tags", []),
            "vegetarian": "vegetarian" in product.get("labels_tags", []),
        }
    except Exception as e:
        print("❌ Error fetching nutrition data:", e)
        return None


def chatbot_response(query: str, nutrition_data: dict):
    if not nutrition_data:
        return "I don't have data for that product yet."

    query = query.lower()
    if "calorie" in query or "energy" in query:
        return f"{nutrition_data['name']} has about {nutrition_data['energy_kcal']} kcal per 100g."
    elif "sugar" in query:
        return f"It contains around {nutrition_data['sugars']} g of sugar per 100g."
    elif "fat" in query and "saturated" in query:
        return f"Saturated fat: {nutrition_data['saturated_fat']} g per 100g."
    elif "fat" in query:
        return f"Total fat: {nutrition_data['fat']} g per 100g."
    elif "protein" in query:
        return f"Protein content: {nutrition_data['proteins']} g per 100g."
    elif "salt" in query or "sodium" in query:
        return f"Salt content: {nutrition_data['salt']} g per 100g."
    elif "vegan" in query:
        return "✅ Yes, it’s vegan!" if nutrition_data["vegan"] else "❌ No, it's not vegan."
    elif "vegetarian" in query:
        return "✅ Yes, it’s vegetarian!" if nutrition_data["vegetarian"] else "❌ No, it's not vegetarian."
    else:
        return "I can answer questions about calories, sugar, fat, protein, salt, and vegan/vegetarian info."
