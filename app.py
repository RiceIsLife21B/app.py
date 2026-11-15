
import streamlit as st
import hmac
from decimal import Decimal
from html import escape

# ==========================================================
# RICE IS LIFE - STAFF RECIPE BOOK
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

SAUCE, MAIN, SALAD = CATEGORIES

CATEGORY_COLORS = {
    SAUCE: "#F27D34",
    MAIN: "#ED2227",
    SALAD: "#81C568",
}

BATCH_COLOR = "#00A7C5"
SELECTED_BORDER = "#D4AF37"

MULTIPLIERS = [
    1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 20, 30
]

RECIPES = {}


# ==========================================================
# RECIPE DATA HANDLING
# ==========================================================

def R(name, category, ingredients, steps, notes=""):
    parsed = []

    for entry in ingredients.split(";"):
        if not entry.strip():
            continue

        parts = [x.strip() for x in entry.split("|")]

        if len(parts) != 3:
            raise ValueError(
                f"Invalid ingredient in {name}: {entry}"
            )

        ingredient, amount, unit = parts

        parsed.append({
            "name": ingredient,
            "amount": amount,
            "unit": unit,
        })

    RECIPES[name] = {
        "category": category,
        "ingredients": parsed,
        "steps": [
            x.strip()
            for x in steps.split("~")
            if x.strip()
        ],
        "notes": notes,
    }


# ==========================================================
# SAUCES + DRESSINGS
# ==========================================================

R(
    "BULGOGI SAUCE(KBBQ)", SAUCE,
    "White Sugar|150|g;Mirin|150|g;House Soy Sauce|150|g;"
    "Water|100|g;Sesame Oil|30|g;Garlic|20|g;"
    "White Vinegar|15|g;Corn Starch|15|g;"
    "Ginger|10|g;Dashida|5|g;Black Pepper|3|g",
    "Grind garlic, ginger finely with mirin in Vitamix.~"
    "Mix together garlic, ginger and mirin with all other ingredients.~"
    "Bring to a boil, let cool."
)

R(
    "CHOJANG (PORK BELLY)", SAUCE,
    "Gochujang Paste|6300|g;White Sugar|3700|g;"
    "Rice Vinegar|3300|g;Brown Sugar|500|g;"
    "Kosher Salt|250|g;Hon Dashi|130|g",
    "Whisk sugars, salt and hon dashi into rice vinegar.~"
    "Whisk until hon dashi and sugars are dissolved.~"
    "Add Gochujang paste last."
)

R(
    "HOT MAYO MUSTARD", SAUCE,
    "Hellman's Mayo|800|g;Dijon Mustard|440|g;"
    "Lemon Juice|120|g;Mirin|100|g;"
    "Rice Vinegar|80|g;White Sugar|60|g",
    "Whisk all ingredients together until sugar is dissolved."
)

R(
    "HOT SAUCE", SAUCE,
    "Habanero Peppers|2000|g;Sherry Vinegar|1200|g;"
    "Water|700|g;Bell Peppers|500|g;"
    "White Sugar|100|g;Kosher Salt|100|g",
    "Cut habanero and bell peppers into pieces.~"
    "Grind all the peppers in Vitamix.~"
    "Whisk all ingredients together.",
    "Original notes: Green, Red and Orange habaneros; "
    "Red and Yellow bell peppers."
)

R(
    "HOUSE DRESSING", SAUCE,
    "White Vinegar|560|g;Carrots|540|g;"
    "Canola Oil|320|g;Onions|280|g;"
    "White Sugar|120|g;Ginger|68|g;Miso Paste|32|g;"
    "Kosher Salt|24|g;Sesame Oil|20|g;Black Pepper|4|g",
    "Peel carrots, onions and ginger.~"
    "Cut into small chunks.~"
    "Blend carrots, onions and ginger with vinegar "
    "in Vitamix until smooth.~"
    "Combine blended vegetables with remaining ingredients "
    "and whisk until smooth.",
    "IMPORTANT: Original specifies making two separate "
    "5X batches for 10X, NOT a 10X batch."
)

R(
    "HOUSE MAYO", SAUCE,
    "Hellman's Mayo|5000|g;Lemon Juice|500|g;"
    "Dashida/Mushroom Powder|100|g",
    "Mix dashida &/or? mushroom powder into lemon juice "
    "until dissolved.~Whisk mixture into mayo.",
    "Makes approximately 6L. Use a 15L container."
)

R(
    "KANG JEONG(KFC)", SAUCE,
    "Corn Syrup|2500|g;Ketchup|1500|g;"
    "Gochujang Paste|500|g;Minced Garlic|300|g;"
    "House Soy Sauce|200|g;MSG|10|g",
    "Mix all ingredients together."
)

R(
    "MISO GLAZE(SALMON)", SAUCE,
    "House Teriyaki Sauce|100|g;Miso Paste|15|g;"
    "Cornstarch Slurry|?|to taste",
    "Whisk together teriyaki and miso paste.~"
    "Gently heat until simmering. Do not let boil!\n"
    "    Make a cornstarch slurry with cold water.~"
    "Whisk in slurry slowly and simmer for one minute.",
    "Cornstarch slurry 10-15ml."
)

R(
    "SEASONED SOY(GF)", SAUCE,
    "House Soy Sauce|2000|g;Water|1000|g;Mirin|900|g;"
    "Sake|600|g;Kombu|50|g;Bonito|25|g",
    "Combine everything in a pot and bring to a boil.~"
    "Cool and infuse overnight, then strain.",
    "Original recipe makes approximately 5L."
)

R(
    "SPICY MAYO", SAUCE,
    "Mayo|400|g;Gochujang Paste|40|g;Sriracha|40|g;"
    "Lemon Juice|40|g;White Sugar|20|g;House Hot Sauce|27|g",
    "Dissolve sugar in lemon juice, "
    "then mix all ingredients together."
)

R(
    "SUSHI SU", SAUCE,
    "Mizkan Yamabuki Vinegar|4000|g;Aka Su|600|g;"
    "White Sugar|1750|g;Kosher Salt|600|g;Kombu|30|g",
    "Whisk all ingredients until sugar and salt"
    "dissolve."
)

R(
    "TENTSUYU(TOFU)", SAUCE,
    "Water|400|g;Dashida / Mushroom Powder|8|g;"
    "House Soy Sauce|200|g;Mirin|160|g;Sugar|20|g",
    "Whisk everything together until dissolved."
)

R(
    "TERIYAKI SAUCE(CHICKEN)", SAUCE,
    "House Soy Sauce|4000|g;White Sugar|3000|g;"
    "Mirin|4000|g;Sake|4000|g;"
    "Garlic(Crushed)|300|g;Ginger(Crushed)|100|g;"
    "Water|130|g;Cornstarch|130|g",
    "Combine house soy sauce, sugar, garlic and ginger.~"
    "Simmer for 30 minutes until flavors are infused.~"
    "Remove garlic and ginger.~"
    "Reduce by 1/4 or until desired consistency.~"
    "Make a cornstarch slurry.~"
    "Whisk in slurry slowly and simmer for 1 minute.~"
    "Cool down.",
    "Original recipe makes approximately 12L."
)

R(
    "YUZU GARLIC SAUCE(OH-MY)", SAUCE,
    "Garlic|1100|g;Wjite Sugar|1000|g;Lemon Juice|825|g;"
    "Honey|500|g;Corn Syrup|500|g;Canola Oil|500|g;"
    "Yuzu|300|g;Yuzu Kosho|160|g;Water|100|g;"
    "Corn Starch|50|g;Chili Pepper Flakes|25|g",
    "Confit garlic in canola oil until soft and golden.~"
    "Blend confit garlic and oil until smooth.~"
    "Combine all ingredients and bring to a boil.~"
    "Make a cornstarch slurry.~"
    "Whisk slurry in slowly and continue boiling for 1 minute."
)


# ==========================================================
# MAINS + MARINADES
# ==========================================================

R(
    "BEEF BRISKET", MAIN,
    "Kosher Salt|600|g;Black Pepper|400|g;"
    "Smoking Wood Chips|150|g:",
    "Mix salt and pepper.~"
    "Season brisket generously.~"
    "Cold smoke using the Rational for 2 hours.~"
    "Brisket can be smoked in advance.~"
    "Roast in combination setting at 100% humidity, "
    "202°F for 15 hours."
)

R(
    "CHICKEN BATTER", MAIN,
    "All Purpose Flour|205|g;House Soy Sauce|10|g;"
    "Kosher Salt|3|g;Can of Club Soda|355|ml",
    "Whisk all ingredients together until no lumps remain."
)

R(
    "CHICKEN BRINE", MAIN,
    "Water|2000|g;House Soy Sauce|100|g;Kosher Salt|50|g;"
    "White Sugar|20|g;Garlic(Crushed)|15|g;"
    "Ginger(Crushed)|15|g",
    "Whisk all ingredients together until sugar dissolved.~"
    "Brine chicken for 24 hours."
)

R(
    "DASHI EGG MARINADE", MAIN,
    "Water|2000|g;House Soy Sauce|300|g;"
    "White Sugar|100|g;Mirin|100|g;Kosher Salt|25|g;"
    "Hon Dashi|24|g;Eggs|60|eggs",
    "Put 1 layer of eggs on a perforated hotel pan.~"
    "Preheat Combi oven to steam at 212°F for 8 minutes.~"
    "Immediately shock eggs in cold running water "
    "until cool, then peel.~"
    "Combine marinade ingredients, bring to a boil and let cool.~"
    "Place cooled peeled eggs into cold marinade "
    "and leave overnight.",
    "Use 5.7L Cambro for the base batch."
)

R(
    "GARLIC SHRIMP", MAIN,
    "Green Onion Whites|200|g;Canola Oil|150|g;"
    "Garlic|100|g;White Vinegar|20|g;"
    "Ginger|20|g;Black Pepper|2|g;Kosher Salt|5|g",
    "slice the green onion whites, garlic and ginger.~"
    "Mix all ingredients together."
)

R(
    "JAPANESE CURRY", MAIN,
    "Onions|600|g;Carrots|450|g;Potatoes|300|g;"
    "Kosher Salt|10|g;Dashida / Mushroom Powder|10|g;"
    "Sesame Oil|?|to taste????;Dashi|1.5|L",
    "",
    "Salt to taste 10-15g Max. Dashi 1.5-2L to taste."
)

R(
    "MISO MARINADE", MAIN,
    "Miso Paste|1000|g;White Sugar|600|g;Water|400|g;"
    "Mirin|200|g;House Soy Sauce|150|g",
    "Whisk all ingredients together until dissolved."
)

R(
    "MISO SOUP", MAIN,
    "Roasted Salmon Head|1|pc;"
    "Aka Miso Paste|100|g;"
    "Water|4|L;"
    "Dashi|1.5|L;"
    "Kosher Salt|2|g",
    "Roast Salmon at 211°F for 2 minutes. .~"
    "ms.~ms.~ms.~ms.~Boil for XXX hours.",
    "Confirm ingredients, amounts and preparation "
    "instructions with Leo."
)

R(
    "MUSHROOM BRAISE", MAIN,
    "Dried Shiitake Mushrooms|1|pc;Water (Soaking)|250|g;"
    "Shimeji Mushrooms|275|g;House Soy Sauce|100|g;White Sugar|20|g;"
    "Ginger|20|g;Kombu|10|g;Water (Cooking)|250|g",
    "Soak shiitake in water overnight.~"
    "Combine everything in a pot and simmer mushrooms "
    "for 30 minutes with a cartouche."
)

R(
    "PORK BELLY", MAIN,
    "Pork Belly|1|slab;Kosher Salt|125|g;White Sugar|50|g;"
    "Mirin|200|g;Sesame Oil|100|g;"
    "Ginger (Sliced)|2|pc;Garlic (Whole)|2|pc",
    "Trim excess fat from pork belly.~"
    "Mix mirin and sesame oil together.~"
    "Rub pork belly with mirin and sesame oil first.~"
    "In a separate bowl, mix salt and sugar.~"
    "Generously rub pork belly with salt and sugar mixture.~"
    "Cut Pork Belly down to fit inside vacuum bags.~"
    "Put each slab in a vacuum bag with ginger and garlic.~"
    "Vacuum seal.~"
    "Sous vide at 80°C for 8 hours or 75°C for 11 hours.",
    "put 2 pcs ginger sliced and 2 garlic inside each vacuum bag."
)

R(
    "SUSHI RICE", MAIN,
    "Sekka Rice|1100|g;Water|1080|g;"
    "Sushi Su (Raw Rice Ratio)|220|g;"
    "Cooked Rice (Reference)|1600|g;"
    "Sushi Su (Cooked Rice Ratio)|320|g",
    "Wash rice in a large strainer over a large bowl.~"
    "Discard starchy water regularly, with atleast 3 washes.~"
    "Completely drain before putting rice in the rice cooker.~"
    "Add water and cook.~Season sushi rice.",
    "IMPORTANT: Original includes raw-rice and cooked-rice "
    "seasoning references. These are alternatives, "
    "not ingredients to add together."
)

R(
    "WHITE RICE", MAIN,
    "Sekka Rice|2740|g;Water (White Rice)|2740|g;"
    "Brown Rice (Alternative)|1000|g;"
    "Water (Brown Rice Alternative)|1300|g",
    "Wash rice in a large strainer over a bowl.~"
    "Discard starchy water regularly, with at least 3 washes.~"
    "Completely drain before putting rice in the rice cooker.~"
    "Add water and cook.",
    "Take Note of the different white-rice and brown-rice ratios."
)

R(
    "TOFU MARINADE", MAIN,
    "Miso Paste|300|g;"
    "Mirin|150|g;"
    "Black Pepper|3|g;"
    "Gochugaru|10|g;"
    "House Soy Sauce|30|g;"
    "Dashida / Mushroom Powder|10|g",
    "Mix all ingredients together.~"
    "Brush all 6 sides of cut tofu."
)


# ==========================================================
# SALADS + PICKLES
# ==========================================================

R(
    "BEAN SPROUTS", SALAD,
    "Raw Bean Sprouts|5000|g;Fish Sauce|198|g;"
    "Garlic (Blitzed)|110|g;Sesame Oil|132|g;Salt|80|g",
    "Steam bean sprouts in Rational at 211°F for 2 minutes.~"
    "Strain bean sprouts and shock in ice water until cool.~"
    "In a separate bowl, mix fish sauce, garlic and sesame oil.~"
    "Add bean sprouts and mix thoroughly.~"
    "Check daily and adjust salt.",
    "7L batch as the recorded base recipe."
)

R(
    "GARLIC CHIVES", SALAD,
    "Garlic Chives|1000|g;House Soy Sauce|100|g;White Sugar|50|g;"
    "Gochujang Paste|40|g;Rice Flour|30|g;Gochugaru|20|g",
    "Cut chives into 2 inch pieces.~"
    "Combine all ingredients except chives into a paste.~"
    "Massage paste into chives.~"
    "Leave at room temperature or a warm spot "
    "for 2 hours to ferment.~"
    "Refrigerate; original says store up to two weeks."
)

R(
    "KIMCHI COLESLAW", SALAD,
    "Green Cabbage|20000|g;Kimchi|10000|g;"
    "White Sugar|2000|g;Lemon Juice|2000|g;Kosher Salt|600|g",
    "Quarter cabbages and remove stems.~"
    "Use Robot Coupe to slice.~"
    "Gently massage cabbage with salt, sugar and lemon juice.~"
    "Let sit 15 minutes.~"
    "Squeeze all moisture out thoroughly.~"
    "Slice kimchi to a similar thickness as cabbage.~"
    "Mix sliced kimchi and cabbage together.",
    "40L batch as the recorded base recipe."
)

R(
    "PICKLED DAIKON", SALAD,
    "Daikon|1000|g;Water|600|g;Rice Vinegar|400|g;"
    "White Sugar|340|g;Kosher Salt|25|g",
    "Peel and cut daikon into quarter-moon shapes.~"
    "Use Robot Coupe to slice.~"
    "Combine water, rice vinegar, sugar and salt.~"
    "Bring to a boil.~"
    "Pour boiling liquid over daikon until covered.~"
    "Cool before storing.",
    "4X + 8X Recipes have been modified to be accurate amounts."
)

R(
    "PICKLED JALAPEÑO", SALAD,
    "Jalapeño|1800|g;White Sugar|500|g;House Soy Sauce|500|g;"
    "Water|500|g;White Vinegar|500|g;"
    "Kosher Salt|20|g;Garlic Cloves|10|pcs",
    "Wash, halve, clean and julienne jalapeño peppers.~"
    "Mix all other ingredients in a pot and bring to a boil.~"
    "Pour over julienned jalapeños and let sit for 24 hours.",
    "Confirm preparation instructions with Leo."
)

R(
    "SESAME BROCCOLI", SALAD,
    "Broccoli|1250|g;Garlic (Blitzed)|30|g;"
    "Sesame Oil|20|g;House Soy Sauce|25|g;Kosher Salt|8|g",
    "Cut broccoli into florets.~"
    "Steam broccoli in oven at 212°F for 3 minutes.~"
    "Cool in water bath.~"
    "Strain well and season broccoli.",
    "1,250g = Approximately 4 heads of broccoli."
)

R(
    "WASABI CUCUMBER", SALAD,
    "Cucumber|1560|g;White Sugar|187|g;"
    "White Vinegar|125|g;Kosher Salt|47|g;Wasabi Powder|8|g",
    "Slice cucumbers 1/8th thickness using Robot Coupe or mandolin.~"
    "Add sugar and salt, mix well, then let sit 20 minutes.~"
    "Drain liquid.~"
    "Whisk wasabi into vinegar until dissolved.~"
    "Pour over cucumbers and cure overnight.~"
    "Rotate cucumbers for the next 2 days "
    "as wasabi powder sinks."
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
# PICKLED DAIKON SPECIAL MULTIPLIERS
# ==========================================================

SPECIAL_MULTIPLIERS = {
    "PICKLED DAIKON": {
        4: {
            "Daikon": 4078,
            "Water": 2447,
            "Rice Vinegar": 1631,
            "White Sugar": 1387,
            "Kosher Salt": 102,
        },
        8: {
            "Daikon": 8157,
            "Water": 4894,
            "Rice Vinegar": 3263,
            "White Sugar": 2773,
            "Kosher Salt": 204,
        },
    },
}


def format_amount(
    amount,
    unit,
    multiplier,
    recipe_name=None,
    ingredient_name=None,
):
    recipe_exceptions = SPECIAL_MULTIPLIERS.get(
        recipe_name, {}
    )

    special_amounts = recipe_exceptions.get(
        multiplier, {}
    )

    if ingredient_name in special_amounts:
        return f"{special_amounts[ingredient_name]:,} {unit}"

    if amount == "?":
        return unit

    result = Decimal(amount) * Decimal(str(multiplier))

    if result == result.to_integral_value():
        number = f"{int(result):,}"
    else:
        number = f"{result:,.3f}".rstrip("0").rstrip(".")

    return f"{number} {unit}"


# ==========================================================
# STYLING - IPAD LAYOUT
# ==========================================================

st.markdown("""
<style>

:root {
    --brand-red: #ED2227;
    --batch-blue: #00A7C5;
    --selected-gold: #D4AF37;
}

/* GENERAL PAGE */

.stApp {
    background: #F7F7F7;
    color: #111111;
}

.block-container {
    max-width: 1500px;

    /* Entire page moved downward 35 pixels */
    padding-top: calc(0.4rem + 35px) !important;

    padding-bottom: 2rem;
}

#MainMenu, footer {
    visibility: hidden;
}

.stApp, .stApp * {
    font-weight: 600;
}

/* LOGO */

.brand-logo {
    text-align: center;
    font-family: Arial, Helvetica, sans-serif;
    font-size: clamp(38px, 4.8vw, 66px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: 0;
    color: #ED2227;
    margin: 8px 0 4px;
}

/* TOP NAVIGATION SPACING */

.st-key-top_navigation [data-testid="stVerticalBlock"] {
    gap: 0.45rem;
}

.st-key-top_navigation [data-testid="stHorizontalBlock"] {
    margin-top: 0;
}

/* GENERAL BUTTONS */

.stButton > button {
    --button-color: #ED2227;

    width: 100%;
    min-height: 95px;
    padding: 10px 6px;

    background: var(--button-color) !important;
    color: #FFFFFF !important;

    border: 5px solid #A4A4A4;
    border-radius: 7px;

    box-shadow:
        0 3px 1px rgba(0,0,0,0.16),
        inset 0 2px 2px rgba(255,255,255,0.22);

    font-family: Arial, Helvetica, sans-serif;
    font-size: clamp(15px, 2.1vw, 29px);
    font-weight: 600;
    line-height: 1.12;
    text-transform: uppercase;
    white-space: normal;
}

/* BUTTON HOVER */

.stButton > button:hover,
.stButton > button:focus,
.stButton > button:active {
    background: var(--button-color) !important;
    color: #FFFFFF !important;
    filter: brightness(0.96);
}

/* CATEGORY COLORS */

.st-key-cat_0 button {
    --button-color: #F27D34;
}

.st-key-cat_1 button {
    --button-color: #ED2227;
}

.st-key-cat_2 button {
    --button-color: #81C568;
}

.st-key-cat_0 button,
.st-key-cat_1 button,
.st-key-cat_2 button {
    min-height: 72px;
    height: 72px;
    font-size: clamp(16px, 2.2vw, 29px);
}

/* RECIPE SELECTION BUTTONS */

div[class*="st-key-recipe_"] button {
    min-height: 94px;
}

/* SAUCES */

.st-key-recipe_grid_sauce
div[class*="st-key-recipe_"] button {
    --button-color: #F27D34;
}

/* MAINS */

.st-key-recipe_grid_main
div[class*="st-key-recipe_"] button {
    --button-color: #ED2227;
}

/* SALADS */

.st-key-recipe_grid_salad
div[class*="st-key-recipe_"] button {
    --button-color: #81C568;
}

/* RECIPE PAGE VERTICAL SPACING */

.st-key-recipe_detail [data-testid="stVerticalBlock"] {
    gap: 0.45rem;
}

/* MULTIPLIER ROW */

.st-key-multiplier_row [data-testid="stHorizontalBlock"] {
    gap: 0.22rem !important;
}

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
    --button-color: #00A7C5;

    background: #00A7C5 !important;
    color: #FFFFFF !important;

    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;

    height: 64px !important;
    min-height: 64px !important;
    max-height: 64px !important;

    padding: 1px !important;
    margin: 0 !important;

    border-width: 3px !important;

    box-sizing: border-box !important;
    text-align: center !important;

    font-size: clamp(9px, 0.95vw, 12px) !important;
    white-space: nowrap !important;
}

/* HEADING ROW */

.st-key-recipe_heading [data-testid="stHorizontalBlock"] {
    align-items: center;
}

/* RECIPE TITLE */

.recipe-banner {
    background: var(
        --recipe-title-color,
        #ED2227
    ) !important;

    color: #FFFFFF;

    border: 4px solid #AAAAAA;
    border-radius: 6px;

    text-align: center;
    padding: 9px 10px;

    font-size: clamp(17px, 2.1vw, 27px);
    font-weight: 700;
    line-height: 1.18;

    overflow-wrap: anywhere;
    margin: 0;
}

/* CURRENT BATCH */

.current-batch {
    color: #00A7C5;
    text-align: center;

    font-size: clamp(18px, 2vw, 25px);
    font-weight: 700;
    line-height: 1.2;

    margin: 0;
}

/* SECTION HEADINGS */

.section-title {
    font-size: clamp(21px, 2.4vw, 30px);
    font-weight: 600;

    margin: 0 0 6px;
    text-transform: uppercase;
}

/* INGREDIENT ROWS */

.ingredient-row {
    display: flex;
    justify-content: space-between;
    align-items: center;

    gap: 12px;
    border-bottom: 1px solid #DDDDDD;

    padding: 5px 0;

    font-size: clamp(16px, 1.85vw, 23px);
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
    margin-bottom: 15px;
    font-size: clamp(17px, 1.9vw, 23px);
    line-height: 1.4;
}

.step-number {
    font-weight: 800;
    margin-bottom: 3px;
}

/* RECIPE NOTES */

.recipe-notes {
    background: #FFFFFF;
    border: 2px solid #ED2227;
    border-radius: 8px;

    color: #ED2227;

    padding: 14px 18px;
    font-size: 18px;
    font-weight: 600;
}

/* LOGIN FORM */

[data-testid="stForm"] {
    background: #FFFFFF !important;
    border: 2px solid #ED2227 !important;
    border-radius: 8px !important;
}

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

/* PASSWORD INPUT */

[data-testid="stTextInput"] [data-baseweb="input"] {
    background: #FFFFFF !important;
    border: 2px solid #ED2227 !important;
    border-radius: 6px !important;
    box-shadow: none !important;
    overflow: hidden !important;
}

[data-testid="stTextInput"]
[data-baseweb="input"]:focus-within {
    border-color: #ED2227 !important;
    box-shadow: none !important;
}

[data-testid="stTextInput"] input {
    background: #FFFFFF !important;
    color: #111111 !important;
    caret-color: #ED2227 !important;

    border: 0 !important;
    outline: 0 !important;
    box-shadow: none !important;

    font-size: 20px !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: #777777 !important;
    opacity: 1 !important;
}

/* PASSWORD EYE CONTROL */

[data-testid="stTextInput"] button,
[data-testid="stTextInput"] button:hover,
[data-testid="stTextInput"] button:focus,
[data-testid="stTextInput"]
[data-testid="stPasswordVisibilityToggle"],
[data-testid="stTextInput"]
[data-baseweb="input"] > div:last-child {
    background: #ED2227 !important;
    background-image: none !important;

    color: #FFFFFF !important;

    border: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

[data-testid="stTextInput"] button svg,
[data-testid="stTextInput"] button svg * {
    color: #FFFFFF !important;
    stroke: #FFFFFF !important;
}

/* LOG IN BUTTON */

[data-testid="stFormSubmitButton"] button,
[data-testid="stFormSubmitButton"] button:hover,
[data-testid="stFormSubmitButton"] button:focus {
    background: #FFFFFF !important;
    color: #ED2227 !important;

    border: 2px solid #ED2227 !important;
    border-radius: 6px !important;

    width: 120px !important;
    height: 44px !important;
    min-height: 44px !important;

    font-size: 18px !important;
    text-transform: none !important;
    box-shadow: none !important;
}

[data-testid="stFormSubmitButton"] button p {
    color: #ED2227 !important;
    text-transform: none !important;
}

/* IPAD PORTRAIT / SMALLER SCREENS */

@media (max-width: 900px) {

    .block-container {
        padding-left: 10px;
        padding-right: 10px;
    }

    .brand-logo {
        margin: 5px 0 2px;
    }

    .st-key-cat_0 button,
    .st-key-cat_1 button,
    .st-key-cat_2 button {
        height: 54px;
        min-height: 54px;

        font-size: clamp(12px, 1.7vw, 18px);
    }

    div[class*="st-key-recipe_"] button {
        min-height: 85px;
    }

    .st-key-multiplier_row
    [data-testid="stHorizontalBlock"] {
        gap: 0.16rem !important;
    }

    .st-key-multiplier_row button {
        height: 57px !important;
        min-height: 57px !important;
        max-height: 57px !important;

        padding: 0 !important;
        border-width: 2px !important;

        font-size: 10px !important;
    }

    .recipe-banner {
        font-size: clamp(15px, 2.15vw, 22px);
        padding: 7px 5px;
    }

    .current-batch {
        font-size: clamp(15px, 2.2vw, 21px);
    }

    .ingredient-row {
        padding: 4px 0;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# ACTIVE BUTTON HIGHLIGHTING - GOLD
# ==========================================================

def highlight_key(key):
    st.markdown(
        f"""
        <style>
        .st-key-{key} button {{
            border-color: #D4AF37 !important;

            box-shadow:
                0 0 0 2px #D4AF37,
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
# TOP HEADER AND CATEGORY NAVIGATION
# ==========================================================

with st.container(key="top_navigation"):

    st.markdown(
        '<div class="brand-logo">riceislife</div>',
        unsafe_allow_html=True,
    )

    category_columns = st.columns(
        3,
        gap="medium",
    )

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
        name
        for name, data in RECIPES.items()
        if data["category"] == category
    ]

    grid_key = {
        SAUCE: "recipe_grid_sauce",
        MAIN: "recipe_grid_main",
        SALAD: "recipe_grid_salad",
    }[category]

    with st.container(key=grid_key):

        for start in range(0, len(recipes), 4):

            row = st.columns(
                4,
                gap="medium",
            )

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

recipe_title_color = CATEGORY_COLORS[
    recipe["category"]
]


with st.container(key="recipe_detail"):

    # ======================================================
    # MULTIPLIER BUTTONS
    # ======================================================

    with st.container(key="multiplier_row"):

        multiplier_columns = st.columns(
            14,
            gap="small",
        )

        # 1X BUTTON

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

        # REMAINING MULTIPLIERS

        for index, multiplier in enumerate(
            MULTIPLIERS
        ):

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

    # ======================================================
    # HEADING ROW
    # CURRENT BATCH LEFT / RECIPE TITLE RIGHT
    # ======================================================

    with st.container(key="recipe_heading"):

        head_left, head_right = st.columns(
            [1, 1],
            gap="large",
        )

        with head_left:

            st.markdown(
                f"""
                <div class="current-batch">
                    CURRENT BATCH: {factor:g}X
                </div>
                """,
                unsafe_allow_html=True,
            )

        with head_right:

            st.markdown(
                f'<div class="recipe-banner" '
                f'style="--recipe-title-color:{recipe_title_color};">'
                f'{escape(recipe_name)}</div>',
                unsafe_allow_html=True,
            )

    # ======================================================
    # TWO-COLUMN RECIPE LAYOUT
    # LEFT = PREPARATION
    # RIGHT = INGREDIENTS
    # ======================================================

    left, right = st.columns(
        [1, 1],
        gap="large",
    )

    # ======================================================
    # LEFT COLUMN - PREPARATION STEPS
    # ======================================================

    with left:

        st.markdown(
            '<div class="section-title">'
            'PREPARATION STEPS:'
            '</div>',
            unsafe_allow_html=True,
        )

        if recipe["steps"]:

            for index, step in enumerate(
                recipe["steps"],
                1
            ):

                safe_step = escape(step)

                safe_step = safe_step.replace(
                    "&lt;strong&gt;",
                    "<strong>"
                ).replace(
                    "&lt;/strong&gt;",
                    "</strong>"
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

    # ======================================================
    # RIGHT COLUMN - INGREDIENTS
    # ======================================================

    with right:

        st.markdown(
            '<div class="section-title">'
            'INGREDIENTS'
            '</div>',
            unsafe_allow_html=True,
        )


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

            ingredient_html = (
                '<div class="ingredient-row">'
                f'<span class="ingredient-name">{ingredient_name}</span>'
                f'<span class="ingredient-amount">{quantity_text}</span>'
                '</div>'
            )

            st.markdown(
                ingredient_html,
                unsafe_allow_html=True,
            )


    # ======================================================
    # RECIPE NOTES
    # ======================================================

    if recipe["notes"]:

        st.markdown(
            f"""
            <div class="recipe-notes">
                {escape(recipe["notes"])}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==========================================================
# LOG OUT - BOTTOM RIGHT
# ==========================================================

st.divider()

logout_left, logout_right = st.columns(
    [5, 1],
    gap="small",
)

with logout_right:

    if st.button(
        "LOG OUT",
        key="logout",
        use_container_width=True,
    ):

        st.session_state.authenticated = False
        st.session_state.recipe = None
        st.session_state.multiplier = 1

        st.rerun()
