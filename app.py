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
        padding: 16px 10px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        width: 100% !important;
        margin-bottom: 8px !important;
        transition: all 0.2s ease;
    }
    div.stButton > button:active {
        background-color: #ff9500 !important;
        border-color: #ffb340 !important;
    }
    .recipe-title {
        font-size: 36px !important;
        font-weight: 800;
        color: #ff9500;
        margin-bottom: 2px;
    }
    .recipe-meta {
        font-size: 18px !important;
        color: #8e8e93;
        margin-bottom: 12px;
    }
    .ingredient-row {
        font-size: 22px !important;
        padding: 10px 0px;
        border-bottom: 1px solid #2c2c2e;
    }
    .qty-highlight {
        color: #34c759;
        font-weight: bold;
    }
    .method-header {
        font-size: 26px !important;
        font-weight: bold;
        color: #ff9500;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .method-step {
        font-size: 20px !important;
        line-height: 1.5 !important;
        margin-bottom: 10px;
        color: #e5e5ea;
    }
    </style>
""", unsafe_allow_html=True)

# FULL RECIPE BOOK DATABASE WITH CORRECT NOMENCLATURE & ALL CATEGORIES
RECIPES = {
    "Salads + Pickles": {
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
                "Squeeze all moisture out thoroughly.",
                "Slice Kimchi to similar thickness as cabbage.",
                "Mix together sliced kimchi and cabbage."
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
        },
        "Pickled Jalapeno": {
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
                "Thoroughly clean jalapeños and prepare garlic inputs.",
                "Place all measured liquid inputs, sugars, salts, and solid ingredients cleanly down into the Vitamix blender vessel.",
                "Run the blender unit engine systematically on high speed parameters until the mixture is completely smooth."
            ]
        }
    },
    "Mains + Marinades": {
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
        }
