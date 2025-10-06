import streamlit as st
import tempfile
import requests
from ocr_reader import extract_text
from allergen_detector import detect_allergens
from recommender import suggest_alternatives

# Optional: camera & barcode scanning
try:
    from streamlit import camera_input      # built-in Streamlit camera
    import cv2
    from pyzbar.pyzbar import decode
    import numpy as np
    CAMERA_AVAILABLE = True
except ImportError:
    CAMERA_AVAILABLE = False

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="AI Food Allergen & Nutrition Checker", layout="wide")
st.title("🥗 AI Food Allergen & Nutrition Checker")

# ---------------------- SIDEBAR NAVIGATION ----------------------
st.sidebar.header("🧭 Choose Mode")
mode = st.sidebar.radio(
    "Select Input Mode:",
    ["Upload Image", "Scan Barcode / Enter Product Name"]
)

# ---------------------- SESSION STATE ----------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "product_data" not in st.session_state:
    st.session_state.product_data = None

# ==========================================================
# MODE 1 → IMAGE UPLOAD
# ==========================================================
if mode == "Upload Image":
    st.header("📸 Upload a Food Label Image")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Save temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_path = tmp_file.name

        st.image(uploaded_file, caption="Uploaded Label", use_container_width=True)

        st.subheader("🔎 Extracting Text from Label...")
        text = extract_text(temp_path)
        st.text_area("Extracted Text", text, height=150)

        st.subheader("🚨 Allergen Detection")
        allergens = detect_allergens(text)
        if allergens:
            st.error(f"⚠️ Allergens detected: {', '.join(allergens)}")
            st.subheader("🌱 Suggested Alternatives")
            suggestions = suggest_alternatives(allergens)
            for allergen, alternatives in suggestions.items():
                st.markdown(f"**{allergen.capitalize()}** → {', '.join(alternatives)}")
        else:
            st.success("🎉 No common allergens detected!")
        from googletrans import Translator

        translator = Translator()

        ...

        if uploaded_file:
            ...
            st.subheader("🔎 Extracting Text from Label...")
            text = extract_text(temp_path)

            # 🔥 Translate to English
            translated = translator.translate(text, src='auto', dest='en').text

            st.text_area("📝 Original Text", text, height=150)
            st.text_area("🌎 Translated to English", translated, height=150)

            # Detect allergens from translated text
            st.subheader("🚨 Allergen Detection")
            allergens = detect_allergens(translated)


        # Save for chatbot
        st.session_state.product_data = {
            "name": "Uploaded Product",
            "ingredients": text,
            "nutriments": {}    # no nutrition info for uploaded image
        }

# ==========================================================
# MODE 2 → BARCODE / PRODUCT NAME
# ==========================================================
elif mode == "Scan Barcode / Enter Product Name":
    st.header("📱 Scan Barcode or Enter Product Name")

    barcode = None
    if CAMERA_AVAILABLE:
        camera_image = st.camera_input("📸 Use your camera to scan the barcode:")
        if camera_image is not None:
            # Convert image to array
            file_bytes = np.asarray(bytearray(camera_image.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            decoded_barcodes = decode(img)

            if decoded_barcodes:
                barcode = decoded_barcodes[0].data.decode("utf-8")
                st.success(f"✅ Detected Barcode: {barcode}")
            else:
                st.warning("❗ Could not detect a barcode. Try again or enter manually.")

    manual_query = st.text_input("Or enter barcode/product name manually:")

    if st.button("🔍 Fetch Product"):
        search_query = barcode if barcode else manual_query
        if search_query:
            with st.spinner("Fetching product details..."):
                if search_query.isdigit():
                    url = f"https://world.openfoodfacts.org/api/v0/product/{search_query}.json"
                    resp = requests.get(url)
                    data = resp.json()
                    product = data.get("product") if data.get("status") == 1 else None
                else:
                    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={search_query}&search_simple=1&json=1&page_size=1"
                    resp = requests.get(url)
                    results = resp.json().get("products", [])
                    product = results[0] if results else None

            if product:
                name = product.get("product_name", "Unknown Product")
                ingredients = product.get("ingredients_text", "No ingredients available.")
                nutriments = product.get("nutriments", {})

                st.success(f"✅ Found: **{name}**")
                st.text_area("🧾 Ingredients", ingredients, height=150)

                st.subheader("🚨 Allergen Detection")
                allergens = detect_allergens(ingredients)
                if allergens:
                    st.error(f"⚠️ Allergens detected: {', '.join(allergens)}")
                else:
                    st.success("🎉 No common allergens detected!")

                with st.expander("📊 Nutrition Facts"):
                    if nutriments:
                        st.json(nutriments)
                    else:
                        st.info("No nutrition data available.")

                # Save product for chatbot
                st.session_state.product_data = {
                    "name": name,
                    "ingredients": ingredients,
                    "nutriments": nutriments
                }
            else:
                st.warning("❌ No product found.")
        else:
            st.info("📥 Please scan or enter a barcode/product name.")

# ==========================================================
# INLINE CHATBOT
# ==========================================================
if st.session_state.product_data:
    st.markdown("---")
    st.subheader("🤖 Nutrition Chatbot")

    user_query = st.text_input("💬 Ask a question about this product (e.g., sugar, fat, calories):")

    if st.button("Ask"):
        q = user_query.lower()
        nutriments = st.session_state.product_data.get("nutriments", {})
        response = "🤔 I can answer about calories, sugar, fat, protein, fiber, salt, or carbs."

        if "calorie" in q or "energy" in q:
            response = f"{nutriments.get('energy-kcal_100g', 'N/A')} kcal per 100g"
        elif "sugar" in q:
            response = f"{nutriments.get('sugars_100g', 'N/A')} g sugar per 100g"
        elif "fat" in q:
            response = f"{nutriments.get('fat_100g', 'N/A')} g fat per 100g"
        elif "protein" in q:
            response = f"{nutriments.get('proteins_100g', 'N/A')} g protein per 100g"
        elif "fiber" in q:
            response = f"{nutriments.get('fiber_100g', 'N/A')} g fiber per 100g"
        elif "salt" in q or "sodium" in q:
            response = f"{nutriments.get('salt_100g', 'N/A')} g salt per 100g"
        elif "carb" in q:
            response = f"{nutriments.get('carbohydrates_100g', 'N/A')} g carbs per 100g"

        st.session_state.chat_history.append({"user": user_query, "bot": response})

    # Show chat history
    if st.session_state.chat_history:
        st.markdown("### 🗨️ Conversation History")
        for chat in st.session_state.chat_history:
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**Bot:** {chat['bot']}")
            st.markdown("---")
