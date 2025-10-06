import json

with open("data/allergens_list.json", "r") as f:
    ALLERGEN_DB = json.load(f)

def suggest_alternatives(allergens):
    """
    Suggest allergen-free alternatives based on detected allergens.
    """
    suggestions = {}
    for allergen in allergens:
        if allergen in ALLERGEN_DB:
            suggestions[allergen] = ALLERGEN_DB[allergen]
    return suggestions
