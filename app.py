import streamlit as st

# Force wide mode optimized for iPad landscape view
st.set_page_config(layout="wide", page_title="Omai Rice Bar - Kitchen POS Hub")

# Initialize session state for password/PIN verification
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- PASSWORD LOCK SCREEN ---
if not st.session_state.authenticated:
    st.markdown("""
        <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #121212;
            color: #FFFFFF;
            text-align: center;
        }
        div.stButton > button {
            background-color: #2c2c2e !important;
            color: white !important;
            border: 2px solid #48484a !important;
            padding: 15px !important;
            font-size: 24px !important;
            font-weight: bold !important;
            border-radius: 12px !important;
            width: 100% !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.write("## 🔒 Staff Login Required")
    password_input = st.text_input("Enter Kitchen Access Code", type="password")
    
    CORRECT_PIN = "1234" 
    
    if st.button("🔓 Access Recipes"):
        if password_input == CORRECT_PIN:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect code. Try again.")
    st.stop()

# --- MAIN APP CODE (Only runs if authenticated) ---
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #121212;
        color: #FFFFFF;
    }
    div.stButton > button {
        background-color: #2c2c2e !important;
        color: white !important;
        border: 2px solid #48484a !important;
        padding: 20px 10px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        width: 100% !important;
        margin-bottom: 10px !important;
        transition: all 0.2s ease;
    }
    div.stButton > button:active {
        background-color: #ff9500 !important;
        border-color: #ffb340 !important;
    }
    .recipe-title {
        font-size: 38px !important;
        font-weight: 800;
        color: #ff9500;
        margin-bottom: 2px;
    }
    .recipe-meta {
        font-size: 20px !important;
        color: #8e8e93;
        margin-bottom: 15px;
    }
    .ingredient-row {
        font-size: 24px !important;
        padding: 10px 0px;
        border-bottom: 1px solid #2c2c2e;
    }
    .qty-highlight {
        color: #34c759;
        font-weight: bold;
    }
    .method-header {
        font-size: 28px !important;
        font-weight: bold;
        color: #ff9500;
        margin-top: 25px;
        margin-bottom: 10px;
    }
    .method-step {
        font-size: 22px !important;
        line-height: 1.5 !important;
        margin-bottom: 12px;
        color: #e5e5ea;
    }
    </style>
""", unsafe_allow_html=True)

# FULL RECIPE BOOK DATABASE
RECIPES = {
    "Salads & Pickles": {
        "Bean Sprout Salad (5KG Base)": {
            "meta": "HALAL | Makes 7L (Use 12L Cambro)",
            "ingredients": [
                {"name": "Raw Bean Sprouts", "base_qty": 5000, "unit": "g"},
                {"name": "Fish Sauce", "base_qty": 198, "unit": "g"},
                {"name": "Garlic (Blitzed)", "base_qty": 110, "unit": "g"},
                {"name": "Sesame Oil", "base_qty": 132, "unit": "g"},
                {"name": "Salt", "base_qty": 80, "unit": "g"}
            ],
            "steps": [
                "Steam Bean Sprouts in Rotational for 2 minutes @ 211°F.",
                "Strain Bean Sprouts and shock in ice water to cool completely.",
                "In a separate bowl, mix Fish Sauce, Blitzed Garlic, and Sesame Oil.",
                "Add cooled Bean Sprouts to the dressing mixture and mix thoroughly.",
                "Check daily and adjust seasoning with Salt if needed."
            ]
        },
        "Bean Sprout Salad (9KG Bulk)": {
            "meta": "HALAL | Makes 11L (Use 12L Cambro)",
            "ingredients": [
                {"name": "Raw Bean Sprouts", "base_qty": 9000, "unit": "g"},
                {"name": "Fish Sauce", "base_qty": 360, "unit": "g"},
                {"name": "Garlic (Blitzed)", "base_qty": 200, "unit": "g"},
                {"name": "Sesame Oil", "base_qty": 240, "unit": "g"},
                {"name": "Salt", "base_qty": 200, "unit": "g"}
            ],
            "steps": [
                "Steam Bean Sprouts in Rotational for 2 minutes @ 211°F.",
                "Strain Bean Sprouts and shock in ice water to cool completely.",
                "In a separate bowl, mix Fish Sauce, Blitzed Garlic, and Sesame Oil.",
                "Add cooled Bean Sprouts to the dressing mixture and mix thoroughly.",
                "Check daily and adjust seasoning with Salt if needed."
            ]
        },
        "Cabbage Kimchi Coleslaw": {
            "meta": "HALAL | x20 Yield Batch (Makes 40L) - Use 50L Blue or Green Bin",
            "ingredients": [
                {"name": "Green Cabbage", "base_qty": 20000, "unit": "g"},
                {"name": "Kimchi", "base_qty": 10000, "unit": "g"},
                {"name": "Sugar", "base_qty": 2000, "unit": "g"},
                {"name": "Lemon Juice", "base_qty": 2000, "unit": "g"},
                {"name": "Salt", "base_qty": 600, "unit": "g"}
            ],
            "steps": [
                "Quarter cabbages and remove stems completely.",
                "Use the Robot Coupe unit to slice the cabbages cleanly.",
                "Gently massage the sliced cabbage with the Salt, Sugar, and Lemon Juice.",
                "Let the massaged cabbage sit undisturbed for 15 minutes.",
                "Squeeze all excess moisture out of the cabbage thoroughly.",
                "Slice the Kimchi to a thickness similar to the cabbage strip profile.",
                "Mix the sliced kimchi and squeezed cabbage together completely."
            ]
        },
        "Daikon Pickle": {
            "meta": "HALAL | Standard Base Yield Profile",
            "ingredients": [
                {"name": "Daikon", "base_qty": 1000, "unit": "g"},
                {"name": "Water", "base_qty": 600, "unit": "g"},
                {"name": "Rice Vinegar", "base_qty": 400, "unit": "g"},
                {"name": "Sugar", "base_qty": 340, "unit": "g"},
                {"name": "Salt", "base_qty": 25, "unit": "g"}
            ],
            "steps": [
                "Peel and cut raw Daikon into quarter moon circle pieces.",
                "Process through the Robot Coupe to slice down efficiently.",
                "Combine the Water, Rice Vinegar, Sugar, and Salt in a pot.",
                "Bring the combined pickling liquid mixture up to a hard boil.",
                "Pour boiling pickling liquid directly over the sliced Daikon until it is fully covered.",
                "Allow the mixture to cool down completely before putting into storage container units."
            ]
        },
        "Garlic Chives Kimchi": {
            "meta": "HALAL | Store sealed up to 2 weeks cold",
            "ingredients": [
                {"name": "Garlic Chives", "base_qty": 1000, "unit": "g"},
                {"name": "Tamari", "base_qty": 100, "unit": "g"},
                {"name": "Sugar", "base_qty": 50, "unit": "g"},
                {"name": "Gochujang Sauce", "base_qty": 40, "unit": "g"},
                {"name": "Rice Flour", "base_qty": 30, "unit": "g"},
                {"name": "Gochu Garu", "base_qty": 20, "unit": "g"}
            ],
            "steps": [
                "Cut the fresh Garlic Chives clean into even 2-inch pieces.",
                "Combine all remaining ingredients except the chives into a smooth, uniform seasoning paste.",
                "Gently massage the prepared seasoning paste deep into the pieces of chives.",
                "Leave the finished Kimchi ambient at room temperature or in a designated warm spot for 2 hours.",
                "Refrigerate, store up to 2 weeks."
            ]
        }
    },
    "Mains & Marinated Proteins": {
        "BBQ Beef Brisket": {
            "meta": "HALAL | Long Roast Setting Setup",
            "ingredients": [
                {"name": "Salt", "base_qty": 600, "unit": "g"},
                {"name": "Black Pepper Powder", "base_qty": 400, "unit": "g"},
                {"name": "Smoking Wood Chips", "base_qty": 1, "unit": "Fill Smoker Box"}
            ],
            "steps": [
                "Thoroughly combine measured salt and pepper rub mix.",
                "Season the raw brisket portion generously across all surfaces.",
                "Cold smoke the seasoned meat using the Rational oven layout for 2 hours.",
                "You may get ahead on smoking before cooking.",
                "Roast brisket in combination setting at 100% humidity, 202°F for 15 hours."
            ]
        },
        "Bulgogi Marinated Beef": {
            "meta": "HALAL | High-Volume Savory Marinade Mix",
            "ingredients": [
                {"name": "White Sugar", "base_qty": 150, "unit": "g"},
                {"name": "Mirin", "base_qty": 150, "unit": "g"},
                {"name": "Tamari", "base_qty": 150, "unit": "g"},
                {"name": "Water", "base_qty": 100, "unit": "g"},
                {"name": "Sesame Oil", "base_qty": 30, "unit": "g"},
                {"name": "Garlic", "base_qty": 20, "unit": "g"},
                {"name": "White Vinegar", "base_qty": 15, "unit": "g"},
                {"name": "Corn Starch", "base_qty": 15, "unit": "g"},
                {"name": "Ginger", "base_qty": 10, "unit": "g"},
                {"name": "Dashida (Beef Stock Powder)", "base_qty": 5, "unit": "g"},
                {"name": "Black Pepper", "base_qty": 3, "unit": "g"}
            ],
            "steps": [
Use code with caution.
"Grind Garlic, Ginger finely with Mirin in the Vitamix.",
"Then mix everything together.",
"Bring to boil, let cool."
]
},
"Chicken Brine Formulation": {
"meta": "HALAL | 24-Hour Deep Structural Brining",
"ingredients": [
{"name": "Water", "base_qty": 2000, "unit": "g"},
{"name": "Salt", "base_qty": 100, "unit": "g"},
{"name": "Soy Sauce", "base_qty": 50, "unit": "g"},
{"name": "Sugar", "base_qty": 20, "unit": "g"},
{"name": "Garlic (Crushed)", "base_qty": 15, "unit": "g"},
{"name": "Ginger (Crushed)", "base_qty": 15, "unit": "g"}
],
"steps": [
"Whisk all ingredients together until Sugar dissolves.",
"Brine Chicken For 24 Hours."
]
},
"Chicken Fry Batter Mix": {
"meta": "HALAL | Light Aerated Fry Coating",
"ingredients": [
{"name": "All Purpose Flour", "base_qty": 205, "unit": "g"},
{"name": "Soy Sauce", "base_qty": 10, "unit": "g"},
{"name": "Salt", "base_qty": 3, "unit": "g"},
{"name": "Club Soda (Chilled)", "base_qty": 1, "unit": "can"}
],
"steps": [
"Whisk all ingredients together until no lumps."
]
},
"Dashi Egg Prep & Marinade": {
"meta": "NOT HALAL | Formulated for 60 Eggs batch - Use 5.7L Cambro",
"ingredients": [
{"name": "Water", "base_qty": 2000, "unit": "g"},
{"name": "Tamari Soy Sauce", "base_qty": 300, "unit": "g"},
{"name": "Sugar", "base_qty": 100, "unit": "g"},
{"name": "Mirin", "base_qty": 100, "unit": "g"},
{"name": "Salt", "base_qty": 25, "unit": "g"},
{"name": "Hon Dashi", "base_qty": 24, "unit": "g"},
{"name": "Whole Raw Eggs", "base_qty": 60, "unit": "pcs"}
],
"steps": [
"Preheat Combi Oven to Steam 212°F.",
"Put one layer of Eggs on a perforated hotel pan.",
"Steam the Eggs for 8 minutes.",
"Immediately shock Eggs in cold running water until cool then peel.",
"Combine all ingredients and bring to boil then let cool.",
"Place peeled eggs into cold marinade and leave overnight."
]
},
"Garlic Shrimp Marinade": {
"meta": "HALAL | Clean Aromatic Seafood Marinade Base",
"ingredients": [
{"name": "Green Onion", "base_qty": 200, "unit": "g"},
{"name": "Canola Oil", "base_qty": 150, "unit": "g"},
{"name": "Garlic", "base_qty": 100, "unit": "g"},
{"name": "White Vinegar", "base_qty": 20, "unit": "g"},
{"name": "Ginger", "base_qty": 20, "unit": "g"},
{"name": "Salt", "base_qty": 5, "unit": "g"},
{"name": "Black Pepper", "base_qty": 2, "unit": "g"}
],
"steps": [
"Whisk together oil, vinegar, seasonings, and minced aromatics until emulsified."
]
},
"Mushroom Braised Reduction": {
"meta": "HALAL | Savory Concentrated Umami Glaze Base",
"ingredients": [
{"name": "Shimeji Mushrooms", "base_qty": 275, "unit": "g"},
{"name": "Water (Braise Liquid)", "base_qty": 250, "unit": "g"},
{"name": "Water (Soaking Liquid)", "base_qty": 250, "unit": "g"},
{"name": "Soy Sauce", "base_qty": 100, "unit": "g"},
{"name": "Sugar", "base_qty": 20, "unit": "g"},
{"name": "Ginger", "base_qty": 20, "unit": "g"},
{"name": "Kombu Sheet", "base_qty": 10, "unit": "g"},
{"name": "Shiitake Mushroom (Dried)", "base_qty": 1, "unit": "pc"}
],
"steps": [
"Soak shiitake with water overnight.",
"Combine everything into a pot and simmer mushrooms for 30 minutes."
]
}
},
"Sauces & Condiments": {
"House Mayo Base": {
"meta": "HALAL | Base Yield (Makes 6L) - Use 15L Container",
"ingredients": [
{"name": "Hellman's Mayo", "base_qty": 5000, "unit": "g"},
{"name": "Lemon Juice", "base_qty": 500, "unit": "g"},
{"name": "Dashida / Mushroom Powder", "base_qty": 100, "unit": "g"}
],
"steps": [
"Mix Dashida/Mushroom Powder into Lemon Juice until dissolved.",
"Whisk mix into Mayo."
]
},
"Chojang Sauce Base": {
"meta": "HALAL | Tangy Korean Hot Sauce Glaze Base",
"ingredients": [
{"name": "Gochujang Sauce", "base_qty": 6300, "unit": "g"},
{"name": "Sugar", "base_qty": 3700, "unit": "g"},
{"name": "Rice Vinegar", "base_qty": 3300, "unit": "g"},
{"name": "Brown Sugar", "base_qty": 500, "unit": "g"},
{"name": "Salt", "base_qty": 250, "unit": "g"},
{"name": "Hon Dashi (Fish Stock Powder)", "base_qty": 130, "unit": "g"}
],
"steps": [
"Whisk Sugars, Salt, Hon Dashi into Rice Vinegar.",
"Add Gochujang last and whisk until Hon Dashi and sugars dissolve."
]
},
"Hot Mustard Mayo": {
"meta": "NOT HALAL | Creamy Pungent Condiment Spread",
"ingredients": [
{"name": "Hellman's Mayo", "base_qty": 800, "unit": "g"},
{"name": "Dijon Mustard", "base_qty": 440, "unit": "g"},
{"name": "Lemon Juice", "base_qty": 120, "unit": "g"},
{"name": "Mirin", "base_qty": 100, "unit": "g"},
{"name": "Rice Vinegar", "base_qty": 80, "unit": "g"},
{"name": "Sugar", "base_qty": 60, "unit": "g"}
],
"steps": [
"Whisk all ingredients together."
]
},
"Hot Sauce (House Habanero)": {
"meta": "HALAL | Intensely Fiery Pepper Reduction Glaze",
"ingredients": [
{"name": "Habanero Peppers", "base_qty": 2000, "unit": "g"},
{"name": "Sherry Vinegar", "base_qty": 1200, "unit": "g"},
{"name": "Water", "base_qty": 700, "unit": "g"},
{"name": "Bell Peppers (Mixed colors)", "base_qty": 500, "unit": "g"},
{"name": "Sugar", "base_qty": 100, "unit": "g"},
{"name": "Salt", "base_qty": 100, "unit": "g"}
],
"steps": [
"Cut Habanero and Bell Peppers into pieces.",
"Grind Peppers in Vitamix.",
"Whisk all ingredients together."
]
},
"Japanese Curry Base": {
"meta": "HALAL | Deep Comforting Base Layout",
"ingredients": [
{"name": "Onions", "base_qty": 600, "unit": "g"},
{"name": "Carrots", "base_qty": 450, "unit": "g"},
{"name": "Potatoes", "base_qty": 300, "unit": "g"},
{"name": "Salt", "base_qty": 15, "unit": "g"},
{"name": "Dashida / Mushroom Powder", "base_qty": 10, "unit": "g"},
{"name": "Dashi Liquid", "base_qty": 2000, "unit": "ml"},
{"name": "Sesame oil", "base_qty": 1, "unit": "To Taste"}
],
"steps": [
"Sauté chopped vegetables with sesame oil in a pot until softened.",
"Add dashi liquid, seasonings, and simmer until thick and tender."
]
},
"KFC Sauce (Kang-Jeong)": {
"meta": "HALAL | Sticky Korean Fried Chicken Glaze Sauce",
"ingredients": [
{"name": "Corn Syrup", "base_qty": 2500, "unit": "g"},
{"name": "Ketchup", "base_qty": 1500, "unit": "g"},
{"name": "Gochujang", "base_qty": 500, "unit": "g"},
{"name": "Minced Garlic", "base_qty": 300, "unit": "g"},
{"name": "Tamari", "base_qty": 200, "unit": "g"},
{"name": "MSG", "base_qty": 10, "unit": "g"}
],
"steps": [
"Mix all ingredients together."
]
},
"Miso Glaze Formulation": {
"meta": "NOT HALAL | Sweet Umami Finishing Sauce Coating",
"ingredients": [
{"name": "Teriyaki", "base_qty": 100, "unit": "g"},
{"name": "Miso Paste", "base_qty": 15, "unit": "g"},
{"name": "Cornstarch Slurry", "base_qty": 1, "unit": "To Taste"}
],
"steps": [
"Whisk together teriyaki and miso paste.",
"Gently heat until a simmer.",
"Make a cornstarch slurry with cold water.",
"Whisk in slurry slowly and simmer for 1 min."
]
},
"Miso Marinade Paste": {
"meta": "NOT HALAL | Thick Concentrate Protein Coating Marinade",
"ingredients": [
{"name": "Miso", "base_qty": 1000, "unit": "g"},
{"name": "Sugar", "base_qty": 600, "unit": "g"},
{"name": "Water", "base_qty": 400, "unit": "g"},
{"name": "Mirin", "base_qty": 200, "unit": "g"},
{"name": "Soy", "base_qty": 150, "unit": "g"}
],
"steps": [
"Whisk all ingredients together."
]
},
"Pickled Jalapeño Blend": {
"meta": "HALAL | Hot Tangy Brined Jalapeño Blend",
"ingredients": [
{"name": "Jalapeño", "base_qty": 1800, "unit": "g"},
{"name": "Sugar", "base_qty": 500, "unit": "g"},
{"name": "Tamari", "base_qty": 500, "unit": "g"},
{"name": "Water", "base_qty": 500, "unit": "g"},
{"name": "White Vinegar", "base_qty": 500, "unit": "g"},
{"name": "Salt", "base_qty": 20, "unit": "g"},
{"name": "Garlic Cloves", "base_qty": 10, "unit": "pcs"}
],
"steps": [
"Peel and cut carrots, onion, ginger into small chunks.",
"Combine all ingredients into a Vitamix, blend until smooth."
]
}
}
}

--- STEP 1: CATEGORY SELECTION GRID ---

st.write("### 🗂️ 1. Choose Category")
categories = list(RECIPES.keys())
if "selected_category" not in st.session_state:
st.session_state.selected_category = categories[0]
cat_cols = st.columns(len(categories))
for idx, cat in enumerate(categories):
with cat_cols[idx]:
label = f"📁 {cat}" if st.session_state.selected_category == cat else cat
if st.button(label, key=f"cat_{cat}"):
st.session_state.selected_category = cat
st.session_state.selected_recipe = list(RECIPES[cat].keys())[0]
st.rerun()
if "selected_recipe" not in st.session_state or st.session_state.selected_recipe not in RECIPES[st.session_state.selected_category]:
st.session_state.selected_recipe = list(RECIPES[st.session_state.selected_category].keys())[0]
if "multiplier" not in st.session_state:
st.session_state.multiplier = 1
st.write("---")

--- STEP 2: RECIPE SELECTION GRID ---

st.write(f"### 🍽️ 2. Select Recipe ({st.session_state.selected_category})")
current_recipes = list(RECIPES[st.session_state.selected_category].keys())
rec_cols = st.columns(3)
for idx, rec in enumerate(current_recipes):
col_idx = idx % 3
with rec_cols[col_idx]:
label = f"⭐ {rec}" if st.session_state.selected_recipe == rec else rec
if st.button(label, key=f"rec_{rec}"):
st.session_state.selected_recipe = rec
st.rerun()
st.write("---")

--- STEP 3: MULTIPLIER AND INGREDIENT DISPLAY ---

if st.session_state.selected_recipe:
recipe_name = st.session_state.selected_recipe
recipe_data = RECIPES[st.session_state.selected_category][recipe_name]
ingredients = recipe_data["ingredients"]
steps = recipe_data["steps"]
display_col1, display_col2 = st.columns(2)
with display_col1:
st.write("### 🎛️ 3. Batch Size")
if st.button("1x Base Batch", type="primary" if st.session_state.multiplier == 1 else "secondary"):
st.session_state.multiplier = 1
st.rerun()
if st.button("2x Double Batch", type="primary" if st.session_state.multiplier == 2 else "secondary"):
st.session_state.multiplier = 2
st.rerun()
if st.button("4x Quadruple Batch", type="primary" if st.session_state.multiplier == 4 else "secondary"):
st.session_state.multiplier = 4
st.rerun()
if st.button("10x Bulk Batch", type="primary" if st.session_state.multiplier == 10 else "secondary"):
st.session_state.multiplier = 10
st.rerun()
with display_col2:
st.markdown(f'{recipe_name}', unsafe_allow_html=True)
st.markdown(f'{recipe_data["meta"]} — Scaling Level: {st.session_state.multiplier}x', unsafe_allow_html=True)
st.write("📋 Scaled Ingredient List:")
for ing in ingredients:
scaled_qty = ing["base_qty"] * st.session_state.multiplier
formatted_qty = int(scaled_qty) if scaled_qty % 1 == 0 else round(scaled_qty, 2)
formatted_qty_str = f"{formatted_qty:,}"
st.markdown(
f'{formatted_qty_str} {ing["unit"]} — {ing["name"]}',
unsafe_allow_html=True
)
st.markdown('🍳 Preparation Steps', unsafe_allow_html=True)
for i, step in enumerate(steps, 1):
st.markdown(f'{i}. {step}', unsafe_allow_html=True)
