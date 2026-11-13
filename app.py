
import streamlit as st
import hmac
from decimal import Decimal
from html import escape

# ==========================================================
# RICE IS LIFE — STAFF RECIPE BOOK
# ==========================================================

st.set_page_config(
    page_title="Rice Is Life | Recipe Book",
    page_icon="🍚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================================
# SETTINGS
# ==========================================================

CATEGORIES = [
    "Sauces + Dressings",
    "Mains + Marinades",
    "Salads + Pickles",
]

MULTIPLIERS = [
    1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30
]

SAUCE = CATEGORIES[0]
MAIN = CATEGORIES[1]
SALAD = CATEGORIES[2]

RECIPES = {}

# ==========================================================
# RECIPE DATA HANDLING
# ==========================================================

def add(name, category, ingredients, steps, notes=""):
    parsed = []

    for ingredient in ingredients.split(";"):
        if not ingredient.strip():
            continue

        parts = [p.strip() for p in ingredient.split("|")]

        if len(parts) != 3:
            raise ValueError(
                f"Invalid ingredient in {name}: {ingredient}"
            )

        item, amount, unit = parts

        parsed.append({
            "name": item,
            "amount": amount,
            "unit": unit,
        })

    RECIPES[name] = {
        "category": category,
        "ingredients": parsed,
        "steps": [
            step.strip()
            for step in steps.split("~")
            if step.strip()
        ],
        "notes": notes,
    }


# ==========================================================
# SAUCES + DRESSINGS
# ==========================================================

add(
    "BULGOGI SAUCE(KBBQ)", SAUCE,
    """
    White Sugar|150|g;
    Mirin|150|g;
    Tamari|150|g;
    Water|100|g;
    Sesame Oil|30|g;
    Garlic|20|g;
    White Vinegar|15|g;
    Corn Starch|15|g;
    Ginger|10|g;
    Dashida|5|g;
    Black Pepper|3|g
    """,
    """
    Grind garlic, ginger finely with mirin in Vitamix.~
    Mix everything together.~
    Bring to a boil, let cool.
    """
)

add(
    "CHOJANG (PORK BELLY)", SAUCE,
    """
    Gochujang Sauce|6300|g;
    Sugar|3700|g;
    Rice Vinegar|3300|g;
    Brown Sugar|500|g;
    Salt|250|g;
    Hon Dashi|130|g
    """,
    """
    Whisk sugars, salt and Hon Dashi into rice vinegar.~
    Whisk until Hon Dashi and sugars dissolved.~
    Add Gochujang last.
    """
)

add(
    "HOT MAYO MUSTARD", SAUCE,
    """
    Hellman's Mayo|800|g;
    Dijon Mustard|440|g;
    Lemon Juice|120|g;
    Mirin|100|g;
    Rice Vinegar|80|g;
    Sugar|60|g
    """,
    "Whisk all ingredients together."
)

add(
    "HOT SAUCE", SAUCE,
    """
    Habanero Peppers|2000|g;
    Sherry Vinegar|1200|g;
    Water|700|g;
    Bell Peppers|500|g;
    Sugar|100|g;
    Salt|100|g
    """,
    """
    Cut habanero and bell peppers into pieces.~
    Grind peppers in Vitamix.~
    Whisk all ingredients together.
    """,
    "Original notes: Green, red and orange habaneros; red and yellow bell peppers."
)

add(
    "HOUSE DRESSING", SAUCE,
    """
    White Vinegar|560|g;
    Carrots|540|g;
    Canola Oil|320|g;
    Onions|280|g;
    Sugar|120|g;
    Ginger|68|g;
    Miso Paste|32|g;
    Salt|24|g;
    Sesame Oil|20|g;
    Black Pepper|4|g
    """,
    """
    Peel carrots, onions and ginger.~
    Cut into small chunks.~
    Blend vegetables with vinegar in Vitamix until smooth.~
    Combine blended vegetables with remaining ingredients and whisk until smooth.
    """,
    "IMPORTANT: Original specifies making two separate 5X batches for 10X, NOT a 10X batch."
)

add(
    "HOUSE MAYO", SAUCE,
    """
    Hellman's Mayo|5000|g;
    Lemon Juice|500|g;
    Dashida/Mushroom Powder|100|g
    """,
    """
    Mix Dashida or mushroom powder into lemon juice until dissolved.~
    Whisk mixture into mayo.
    """,
    "Makes approximately 6L. Use a 15L container."
)

add(
    "KANG JEONG(KFC)", SAUCE,
    """
    Corn Syrup|2500|g;
    Ketchup|1500|g;
    Gochujang|500|g;
    Minced Garlic|300|g;
    Tamari|200|g;
    MSG|10|g
    """,
    "Mix all ingredients together."
)

add(
    "MISO GLAZE(SALMON)", SAUCE,
    """
    Teriyaki|100|g;
    Miso Paste|15|g;
    Cornstarch Slurry|?|to taste
    """,
    """
    Whisk together teriyaki and miso paste.~
    Gently heat until simmering. Do not let boil!
    Make a cornstarch slurry with cold water.~
    Whisk in slurry slowly and simmer for one minute.
    """,
    "Cornstarch slurry has no fixed quantity in the original."
)

add(
    "SEASONED SOY(GF)", SAUCE,
    """
    Tamari|2000|g;
    Water|1000|g;
    Mirin|900|g;
    Sake|600|g;
    Kombu|50|g;
    Bonito|25|g
    """,
    """
    Combine everything in a pot and bring to a boil.~
    Cool and infuse overnight, then strain.
    """,
    "Original recipe makes approximately 5L."
)

add(
    "SPICY MAYO", SAUCE,
    """
    Mayo|400|g;
    Gochujang|40|g;
    Sriracha|40|g;
    Lemon Juice|40|g;
    Sugar|20|g;
    Hot Sauce|27|g
    """,
    "Dissolve sugar in lemon juice, then mix all ingredients together."
)

add(
    "SUSHI SU", SAUCE,
    """
    Mizkan Yamabuki Vinegar|4000|g;
    Aka Su|600|g;
    Sugar|1750|g;
    Kosher Salt|600|g;
    Kombu|30|g
    """,
    "Whisk all ingredients in a Cambro until sugar and salt dissolve."
)

add(
    "TENTSUYU(TOFU)", SAUCE,
    """
    Water|400|g;
    Dashida / Mushroom Powder|8|g;
    Soy|200|g;
    Mirin|160|g;
    Sugar|20|g
    """,
    "Whisk everything together until dissolved."
)

add(
    "TERIYAKI SAUCE(CHICKEN)", SAUCE,
    """
    Tamari Soy Sauce|4000|g;
    Sugar|3000|g;
    Mirin|4000|g;
    Sake|4000|g;
    Garlic(Crushed)|300|g;
    Ginger(Crushed)|100|g;
    Water|130|g;
    Cornstarch|130|g
    """,
    """
    Combine tamari soy, sugar, garlic and ginger.~
    Simmer for 30 minutes until flavors are infused.~
    Remove garlic and ginger.~
    Reduce by 1/4 or until desired consistency.~
    Create a slurry with cornstarch and water if needed.~
    Whisk in slurry slowly and simmer for 1 minute.~
    Cool down.
    """,
    "Original recipe makes approximately 12 L."
)

add(
    "YUZU GARLIC SAUCE(OH-MY)", SAUCE,
    """
    Garlic|1100|g;
    Sugar|1000|g;
    Lemon Juice|825|g;
    Honey|500|g;
    Corn Syrup|500|g;
    Canola Oil|500|g;
    Yuzu|300|g;
    Yuzu Kosho|160|g;
    Water|100|g;
    Corn Starch|50|g;
    Chili Pepper Flakes|25|g
    """,
    """
    Confit garlic in canola oil until soft and golden.~
    Blend confit garlic and oil until smooth.~
    Combine all ingredients and bring to a boil.~
    Whisk in cornstarch slurry slowly and continue boiling for 1 minute.
    """
)

# ==========================================================
# MAINS + MARINADES
# ==========================================================

add(
    "BEEF BRISKET", MAIN,
    """
    Salt|600|g;
    Black Pepper Powder|400|g;
    Smoking Wood Chips|?|fill smoker
    """,
    """
    Mix salt and pepper.~
    Season brisket generously.~
    Cold smoke using the Rational for two hours.~
    Brisket can be smoked in advance.~
    Roast in combination setting at 100% humidity, 202°F for 15 hours.
    """
)

add(
    "CHICKEN BATTER", MAIN,
    """
    All Purpose Flour|205|g;
    Soy Sauce|10|g;
    Salt|3|g;
    Can of Club Soda|355|ml
    """,
    "Whisk all ingredients together until no lumps remain."
)

add(
    "CHICKEN BRINE", MAIN,
    """
    Water|2000|g;
    Soy Sauce|100|g;
    Salt|50|g;
    Sugar|20|g;
    Garlic(Crushed)|15|g;
    Ginger(Crushed)|15|g
    """,
    """
    Whisk all ingredients together until sugar dissolves.~
    Brine chicken for 24 hours.
    """
)

add(
    "DASHI EGG MARINADE", MAIN,
    """
    Water|2000|g;
    Tamari Soy Sauce|300|g;
    Sugar|100|g;
    Mirin|100|g;
    Salt|25|g;
    Hon Dashi|24|g;
    Eggs|60|eggs
    """,
    """
    Put 1 layer of eggs on a perforated hotel pan.~
    Preheat Combi oven to steam at 212°F for 8 minutes.~
    Immediately shock eggs in cold running water until cool, then peel.~
    Combine marinade ingredients, bring to a boil and let cool.~
    Place cooled peeled eggs into cold marinade and leave overnight.
    """,
    "Use 5.7L Cambro for the base batch."
)

add(
    "GARLIC SHRIMP", MAIN,
    """
    Green Onion Whites|200|g;
    Canola Oil|150|g;
    Garlic|100|g;
    White Vinegar|20|g;
    Ginger|20|g;
    Black Pepper|2|g;
    Salt|5|g
    """,
    "Mix all ingredients together."
)

add(
    "JAPANESE CURRY", MAIN,
    """
    Onions|600|g;
    Carrots|450|g;
    Potatoes|300|g;
    Salt|10|g;
    Dashida / Mushroom Powder|10|g;
    Sesame Oil|?|to taste;
    Dashi|1.5|L
    """,
    "",
    "Salt to taste 10-15g Max. Dashi 1.5-2L to taste."
)

add(
    "MISO MARINADE", MAIN,
    """
    Miso Paste|1000|g;
    Sugar|600|g;
    Water|400|g;
    Mirin|200|g;
    Soy|150|g
    """,
    "Whisk all ingredients together until dissolved."
)

add(
    "MISO SOUP", MAIN,
    """
    Roasted Salmon|?|pc;
    Miso Paste|100|g;
    Water|4|L
    """,
    """
    Roast Salmon at 211°F for 2 minutes. .~
    Mix together mirin and sesame oil.~
    In a separate bowl, mix salt and sugar.~
    Rub pork belly with mirin and sesame oil first.~
    Generously rub with salt and sugar mixture.~
    Boil for 8 hours.
    """,
    "Confirm ingredients, amounts and preparation instructions with Leo."
)
add(
    "MUSHROOM BRAISE", MAIN,
    """
    Shiitake (Dried)|1|pc;
    Water (Soaking)|250|g;
    Shimeji|275|g;
    Soy|100|g;
    Sugar|20|g;
    Ginger|20|g;
    Kombu|10|g;
    Water (Cooking)|250|g
    """,
    """
    Soak shiitake in water overnight.~
    Combine everything in a pot and simmer mushrooms for 30 minutes with a cartouche.
    """
)

add(
    "PORK BELLY", MAIN,
    """
    Pork Belly|1|slab;
    Salt|600|g;
    Sugar|200|g;
    Mirin|200|g;
    Sesame Oil|100|g;
    Ginger (Sliced)|2|pc;
    Garlic (Whole)|2|pc
    """,
    """
    Trim excess fat from pork belly.~
    Mix mirin and sesame oil together.~
    Rub pork belly with mirin and sesame oil first.~
    In a separate bowl, mix salt and sugar.~
    Generously rub pork belly with salt and sugar mixture.~
    Depending on size, cut Pork Belly down to fit in vacuum bags.~
    Put each slab in a vacuum bag with ginger and garlic.~
    Vacuum seal.~
    Sous vide at 80°C for 8 hours or 75°C for 11 hours.
    """,
    "put 2 pcs ginger sliced and 2 garlic inside each vacuum bag."
)

add(
    "SUSHI RICE", MAIN,
    """
    Sekka Rice|1100|g;
    Water|1080|g;
    Sushi Su (Raw Rice Ratio)|220|g;
    Cooked Rice (Reference)|1600|g;
    Sushi Su (Cooked Rice Ratio)|320|g
    """,
    """
    Wash rice in a large strainer over a large bowl.~
    Discard starchy water regularly, with atleast 3 washes.~
    Completely drain before putting rice in the rice cooker.~
    Add water and cook.~
    Season sushi rice.
    """,
    "IMPORTANT: Original includes raw-rice and cooked-rice "
    "seasoning references. These are alternatives, not "
    "ingredients to add together."
)

add(
    "WHITE RICE", MAIN,
    """
    Sekka Rice|2740|g;
    Water (White Rice)|2740|g;
    Brown Rice (Alternative)|1000|g;
    Water (Brown Rice Alternative)|1300|g
    """,
    """
    Wash rice in a large strainer over a bowl.~
    Discard starchy water regularly, with at least 3 washes.~
    Completely drain before putting rice in the rice cooker.~
    Add water and cook.
    """,
    "Take Note of the different white-rice and brown-rice ratios."
)

add(
    "TOFU MARINADE", MAIN,
    """
    Miso Paste|300|g;
    Mirin|150|g;
    Black Pepper|3|g;
    Gochugaru|10|g;
    Tamari|30|g;
    Dashida / Mushroom Powder|10|g;
    Tofu|70|g;
    Marinate|30|g
    """,
    """
    Mix all ingredients together.~
    Marinate tofu for at least 1 hour before use.
    """,
    "REVIEW REQUIRED: The original lists 'Tofu 70g' and "
    "'Marinate 30g'. Confirm what these entries represent."
)

# ==========================================================
# SALADS + PICKLES
# ==========================================================

add(
    "BEAN SPROUTS", SALAD,
    """
    Raw Bean Sprouts|5000|g;
    Fish Sauce|198|g;
    Garlic (Blitzed)|110|g;
    Sesame Oil|132|g;
    Salt|80|g
    """,
    """
    Steam bean sprouts in Rational at 211°F for 2 minutes.~
    Strain bean sprouts and shock in ice water until cool.~
    In a separate bowl, mix fish sauce, garlic and sesame oil.~
    Add bean sprouts and mix thoroughly.~
    Check daily and adjust salt.
    """,
    "7L batch as the recorded base recipe."
)

add(
    "GARLIC CHIVES", SALAD,
    """
    Garlic Chives|1000|g;
    Tamari|100|g;
    Sugar|50|g;
    Gochujang Sauce|40|g;
    Rice Flour|30|g;
    Gochugaru|20|g
    """,
    """
    Cut chives into 2 inch pieces.~
    Combine all ingredients except chives into a paste.~
    Massage paste into chives.~
    Leave at room temperature or a warm spot for 2 hours to ferment.~
    Refrigerate; original says store up to two weeks.
    """
)

add(
    "KIMCHI COLESLAW", SALAD,
    """
    Green Cabbage|20000|g;
    Kimchi|10000|g;
    Sugar|2000|g;
    Lemon Juice|2000|g;
    Salt|600|g
    """,
    """
    Quarter cabbages and remove stems.~
    Use Robot Coupe to slice.~
    Gently massage cabbage with salt, sugar and lemon juice.~
    Let sit 15 minutes.~
    Squeeze all moisture out thoroughly.~
    Slice kimchi to a similar thickness as cabbage.~
    Mix sliced kimchi and cabbage together.
    """,
    "40L batch as the recorded base recipe."
)

add(
    "PICKLED DAIKON", SALAD,
    """
    Daikon|1000|g;
    Water|600|g;
    Rice Vinegar|400|g;
    Sugar|340|g;
    Salt|25|g
    """,
    """
    Peel and cut daikon into quarter-moon shapes.~
    Use Robot Coupe to slice.~
    Combine water, rice vinegar, sugar and salt.~
    Bring to a boil.~
    Pour boiling liquid over daikon until covered.~
    Cool before storing.
    """,
    "4X + 8X Recipes have been modified to be accurate amounts."
)

add(
    "PICKLED JALAPEÑO", SALAD,
    """
    Jalapeño|1800|g;
    Sugar|500|g;
    Tamari|500|g;
    Water|500|g;
    White Vinegar|500|g;
    Salt|20|g;
    Garlic Cloves|10|pcs
    """,
    """
    Wash, halve, clean and julienne jalapeño peppers.~
    Mix all other ingredients in a pot and bring to a boil.~
    Pour over julienned jalapeños and let sit for 24 hours.
    """,
    "Confirm preparation instructions with Leo."
)

add(
    "SESAME BROCCOLI", SALAD,
    """
    Broccoli|1250|g;
    Garlic (Blitzed)|30|g;
    Sesame Oil|20|g;
    Tamari|25|g;
    Salt|8|g
    """,
    """
    Cut broccoli into florets.~
    Steam broccoli in oven at 212°F for 3 minutes.~
    Cool in water bath.~
    Strain well and season broccoli.
    """,
    "1,250g = Approximately 4 heads of broccoli."
)

add(
    "WASABI CUCUMBER", SALAD,
    """
    Cucumber|1560|g;
    Sugar|187|g;
    White Vinegar|125|g;
    Salt|47|g;
    Wasabi Powder|8|g
    """,
    """
    Slice cucumbers using Robot Coupe.~
    Add sugar and salt, mix well, then let sit 20 minutes.~
    Drain liquid.~
    Whisk wasabi into vinegar until dissolved.~
    Pour over cucumbers and cure overnight.~
    Rotate cucumbers for the next 2 days as wasabi powder sinks.
    """
)

# ==========================================================
# APPLICATION STATE
# ==========================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "category" not in st.session_state:
    st.session_state.category = SAUCE

if "recipe" not in st.session_state:
    st.session_state.recipe = None

if "multiplier" not in st.session_state:
    st.session_state.multiplier = 1


def select_category(category):
    st.session_state.category = category
    st.session_state.recipe = None
    st.session_state.multiplier = 1


def select_recipe(recipe):
    st.session_state.recipe = recipe
    st.session_state.multiplier = 1


def select_multiplier(multiplier):
    st.session_state.multiplier = multiplier



# ==========================================================
# SPECIAL RECIPE MULTIPLIER EXCEPTIONS
# ==========================================================

SPECIAL_MULTIPLIERS = {
    "PICKLED DAIKON": {
        4: {
            "Daikon": 4078,
            "Water": 2447,
            "Rice Vinegar": 1631,
            "Sugar": 1387,
            "Salt": 102,
        },
        8: {
            "Daikon": 8157,
            "Water": 4894,
            "Rice Vinegar": 3263,
            "Sugar": 2773,
            "Salt": 204,
        },
    },
}


def format_amount(amount, unit, multiplier,
                  recipe_name=None, ingredient_name=None):

    # Check for an exact recipe-specific exception
    if recipe_name in SPECIAL_MULTIPLIERS:
        recipe_exceptions = SPECIAL_MULTIPLIERS[recipe_name]

        if multiplier in recipe_exceptions:
            special_amount = recipe_exceptions[multiplier].get(
                ingredient_name
            )

            if special_amount is not None:
                return f"{special_amount:,} {unit}"

    # Normal calculation for all other cases
    if amount == "?":
        return unit

    result = Decimal(amount) * Decimal(str(multiplier))

    if result == result.to_integral_value():
        number = f"{int(result):,}"
    else:
        number = f"{result:,.3f}".rstrip("0").rstrip(".")

    return f"{number} {unit}"



# ==========================================================
# MAIN CSS STYLING
# ==========================================================

st.markdown("""
<style>

/* GENERAL PAGE */

.stApp {
    background-color: #F7F7F7;
    color: #111111;
}

.block-container {
    max-width: 1500px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

#MainMenu, footer {
    visibility: hidden;
}

/* MEDIUM-BOLD FONTS */

.stApp, .stApp * {
    font-weight: 600;
}

/* RICE IS LIFE LOGO */

.brand-logo {
    text-align: center;
    font-family: Arial, Helvetica, sans-serif;
    font-size: clamp(42px, 5vw, 72px);
    font-weight: 800;
    letter-spacing: 0px;
    color: #ED2227;
    margin: 24px 0 28px 0;
}

/* GENERAL RED BUTTONS */

.stButton > button {
    width: 100%;
    min-height: 95px;
    padding: 12px 7px;

    background: linear-gradient(
        to bottom,
        #FFAAAA 0%,
        #FF5555 7%,
        #ED2227 16%,
        #ED2227 82%,
        #D7080D 100%
    );

    color: #FFFFFF !important;
    border: 6px solid #A4A4A4;
    border-radius: 7px;

    box-shadow:
        0 3px 1px rgba(0,0,0,0.16),
        inset 0 2px 2px rgba(255,255,255,0.45);

    font-family: Arial, Helvetica, sans-serif;
    font-size: clamp(15px, 2.1vw, 29px);
    font-weight: 600;
    line-height: 1.1;
    text-transform: uppercase;
    white-space: normal;
}

.stButton > button:hover,
.stButton > button:focus,
.stButton > button:active {
    color: #FFFFFF !important;
    background: #ED2227 !important;
}

/* CATEGORY BUTTONS */

div[class*="st-key-cat_"] button {
    min-height: 72px;
    height: 72px;
    font-size: clamp(18px, 2.5vw, 37px);
}

/* RECIPE SELECTION BUTTONS */

div[class*="st-key-recipe_"] button {
    min-height: 105px;
}

/* MULTIPLIER BUTTONS */

.st-key-multiplier_row [data-testid="stColumn"] {
    min-width: 0 !important;
    width: 0 !important;
    flex: 1 1 0 !important;
}

.st-key-multiplier_row .stButton {
    width: 100% !important;
    min-width: 0 !important;
}

.st-key-multiplier_row button {
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;

    height: 72px !important;
    min-height: 72px !important;
    max-height: 72px !important;

    padding: 2px !important;
    margin: 0 !important;

    border-width: 4px !important;
    font-size: 12px !important;
    line-height: 1.1 !important;
    box-sizing: border-box !important;
    text-align: center !important;
}

/* RECIPE TITLES */

.section-title {
    font-size: clamp(22px, 2.5vw, 32px);
    font-weight: 800;
    margin: 5px 0 20px 0;
    text-transform: uppercase;
}

.recipe-banner {
    background: #ED2227;
    border: 6px solid #AAAAAA;
    border-radius: 6px;
    text-align: center;
    padding: 17px 10px;
    color: #FFFFFF;
    font-size: clamp(24px, 3vw, 43px);
    font-weight: 800;
    margin-bottom: 22px;
}

/* INGREDIENTS */

.ingredient-row {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    border-bottom: 1px solid #DDDDDD;
    padding: 10px 0;
    font-size: clamp(16px, 1.9vw, 24px);
}

.ingredient-name {
    font-weight: 600;
    overflow-wrap: anywhere;
}

.ingredient-amount {
    font-weight: 700;
    text-align: right;
    white-space: nowrap;
}

/* PREPARATION STEPS */

.step-block {
    margin-bottom: 22px;
    font-size: clamp(17px, 1.9vw, 24px);
    line-height: 1.4;
}

.step-number {
    font-weight: 800;
    margin-bottom: 5px;
}

/* BATCH LABEL */

.batch-label {
    text-align: center;
    color: #555555;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 12px;
}

/* RECIPE NOTES */

.recipe-notes {
    background-color: #FFFFFF;
    border: 2px solid #ED2227;
    border-radius: 8px;
    color: #ED2227 !important;
    padding: 18px 20px;
    font-size: 18px;
    font-weight: 600;
    line-height: 1.5;
}

/* ==========================================
   STAFF LOGIN — RED AND WHITE
   ========================================== */

/* Outer login form */

[data-testid="stForm"] {
    background: #FFFFFF !important;
    border: 2px solid #ED2227 !important;
    border-radius: 8px !important;
}

/* Staff heading and instruction */

.login-heading {
    color: #ED2227;
    font-size: 28px;
    font-weight: 800;
}

.login-instruction {
    color: #ED2227;
    font-size: 18px;
    font-weight: 600;
}

/* Password field outer border */

[data-testid="stTextInput"] [data-baseweb="input"] {
    background: #FFFFFF !important;
    border: 2px solid #ED2227 !important;
    border-radius: 6px !important;
    box-shadow: none !important;
    overflow: hidden !important;
}

/* Streamlit BaseWeb outline */

[data-testid="stTextInput"] [data-baseweb="input"]:focus-within {
    border-color: #ED2227 !important;
    box-shadow: none !important;
}

/* Password entry area */

[data-testid="stTextInput"] input {
    background: #FFFFFF !important;
    color: #111111 !important;
    caret-color: #ED2227 !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    font-size: 20px !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: #777777 !important;
    opacity: 1 !important;
}

/* Password eye button */

[data-testid="stTextInput"] button,
[data-testid="stTextInput"] button:hover,
[data-testid="stTextInput"] button:focus,
[data-testid="stTextInput"] [data-testid="stPasswordVisibilityToggle"] {
    background: #ED2227 !important;
    background-color: #ED2227 !important;
    background-image: none !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    color: #FFFFFF !important;
}

/* Surrounding password eye area */

[data-testid="stTextInput"] [data-baseweb="input"] > div:last-child {
    background: #ED2227 !important;
    border: none !important;
}

/* White eye icon */

[data-testid="stTextInput"] button svg,
[data-testid="stTextInput"] button svg * {
    color: #FFFFFF !important;
    stroke: #FFFFFF !important;
}

/* LOGIN BUTTON */

[data-testid="stFormSubmitButton"] button,
[data-testid="stFormSubmitButton"] button:hover,
[data-testid="stFormSubmitButton"] button:focus,
[data-testid="stFormSubmitButton"] button:active {
    background: #FFFFFF !important;
    background-image: none !important;
    color: #ED2227 !important;
    border: 2px solid #ED2227 !important;
    border-radius: 6px !important;

    width: 120px !important;
    min-height: 44px !important;
    height: 44px !important;

    font-size: 18px !important;
    font-weight: 600 !important;
    text-transform: none !important;
    box-shadow: none !important;
}

[data-testid="stFormSubmitButton"] button p {
    color: #ED2227 !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    text-transform: none !important;
}

/* SMALLER SCREENS */

@media (max-width: 900px) {

    .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }

    div[class*="st-key-cat_"] button {
        min-height: 54px;
        height: 54px;
        font-size: 18px;
    }

    div[class*="st-key-recipe_"] button {
        min-height: 88px;
    }

    .st-key-multiplier_row button {
        height: 65px !important;
        min-height: 65px !important;
        max-height: 65px !important;
        font-size: 11px !important;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# ACTIVE BUTTON HIGHLIGHTING
# ==========================================================

def highlight_key(key):
    st.markdown(
        f"""
        <style>
        .st-key-{key} button {{
            border-color: #4AF000 !important;
            box-shadow:
                0 0 0 2px #4AF000,
                inset 0 2px 2px rgba(255,255,255,0.5)
                !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# PASSWORD PROTECTION
# ==========================================================

def login_screen():

    st.markdown(
        '<div class="brand-logo">riceislife</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="login-heading">STAFF</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="login-instruction">'
        'Enter the staff password to access recipes.'
        '</p>',
        unsafe_allow_html=True,
    )

    try:
        correct_password = str(
            st.secrets["STAFF_PASSWORD"]
        )
    except Exception:
        st.error(
            "Staff password has not been configured. "
            "Set STAFF_PASSWORD in Streamlit Secrets."
        )
        st.stop()

    with st.form("login_form"):

        entered = st.text_input(
            "Staff password",
            type="password",
            placeholder="Enter password",
        )

        submit = st.form_submit_button("Log In")

    if submit:

        if hmac.compare_digest(
            entered,
            correct_password
        ):
            st.session_state.authenticated = True
            st.rerun()

        else:
            st.error("Incorrect password.")

    st.stop()


if not st.session_state.authenticated:
    login_screen()


# ==========================================================
# LOGO
# ==========================================================

st.markdown(
    '<div class="brand-logo">riceislife</div>',
    unsafe_allow_html=True,
)


# ==========================================================
# CATEGORY NAVIGATION
# ==========================================================

category_columns = st.columns(3, gap="medium")

for index, category in enumerate(CATEGORIES):

    with category_columns[index]:

        st.button(
            category.upper(),
            key=f"cat_{index}",
            use_container_width=True,
            on_click=select_category,
            args=(category,),
        )

        if st.session_state.category == category:
            highlight_key(f"cat_{index}")


# ==========================================================
# RECIPE SELECTION PAGE
# ==========================================================

if st.session_state.recipe is None:

    category = st.session_state.category

    recipes = [
        name for name, data in RECIPES.items()
        if data["category"] == category
    ]

    # Four recipe buttons per row

    for start in range(0, len(recipes), 4):

        row = st.columns(4, gap="medium")

        for index, name in enumerate(
            recipes[start:start + 4]
        ):

            with row[index]:

                st.button(
                    name,
                    key=f"recipe_{start + index}",
                    use_container_width=True,
                    on_click=select_recipe,
                    args=(name,),
                )

        st.write("")

    st.stop()


# ==========================================================
# RECIPE DETAIL PAGE
# ==========================================================

recipe_name = st.session_state.recipe

if recipe_name not in RECIPES:
    st.session_state.recipe = None
    st.session_state.multiplier = 1
    st.rerun()

recipe = RECIPES[recipe_name]


# ==========================================================
# MULTIPLIER BUTTONS
# ==========================================================

st.markdown(
    '<div class="batch-label">'
    'SELECT BATCH MULTIPLIER'
    '</div>',
    unsafe_allow_html=True,
)

# 13 buttons in one row:
# 1X + twelve multiplier buttons

with st.container(key="multiplier_row"):

    multiplier_columns = st.columns(
        13,
        gap="small",
    )

    # 1X button

    with multiplier_columns[0]:

        st.button(
            "1X",
            key="reset_multiplier",
            use_container_width=True,
            on_click=select_multiplier,
            args=(1,),
        )

        if st.session_state.multiplier == 1:
            highlight_key("reset_multiplier")

    # Remaining multipliers

    for index, multiplier in enumerate(MULTIPLIERS):

        with multiplier_columns[index + 1]:

            st.button(
                f"{multiplier:g}X",
                key=f"mult_{index}",
                use_container_width=True,
                on_click=select_multiplier,
                args=(multiplier,),
            )

            if st.session_state.multiplier == multiplier:
                highlight_key(f"mult_{index}")


factor = st.session_state.multiplier

st.markdown(
    f"""
    <div class="batch-label" style="color: #0000FF !important;">
        CURRENT BATCH: {factor:g}X
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# INGREDIENTS + PREPARATION STEPS
# ==========================================================

left, right = st.columns([1, 1], gap="large")


# ==========================================================
# LEFT COLUMN — INGREDIENTS
# ==========================================================

with left:

    st.markdown(
        '<div class="section-title">'
        'RECIPE NAME:'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="recipe-banner">{escape(recipe_name)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### INGREDIENTS")


    for ingredient in recipe["ingredients"]:

        quantity = format_amount(
            ingredient["amount"],
            ingredient["unit"],
            factor,
            recipe_name=recipe_name,
            ingredient_name=ingredient["name"],
        )

        ingredient_name = escape(ingredient["name"])
        quantity_text = escape(quantity)

        st.markdown(
            f"""
            <div class="ingredient-row">
                <span class="ingredient-name">
                    {ingredient_name}
                </span>
                <span class="ingredient-amount">
                    {quantity_text}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )



# ==========================================================
# RIGHT COLUMN — PREPARATION STEPS
# ==========================================================

with right:

    st.markdown(
        '<div class="section-title">'
        'PREPARATION STEPS:'
        '</div>',
        unsafe_allow_html=True,
    )

    if recipe["steps"]:

        for index, step in enumerate(
            recipe["steps"], 1
        ):

            # Permit intentional bold tags in instructions.
            safe_step = escape(step)
            safe_step = safe_step.replace(
                "&lt;strong&gt;", "<strong>"
            ).replace(
                "&lt;/strong&gt;", "</strong>"
            )

            st.markdown(
                f"""
                <div class="step-block">
                    <div class="step-number">
                        STEP #{index}:
                    </div>
                    <div>{safe_step}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:
        st.warning(
            "Preparation steps have not been provided."
        )


# ==========================================================
# IMPORTANT RECIPE NOTES
# ==========================================================

if recipe["notes"]:

    st.divider()

    st.markdown(
        f"""
        <div class="recipe-notes">
            {escape(recipe["notes"])}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# LOG OUT
# ==========================================================

st.divider()

if st.button("LOG OUT", key="logout"):

    st.session_state.authenticated = False
    st.session_state.recipe = None
    st.session_state.multiplier = 1

    st.rerun()
