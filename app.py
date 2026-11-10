import streamlit as st
# Force wide mode optimized for iPad landscape view
st.set_page_config(layout="wide", page_title="Kitchen POS Recipe Hub")

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
    
    # Simple password field
    password_input = st.text_input("Enter Kitchen Access Code", type="password")
    
    # Set your password here
    CORRECT_PIN = "1234" 
    
    if st.button("🔓 Access Recipes"):
        if password_input == CORRECT_PIN:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect code. Try again.")
    st.stop() # Prevents anything below from loading unless authenticated

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
        font-size: 36px !important;
        font-weight: 800;
        color: #ff9500;
        margin-bottom: 5px;
    }
    .ingredient-row {
        font-size: 24px !important;
        padding: 12px 0px;
        border-bottom: 1px solid #2c2c2e;
    }
    .qty-highlight {
        color: #34c759;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 1. RECIPE DATABASE (Easily add your 30-40 recipes here)
RECIPES = {
    "Doughs & Breads": {
        "Pizza Dough (Bulk)": [
            {"name": "Bread Flour", "base_qty": 1000, "unit": "g"},
            {"name": "Water (Lukewarm)", "base_qty": 650, "unit": "g"},
            {"name": "Fine Sea Salt", "base_qty": 25, "unit": "g"},
            {"name": "Instant Yeast", "base_qty": 7, "unit": "g"},
            {"name": "Olive Oil", "base_qty": 20, "unit": "g"}
        ],
        "Brioche Buns": [
            {"name": "Flour", "base_qty": 500, "unit": "g"},
            {"name": "Butter (Softened)", "base_qty": 250, "unit": "g"},
            {"name": "Whole Eggs", "base_qty": 5, "unit": "pcs"},
            {"name": "Sugar", "base_qty": 50, "unit": "g"}
        ]
    },
    "Sauces & Dressings": {
        "House Marinara": [
            {"name": "San Marzano Tomatoes", "base_qty": 3, "unit": "cans"},
            {"name": "Olive Oil", "base_qty": 100, "unit": "ml"},
            {"name": "Minced Garlic", "base_qty": 40, "unit": "g"},
            {"name": "Fresh Basil", "base_qty": 15, "unit": "g"}
        ],
        "Garlic Aioli": [
            {"name": "Mayonnaise", "base_qty": 1, "unit": "qt"},
            {"name": "Garlic Cloves", "base_qty": 12, "unit": "pcs"},
            {"name": "Lemon Juice", "base_qty": 4, "unit": "tbsp"}
        ]
    },
    "Fillings & Proteins": {
        "Taco Seasoned Beef": [
            {"name": "Ground Beef", "base_qty": 5, "unit": "lbs"},
            {"name": "Spice Blend", "base_qty": 150, "unit": "g"},
            {"name": "Diced Onions", "base_qty": 2, "unit": "cups"}
        ]
    }
}

# Initialize session states so the app remembers what was tapped
if "selected_category" not in st.session_state:
    st.session_state.selected_category = list(RECIPES.keys())[0]
if "selected_recipe" not in st.session_state:
    st.session_state.selected_recipe = list(RECIPES[st.session_state.selected_category].keys())[0]
if "multiplier" not in st.session_state:
    st.session_state.multiplier = 1

# --- STEP 1: CATEGORY SELECTION GRID ---
st.write("### 🗂️ 1. Choose Category")
categories = list(RECIPES.keys())
cat_cols = st.columns(len(categories))

for idx, cat in enumerate(categories):
    with cat_cols[idx]:
        label = f"📁 {cat}" if st.session_state.selected_category == cat else cat
        if st.button(label, key=f"cat_{cat}"):
            st.session_state.selected_category = cat
            st.session_state.selected_recipe = list(RECIPES[cat].keys())[0]
            st.rerun()

st.write("---")

# --- STEP 2: RECIPE SELECTION GRID ---
st.write(f"### 🍽️ 2. Select Recipe ({st.session_state.selected_category})")
current_recipes = list(RECIPES[st.session_state.selected_category].keys())

rec_cols = st.columns(4)
for idx, rec in enumerate(current_recipes):
    col_idx = idx % 4
    with rec_cols[col_idx]:
        label = f"⭐ {rec}" if st.session_state.selected_recipe == rec else rec
        if st.button(label, key=f"rec_{rec}"):
            st.session_state.selected_recipe = rec
            st.rerun()

st.write("---")

# --- STEP 3: MULTIPLIER AND INGREDIENT DISPLAY ---
if st.session_state.selected_recipe:
    recipe_name = st.session_state.selected_recipe
    ingredients = RECIPES[st.session_state.selected_category][recipe_name]
    
    display_col1, display_col2 = st.columns()
    
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
        st.markdown(f'<div class="recipe-title">{recipe_name} ({st.session_state.multiplier}x Batch)</div>', unsafe_allow_html=True)
        st.write("Keep open on iPad while preparing:")
        
        for ing in ingredients:
            scaled_qty = ing["base_qty"] * st.session_state.multiplier
            formatted_qty = int(scaled_qty) if scaled_qty % 1 == 0 else round(scaled_qty, 2)
            st.markdown(
                f'<div class="ingredient-row"><span class="qty-highlight">{formatted_qty} {ing["unit"]}</span> — {ing["name"]}</div>', 
                unsafe_allow_html=True
            )
