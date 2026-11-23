
import streamlit as st
import hmac
from decimal import Decimal, InvalidOperation
from html import escape

# ==========================================================
# RICE IS LIFE - STAFF RECIPE BOOK
# ==========================================================

st.set_page_config(
    page_title="Rice Is Life | Staff Recipes",
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
    SAUCE: "#C46B2B",
    MAIN: "#D83A40",
    SALAD: "#4E8562",
}

MULTIPLIERS = [
    1, 1.5, 2, 3, 4, 5, 6, 7, 8,
    9, 10, 13, 20, 30
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

        parts = [
            p.strip()
            for p in entry.split("|")
        ]

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
            s.strip()
            for s in steps.split("~")
            if s.strip()
        ],
        "notes": [
            n.strip()
            for n in notes.split("~")
            if n.strip()
        ],
    }


# ==========================================================
# SAUCES + DRESSINGS
# ==========================================================

R(
    "BULGOGI SAUCE(KBBQ)", SAUCE,
    "White Sugar|150|g;Mirin|150|g;"
    "House Soy Sauce|150|g;Water|20|g;"
    "Sesame Oil|30|g;Garlic|20|g;"
    "White Vinegar|15|g;Corn Starch|20|g;"
    "Ginger|10|g;Dashida|5|g;Black Pepper|3|g",
    "Grind garlic, ginger finely with mirin in Vitamix.~"
    "Mix together garlic, ginger and mirin with all other ingredients.~"
    "Bring to a boil, add the mix of corn starch and water.~"
    "Simmer 1-2 minutes and let cool.",
    "20x: fits in 12L cambro"
)

R(
    "CHOJANG (PORK BELLY)", SAUCE,
    "Gochujang Paste|6300|g;White Sugar|3700|g;"
    "Rice Vinegar|3300|g;Brown Sugar|500|g;"
    "Kosher Salt|250|g;Hon Dashi|130|g",
    "Whisk sugars, salt and hon dashi into rice vinegar.~"
    "Whisk at low heat until hon dashi and sugars are dissolved.~"
    "Add Gochujang paste last.",
    "Final product: every 500g add 20g of brown sugar.~"
    "1x: fits 22L cambro"
)

R(
    "HOT MAYO MUSTARD", SAUCE,
    "House Mayo|800|g;Dijon Mustard|440|g;"
    "Lemon Juice|120|g;Mirin|100|g;"
    "Rice Vinegar|80|g;White Sugar|60|g",
    "Whisk all ingredients together until sugar is dissolved."
)

R(
    "HOT SAUCE", SAUCE,
    "Habanero Peppers|2000|g;Sherry Vinegar|1200|g;"
    "Water|700|g;Bell Peppers|500|g;"
    "White Sugar|100|g;Kosher Salt|100|g;"
    "Canola Oil|100|g",
    "Cut bell peppers in half, Rinse with all peppers in water.~"
    "Mix in canola oil~"
    "Roast whole habanero and bell peppers at 500°F until blister (7-10 min max).~"
    "Grind all the peppers in Vitamix.~"
    "Whisk all ingredients together.~"
    "Wrap bowl with saran wrap and let ferment at room temerature for 48-72 hours.",
    "Green, Red and Orange habaneros and Red and Yellow bell peppers preferred.~"
    "After roasting, turn and repeat if neccessary"
)

R(
    "HOUSE DRESSING", SAUCE,
    "Rice Vinegar|600|g;Carrots|540|g;"
    "Canola Oil|320|g;Onions|280|g;"
    "White Sugar|120|g;Ginger|68|g;"
    "Miso Paste|32|g;Kosher Salt|24|g;"
    "Sesame Oil|20|g;Black Pepper|4|g",
    "Peel carrots, onions and ginger.~"
    "Cut into small chunks.~"
    "Blend carrots, onions and ginger with rice vinegar in Vitamix until smooth.~"
    "Combine blended vegetables with remaining ingredients and whisk until smooth.",
    "IMPORTANT: Original specifies making two separate 5X batches for 10X, NOT a 10X batch.~"
    "5X: fits in 12L cambro"
)

R(
    "HOUSE MAYO", SAUCE,
    "Hellman's Mayo|5000|g;Lemon Juice|500|g;"
    "Mushroom Powder|100|g",
    "Mix mushroom powder into lemon juice until dissolved.~"
    "Whisk mixture into mayo.",
    "3x: fits in 22L cambro"
)

R(
    "KANG JEONG(KFC)", SAUCE,
    "Corn Syrup|2500|g;Ketchup|1500|g;"
    "Gochujang Paste|500|g;Minced Garlic|300|g;"
    "MSG|10|g;House Soy Sauce|200|g;"
    "Mushroom Powder|10|g",
    "Mix all ingredients together.",
    "1x: fits in 5L cambro"
)

R(
    "MISO GLAZE(SALMON)", SAUCE,
    "House Teriyaki Sauce|100|g;Water|50|g;"
    "Corn Starch|50|g;Aka Miso Paste|15|g",
    "Whisk the miso paste into the teriyaki.~"
    "Make the cornstarch slurry with cold water.~"
    "Slowly whisk in slurry and simmer for one minute.",
    "Gently heat, do not let boil."
)

R(
    "SEASONED SOY(GF)", SAUCE,
    "House Soy Sauce|2000|g;Water|1000|g;"
    "Mirin|900|g;Sake|600|g;"
    "Kombu|50|g;Bonito|25|g",
    "Combine everything in a pot and bring to a boil.~"
    "Cool and infuse overnight, then strain.",
    "Original recipe makes approximately 5L.~"
    "5x: fits 22L cambro"
)

R(
    "SPICY MAYO", SAUCE,
    "House Mayo|400|g;Gochujang Paste|40|g;"
    "House Hot Sauce|40|g",
    "Mix all ingredients together."
)

R(
    "SUSHI SU", SAUCE,
    "Mizkan Yamabuki Vinegar|4000|g;"
    "White Sugar|1750|g;Aka Su|600|g;"
    "Kosher Salt|600|g;Kombu|30|g",
    "Whisk all ingredients at low temperasture until sugar and salt dissolve.",
    "Cool it down in ice bath. Do not let boil.~"
    "3x: fits 22L cambro"
)

R(
    "TENTSUYU(TOFU)", SAUCE,
    "Water|400|g;House Soy Sauce|200|g;"
    "Mirin|160|g;White Sugar|20|g;"
    "Mushroom Powder|8|g",
    "Whisk all ingredients until dissolved."
)

R(
    "TERIYAKI SAUCE(CHICKEN)", SAUCE,
    "House Soy Sauce|4000|g;Sake|4000|g;"
    "Mirin|4000|g;White Sugar|3000|g;"
    "Garlic(Crushed)|300|g;Water|130|g;"
    "Cornstarch|130|g;Ginger(Crushed)|100|g",
    "Combine house soy sauce, sugar, garlic and ginger.~"
    "Simmer for 30 minutes until flavors are infused.~"
    "Remove garlic and ginger.~"
    "Reduce by 25% or until desired consistency.~"
    "Make a cornstarch slurry.~"
    "Whisk in slurry slowly and simmer for 1 minute.~"
    "Cool down.",
    "Original recipe makes approximately 12L."
)

R(
    "YUZU GARLIC SAUCE(OH-MY)", SAUCE,
    "Garlic|1100|g;White Sugar|1000|g;"
    "Lemon Juice|825|g;Honey|500|g;"
    "Corn Syrup|500|g;Canola Oil|500|g;"
    "Yuzu|300|g;Yuzu Kosho|160|g;"
    "Water|50|g;Corn Starch|50|g;"
    "Chili Pepper Flakes|25|g",
    "Confit garlic in canola oil until soft and golden for 2 hours at low temperature.~"
    "Blend confit garlic and oil until smooth.~"
    "Combine all ingredients and bring to a boil.~"
    "Make a corn starch slurry.~"
    "Whisk slurry in slowly and continue boiling for 1-2 minutes."
)


# ==========================================================
# MAINS + MARINADES
# ==========================================================

R(
    "BEEF BRISKET", MAIN,
    "Kosher Salt|600|g;Black Pepper|400|g;"
    "Smoking Wood Chips|150|g",
    "Mix salt and pepper.~"
    "Season brisket generously.~"
    "Braise & Smoke function in the Rational for 90 minutes.~"
    "Set it for 215°F for 12-15 hours with 80% humidity.~"
    "Remove, put into hotel pan.~"
    "Collect the drippings and pour overtop of brisket.~"
    "Wrap in aluminum foil and leave out to cool for 5-6 hours before refrigeration."
)

R(
    "CHICKEN BATTER", MAIN,
    "All Purpose Flour|205|g;House Soy Sauce|10|g;"
    "Kosher Salt|3|g;Can of Club Soda|355|ml",
    "Whisk all ingredients together until no lumps remain."
)

R(
    "CHICKEN BRINE", MAIN,
    "Water|2000|g;House Soy Sauce|100|g;"
    "Kosher Salt|50|g;White Sugar|20|g;"
    "Garlic(Crushed)|15|g;Ginger(Crushed)|15|g",
    "Whisk all ingredients together until sugar dissolved.~"
    "Brine chicken for 24 hours."
)

R(
    "DASHI", MAIN,
    "Water|20|L;Roasted Salmon Head|1|pc;"
    "Daikon|1000|g;Mirin|190|g;"
    "Whole Green Onions|150|g;Kombu|70|g;"
    "Kosher Salt|50|g;Katsuo Bushi|40|g;"
    "Dried Shiitake Mushroom|30|g;Hon Dashi|4|g",
    "Roast Salmon Head at 460°C at 50% Humidity for 15-20 minutes.~"
    "Slice Daikon in 1 inch thickness.~"
    "Bring all ingredients to boil in pot.~"
    "Skim surface, and simmer for 40 minutes.~"
    "After simmering, strain while still hot.~"
    "Then cool in ice water bath."
)

R(
    "DASHI EGG MARINADE", MAIN,
    "Water|2000|g;House Soy Sauce|300|g;"
    "White Sugar|100|g;Mirin|100|g;"
    "Kosher Salt|25|g;Hon Dashi|24|g;"
    "Eggs|60|eggs",
    "Put 1 layer of eggs on a perforated hotel pan.~"
    "Preheat Combi oven to steam at 212°F for 8 minutes.~"
    "Immediately shock eggs in cold running water until cool, then peel.~"
    "Combine marinade ingredients, bring to a boil and let cool.~"
    "Place cooled peeled eggs into cold marinade and marinade for 48 hours.",
    "Use 5.7L Cambro for the base batch."
)

R(
    "GARLIC SHRIMP", MAIN,
    "Green Onion Whites|200|g;Canola Oil|150|g;"
    "Garlic|100|g;White Vinegar|20|g;"
    "Ginger|20|g;Kosher Salt|5|g;"
    "Black Pepper|2|g",
    "slice the green onion whites, garlic and ginger.~"
    "Mix all ingredients together."
)

R(
    "JAPANESE CURRY", MAIN,
    "Dashi|1.5|L;Curry Powder|??|g;"
    "Onions|600|g;Carrots|450|g;"
    "Potatoes|300|g;Kosher Salt|10|g;"
    "Mushroom Powder|10|g;Sesame Oil|5|ml to taste",
    "Dice potato and keep in cold water for service.~"
    "Dry them off prior to deep frying for 90 seconds.~"
    "Mix into curry and serve."
)

R(
    "MISO MARINADE", MAIN,
    "Miso Paste|1000|g;White Sugar|600|g;"
    "Water|400|g;Mirin|200|g;"
    "House Soy Sauce|150|g",
    "Whisk all ingredients together until dissolved."
)

R(
    "MISO SOUP", MAIN,
    "Dashi|4|L;Aka Miso Paste|200|g;"
    "Hon Dashi|4|g;Kosher Salt|1|g",
    "Mix dashi, hon dashi, miso paste and salt and bring to boil.",
    "Confirm ingredients, amounts and preparation with Leo"
)

R(
    "MUSHROOM BRAISE", MAIN,
    "Dried Shiitake Mushrooms|1|pc;"
    "Water (Soak overnight)|250|g;"
    "Shimeji Mushrooms|275|g;"
    "Water (Cooking)|250|g;"
    "House Soy Sauce|100|g;"
    "Water (Cooking)|250|g;"
    "White Sugar|20|g;Ginger|20|g;Kombu|10|g",
    "Soak shiitake mushroom in water overnight.~"
    "Combine everything in a pot and simmer mushrooms for 30 minutes with a cartouche."
)

R(
    "PORK BELLY", MAIN,
    "Pork Belly|1|slab;Mirin|200|g;"
    "Kosher Salt|125|g;Sesame Oil|100|g;"
    "White Sugar|50|g;Ginger (Sliced)|2|pc;"
    "Garlic (Whole)|2|pc",
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
    "Add water and cook.~"
    "Season sushi rice.",
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
    "Miso Paste|300|g;Mirin|150|g;"
    "House Soy Sauce|30|g;"
    "Dashida / Mushroom Powder|10|g;"
    "Gochugaru|10|g;Black Pepper|3|g",
    "Mix all ingredients together.~"
    "Brush all 6 sides of cut tofu with marinade."
)


# ==========================================================
# SALADS + PICKLES
# ==========================================================

R(
    "BEAN SPROUTS", SALAD,
    "Raw Bean Sprouts|3000|g;Fish Sauce|118.8|g;"
    "Sesame Oil|79.2|g;Garlic (Blitzed)|66|g;"
    "Salt|48|g",
    "Steam bean sprouts in Rational at 211°F for 2 minutes.~"
    "Strain bean sprouts and shock in ice water until cool.~"
    "Drain with a spinner.~"
    "In a separate bowl, mix fish sauce, garlic and sesame oil.~"
    "Add bean sprouts and mix thoroughly.~"
    "Check daily and adjust salt to taste.",
    "Batch sizes: 1X = 3 kg, 2X = 6 kg, 3X = 9 kg."
)

R(
    "GARLIC CHIVES", SALAD,
    "Garlic Chives|1000|g;"
    "House Soy Sauce|100|g;White Sugar|50|g;"
    "Gochujang Paste|40|g;Rice Flour|30|g;"
    "Gochugaru|20|g",
    "Cut chives into 2 inch pieces.~"
    "Combine all ingredients except chives into a paste.~"
    "Massage paste into chives.~"
    "Leave at room temperature or a warm spot for 2 hours to ferment.~"
    "Refrigerate; original says store up to two weeks."
)

R(
    "KIMCHI COLESLAW", SALAD,
    "Green Cabbage|20000|g;Kimchi|10000|g;"
    "White Sugar|2000|g;Lemon Juice|2000|g;"
    "Kosher Salt|600|g",
    "Quarter cabbages and remove stems.~"
    "Slice cabbage with Robot Coupe.~"
    "Lovingly massage cabbage with salt, sugar and lemon juice.~"
    "Let sit 45 minutes.~"
    "Squeeze all moisture out.~"
    "Slice kimchi to a similar thickness as cabbage.~"
    "Mix sliced kimchi and cabbage together.~"
    "Mix kimchi every 24 hours, mix bottom to top.~",
    "40L batch as the recorded base recipe."
)

R(
    "PICKLED DAIKON", SALAD,
    "Daikon|1000|g;Water|600|g;"
    "Rice Vinegar|400|g;White Sugar|340|g;"
    "Kosher Salt|25|g",
    "Peel and cut daikon into 1/8 inch quarter-moon shapes.~"
    "Use Robot Coupe to slice.~"
    "Combine water, rice vinegar, sugar and salt.~"
    "Bring to a boil.~"
    "Pour boiling liquid over daikon until covered.~"
    "Cool before storing.~"
    "Mix pickled daikon every 24 hours, mix bottom to top.",
    "4X + 8X Recipes have been modified to be accurate amounts."
)

R(
    "PICKLED JALAPEÑO", SALAD,
    "Jalapeño|1800|g;White Sugar|500|g;"
    "House Soy Sauce|500|g;Water|500|g;"
    "White Vinegar|500|g;Kosher Salt|20|g;"
    "Garlic Cloves|10|pcs",
    "Wash, halve, clean and julienne jalapeño peppers.~"
    "Mix all other ingredients in a pot and bring to a boil.~"
    "Pour over julienned jalapeños and let sit for 24 hours.",
    "Confirm preparation instructions with Leo."
)

R(
    "SESAME BROCCOLI", SALAD,
    "Broccoli|300|g;Garlic (Blitzed)|7.2|g;"
    "House Soy Sauce|6|g;Sesame Oil|4.8|g;"
    "Kosher Salt|1.92|g",
    "Cut broccoli into florets.~"
    "Steam broccoli in oven at 212°F for 3 minutes.~"
    "Cool in water bath.~"
    "Drain with a spinner.~"
    "Mix broccoli with garlic, house soy, sesame oil, and salt.~"
    "Put on flat hotel pan, saran wrap and put in fridge.",
    "Base: 1X = 300 g. Usual batches: "
    "2X = 600 g, 3X = 900 g, 4X = 1,200 g."
)

R(
    "WASABI CUCUMBER", SALAD,
    "Cucumber|1560|g;White Sugar|187|g;"
    "White Vinegar|125|g;Kosher Salt|47|g;"
    "Wasabi Powder|8|g",
    "Slice cucumbers 1/8th thickness using Robot Coupe or mandolin.~"
    "Add sugar and salt, mix well, then let sit 20 minutes.~"
    "Drain liquid.~"
    "Whisk wasabi into vinegar until dissolved.~"
    "Pour over cucumbers and cure overnight.~"
    "Rotate cucumbers for the next 2 days as wasabi powder sinks."
)


# ==========================================================
# PICKLED DAIKON SPECIAL QUANTITIES
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
    }
}


# ==========================================================
# INGREDIENT MULTIPLIER
# ==========================================================

def format_amount(
    amount,
    unit,
    multiplier,
    recipe_name=None,
    ingredient_name=None,
):
    amount = (
        str(amount).strip()
        if amount is not None
        else ""
    )

    unit = str(unit).strip()

    override = (
        SPECIAL_MULTIPLIERS
        .get(recipe_name, {})
        .get(multiplier, {})
        .get(ingredient_name)
    )

    if override is not None:
        return f"{override:,} {unit}"

    if amount in ("", "?"):
        return unit

    try:
        value = (
            Decimal(amount)
            * Decimal(str(multiplier))
        )

        if not value.is_finite():
            raise InvalidOperation

    except (InvalidOperation, ValueError, TypeError):
        return f"{amount} {unit}".strip()

    if value != value.to_integral_value():
        text = (
            f"{value:,.3f}"
            .rstrip("0")
            .rstrip(".")
        )

    else:
        text = f"{int(value):,}"

    return f"{text} {unit}"


def fmt_factor(factor):
    return f"{factor:g}X"


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
    st.session_state.multiplier = 1.0

if "custom_percentage" not in st.session_state:
    st.session_state.custom_percentage = None


def select_category(category):
    st.session_state.category = category
    st.session_state.recipe = None
    st.session_state.multiplier = 1.0
    st.session_state.custom_percentage = None


def select_recipe(name):
    st.session_state.recipe = name
    st.session_state.multiplier = 1.0
    st.session_state.custom_percentage = None


def select_multiplier(factor):
    st.session_state.multiplier = float(factor)
    st.session_state.custom_percentage = None


# ==========================================================
# CUSTOM PERCENTAGE MULTIPLIER
# ==========================================================

def set_custom_percent(percent_text):

    clean = (
        percent_text
        .strip()
        .replace("%", "")
        .replace(",", ".")
    )

    try:
        value = Decimal(clean)

    except InvalidOperation:
        return (
            "Enter a valid percentage such as "
            "75, 125 or 250."
        )

    if (
        not value.is_finite()
        or value <= 0
        or value > 10000
    ):
        return (
            "Choose a percentage above 0 "
            "and no greater than 10000."
        )

    st.session_state.custom_percentage = float(value)

    st.session_state.multiplier = float(
        value / Decimal(100)
    )

    return None


# ==========================================================
# CLEAN STYLESHEET - IPAD LANDSCAPE FIRST
# ==========================================================

st.markdown("""
<style>

:root {
    --ink: #26313A;
    --muted: #73808A;
    --line: #E0E5E6;
    --panel: #FFFFFF;
    --gold: #C6A057;
}

/* PAGE */

.stApp {
    background: #F4F6F5;
    color: var(--ink);
}

.block-container {
    max-width: 1480px;
    padding-top: 48px !important;
    padding-bottom: 30px;
}

#MainMenu, footer {
    visibility: hidden;
}

/* BRAND */

.brand-logo {
    font: 800 clamp(34px,4.3vw,56px)/1.1
          Arial, sans-serif;
    color: #E5252D;
    letter-spacing: -1.6px;
    text-align: center;
    margin: 0 0 8px;
}

.brand-subtitle {
    text-align: center;
    color: #7F898B;
    font: 600 11px Arial, sans-serif;
    letter-spacing: .22em;
    margin: 0 0 12px;
}

/* BASE BUTTONS */

.stButton > button,
[data-testid="stPopover"] button {
    background: #FFFFFF !important;
    color: var(--ink) !important;

    border: 1px solid #DCE2E3 !important;
    border-radius: 11px !important;

    box-shadow:
        0 2px 7px rgba(23,40,45,.045) !important;

    font-family: Arial, sans-serif !important;
    font-weight: 650 !important;

    transition:
        background .14s ease,
        border-color .14s ease !important;
}

.stButton > button:hover,
[data-testid="stPopover"] button:hover {
    background: #F8FAF9 !important;
    border-color: #9CA9AC !important;
}

.stButton > button p,
[data-testid="stPopover"] button p {
    color: inherit !important;
    font-weight: inherit !important;
}

/* CATEGORY TABS */

.st-key-cat_0 button,
.st-key-cat_1 button,
.st-key-cat_2 button {
    min-height: 64px !important;
    width: 100%;
    font-size: clamp(13px,1.35vw,17px) !important;
    letter-spacing: .015em;
}

.st-key-cat_0 button {
    color: #BD6B31 !important;
    border-bottom: 3px solid #D48A55 !important;
}

.st-key-cat_1 button {
    color: #C8464B !important;
    border-bottom: 3px solid #D8787B !important;
}

.st-key-cat_2 button {
    color: #4B8060 !important;
    border-bottom: 3px solid #80A68C !important;
}

/* RECIPE CARDS */

div[class*="st-key-recipe_"] button {
    width: 100%;
    min-height: 86px !important;
    padding: 12px !important;
    font-size: clamp(12px,1.35vw,17px) !important;
    text-align: left !important;
    line-height: 1.22 !important;
}

.st-key-recipe_grid_sauce
div[class*="st-key-recipe_"] button {
    border-left: 4px solid #D48A55 !important;
}

.st-key-recipe_grid_main
div[class*="st-key-recipe_"] button {
    border-left: 4px solid #D8787B !important;
}

.st-key-recipe_grid_salad
div[class*="st-key-recipe_"] button {
    border-left: 4px solid #80A68C !important;
}

/* MULTIPLIER BUTTONS - 15 CONTROLS */

.st-key-multiplier_row
[data-testid="stHorizontalBlock"] {
    gap: .22rem !important;
    flex-wrap: nowrap !important;
}

.st-key-multiplier_row
[data-testid="stColumn"] {
    min-width: 0 !important;
    width: 0 !important;
    flex: 1 1 0 !important;
}

.st-key-multiplier_row .stButton,
.st-key-multiplier_row
[data-testid="stPopover"] {
    width: 100% !important;
    min-width: 0 !important;
}

.st-key-multiplier_row button {
    width: 100% !important;
    min-width: 0 !important;
    padding: 0 2px !important;

    min-height: 53px !important;
    height: 53px !important;

    border-radius: 9px !important;
    font-size: clamp(10px,.9vw,13px) !important;
    white-space: nowrap !important;
}

.st-key-multiplier_row button:hover {
    border-color: #00A7C5 !important;
    color: #007F95 !important;
}

/* SELECTED BUTTONS */

.st-key-top_navigation
.selected-button button,
.st-key-multiplier_row
.selected-button button {
    border-color: #C6A057 !important;
    box-shadow:
        inset 0 0 0 1px #C6A057 !important;
    background: #FFFCF5 !important;
}

/* RECIPE HEADING */

.recipe-card-heading {
    font: 700 clamp(18px,1.9vw,26px)/1.2
          Arial,sans-serif;

    color: var(--recipe-accent,#26313A);

    padding: 15px 18px;
    background: #FFF;

    border: 1px solid #E2E6E6;
    border-left:
        4px solid var(--recipe-accent,#26313A);

    border-radius: 10px;
    overflow-wrap: anywhere;
}

.current-batch {
    font: 700 clamp(17px,1.8vw,23px)/1.3
          Arial,sans-serif;

    color: #008DA5;
    padding: 15px 0;
}

/* SECTION HEADINGS */

.section-title {
    font: 700 16px Arial,sans-serif;
    letter-spacing: .08em;
    color: #59666D;
    margin: 10px 0 9px;
}

/* INGREDIENTS */

.ingredient-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;

    border-bottom: 1px solid #E7EAEB;
    padding: 8px 0;

    font: 500 clamp(15px,1.5vw,19px)/1.35
          Arial,sans-serif;
}

.ingredient-name {
    overflow-wrap: anywhere;
}

.ingredient-amount {
    font-weight: 700;
    white-space: nowrap;
    font-variant-numeric: tabular-nums;
    color: #23313A;
}

/* PREPARATION STEPS */

.step-block {
    border-bottom: 1px solid #ECF0F0;

    padding: 0 0 12px;
    margin: 0 0 12px;

    font: 500 clamp(15px,1.5vw,19px)/1.48
          Arial,sans-serif;
}

.step-number {
    font-size: 12px;
    letter-spacing: .07em;
    color: #708088;
    font-weight: 800;
    margin-bottom: 6px;
}

/* RECIPE NOTES */

.recipe-notes {
    border-left: 3px solid #B8C4C7;
    background: #EDF2F2;
    border-radius: 7px;

    padding: 12px 16px;
    color: #485B62;
    margin-top: 15px;
    font-size: 15px;
}

.recipe-notes div + div {
    margin-top: 7px;
}

/* GENERAL SPACING */

.st-key-recipe_detail
[data-testid="stVerticalBlock"] {
    gap: .65rem;
}

/* LOGIN */

.login-heading {
    color: #26313A;
    font: bold 22px Arial,sans-serif;
    margin-bottom: 4px;
}

.login-instruction {
    color: #657178;
    font: 15px Arial,sans-serif;
}

[data-testid="stForm"] {
    background: #FFF;
    border: 1px solid #DEE4E4;
    border-radius: 12px;
    padding: 18px;
}

[data-testid="stTextInput"]
[data-baseweb="input"] {
    background: #FFF;
    border: 1px solid #A4B2B5;
    border-radius: 9px;
}

[data-testid="stTextInput"] input {
    background: #FFF;
    color: #26313A;
    caret-color: #C8464B;
}

[data-testid="stFormSubmitButton"] button {
    background: #26313A !important;
    color: #FFF !important;
    min-height: 44px;
}

/* LOG OUT */

.st-key-logout button {
    min-height: 46px;
    width: 100%;
    color: #59666D !important;
    font-size: 13px;
}

/* IPAD PORTRAIT */

@media(max-width:900px) {

    .block-container {
        padding-left: 14px;
        padding-right: 14px;
    }

    .st-key-multiplier_row
    [data-testid="stHorizontalBlock"] {
        overflow-x: auto !important;
        padding-bottom: 6px;
    }

    .st-key-multiplier_row
    [data-testid="stColumn"] {
        flex: 0 0 52px !important;
        width: 52px !important;
    }

    .st-key-cat_0 button,
    .st-key-cat_1 button,
    .st-key-cat_2 button {
        font-size: 12px !important;
        min-height: 58px !important;
        padding: 4px !important;
    }

    .recipe-card-heading {
        padding: 12px 9px;
        font-size: 17px;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# GOLD BUTTON HIGHLIGHT
# ==========================================================

def highlight_key(key):

    st.markdown(
        f'<style>'
        f'.st-key-{key} button {{'
        f'border-color:#C6A057 !important;'
        f'box-shadow:inset 0 0 0 1px #C6A057 !important;'
        f'background:#FFFCF5 !important;'
        f'}}'
        f'</style>',
        unsafe_allow_html=True,
    )


# ==========================================================
# PASSWORD PROTECTION
# ==========================================================

def login_screen():

    st.markdown(
        '<div class="brand-logo">riceislife</div>'
        '<div class="brand-subtitle">'
        'THE KITCHEN RECIPE BOOK'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="login-heading">Staff access</div>'
        '<p class="login-instruction">'
        'Enter the staff password to view recipes.'
        '</p>',
        unsafe_allow_html=True,
    )

    try:
        secret = str(st.secrets["STAFF_PASSWORD"])

    except Exception:
        st.error(
            "Set STAFF_PASSWORD in the "
            "Streamlit app's Secrets settings."
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

        if hmac.compare_digest(entered, secret):
            st.session_state.authenticated = True
            st.rerun()

        else:
            st.error("Incorrect password.")

    st.stop()


if not st.session_state.authenticated:
    login_screen()


# ==========================================================
# HEADER AND CATEGORY NAVIGATION
# ==========================================================

with st.container(key="top_navigation"):

    st.markdown(
        '<div class="brand-logo">riceislife</div>'
        '<div class="brand-subtitle">'
        'STAFF RECIPE LIBRARY'
        '</div>',
        unsafe_allow_html=True,
    )

    columns = st.columns(3, gap="medium")

    for index, cat in enumerate(CATEGORIES):

        with columns[index]:

            st.button(
                cat.upper(),
                key=f"cat_{index}",
                use_container_width=True,
                on_click=select_category,
                args=(cat,),
            )

            if st.session_state.category == cat:
                highlight_key(f"cat_{index}")


# ==========================================================
# RECIPE SELECTION PAGE
# ==========================================================

if st.session_state.recipe is None:

    current = st.session_state.category

    names = [
        n
        for n, data in RECIPES.items()
        if data["category"] == current
    ]

    grid_key = {
        SAUCE: "recipe_grid_sauce",
        MAIN: "recipe_grid_main",
        SALAD: "recipe_grid_salad",
    }[current]

    with st.container(key=grid_key):

        for start in range(0, len(names), 4):

            cols = st.columns(4, gap="medium")

            for index, name in enumerate(
                names[start:start + 4]
            ):

                with cols[index]:

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
    st.rerun()

recipe = RECIPES[recipe_name]
color = CATEGORY_COLORS[recipe["category"]]


with st.container(key="recipe_detail"):

    # ======================================================
    # 14 PRESET MULTIPLIERS + CUSTOM PERCENTAGE
    # ======================================================

    with st.container(key="multiplier_row"):

        cols = st.columns(15, gap="small")

        for index, factor in enumerate(MULTIPLIERS):

            with cols[index]:

                st.button(
                    fmt_factor(factor),
                    key=f"mult_{index}",
                    use_container_width=True,
                    on_click=select_multiplier,
                    args=(factor,),
                )

                if (
                    st.session_state.custom_percentage is None
                    and st.session_state.multiplier == factor
                ):
                    highlight_key(f"mult_{index}")

        # CUSTOM PERCENTAGE BUTTON

        with cols[14]:

            with st.popover(
                "?",
                use_container_width=True,
            ):

                st.markdown(
                    "**Custom batch percentage**"
                )

                st.caption(
                    "100% = 1X · 150% = 1.5X · "
                    "250% = 2.5X"
                )

                with st.form("custom_batch_form"):

                    percentage = st.text_input(
                        "Enter desired percentage",
                        placeholder="__%",
                        value="",
                    )

                    submitted = st.form_submit_button(
                        "Apply percentage",
                        use_container_width=True,
                    )

                if submitted:

                    error = set_custom_percent(
                        percentage
                    )

                    if error:
                        st.error(error)

                    else:
                        st.rerun()

    # ======================================================
    # CURRENT BATCH INDICATOR
    # ======================================================

    factor = st.session_state.multiplier

    if st.session_state.custom_percentage is not None:

        percentage_text = (
            f"{st.session_state.custom_percentage:g}%"
        )

        batch_text = (
            f"CURRENT BATCH: {percentage_text} "
            f"({factor:g}X)"
        )

    else:
        batch_text = f"CURRENT BATCH: {factor:g}X"

    # ======================================================
    # RECIPE HEADING
    # ======================================================

    heading_left, heading_right = st.columns(
        [1, 1],
        gap="large",
    )

    with heading_left:

        st.markdown(
            f'<div class="current-batch">'
            f'{escape(batch_text)}'
            f'</div>',
            unsafe_allow_html=True,
        )

    with heading_right:

        st.markdown(
            f'<div class="recipe-card-heading" '
            f'style="--recipe-accent:{color}">'
            f'{escape(recipe_name)}'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ======================================================
    # TWO-COLUMN RECIPE LAYOUT
    # ======================================================

    left, right = st.columns(
        [1, 1],
        gap="large",
    )

    # LEFT COLUMN - PREPARATION STEPS

    with left:

        st.markdown(
            '<div class="section-title">'
            'PREPARATION STEPS'
            '</div>',
            unsafe_allow_html=True,
        )

        if recipe["steps"]:

            for number, step in enumerate(
                recipe["steps"], 1
            ):

                html = (
                    '<div class="step-block">'
                    f'<div class="step-number">'
                    f'STEP {number:02d}'
                    '</div>'
                    f'<div>{escape(step)}</div>'
                    '</div>'
                )

                st.markdown(
                    html,
                    unsafe_allow_html=True,
                )

        else:
            st.warning(
                "Preparation steps have not been provided."
            )

    # RIGHT COLUMN - INGREDIENTS

    with right:

        st.markdown(
            '<div class="section-title">'
            'INGREDIENTS'
            '</div>',
            unsafe_allow_html=True,
        )

        for ingredient in recipe["ingredients"]:

            amount = format_amount(
                ingredient["amount"],
                ingredient["unit"],
                factor,
                recipe_name,
                ingredient["name"],
            )

            html = (
                '<div class="ingredient-row">'
                f'<span class="ingredient-name">'
                f'{escape(ingredient["name"])}'
                '</span>'
                f'<span class="ingredient-amount">'
                f'{escape(amount)}'
                '</span>'
                '</div>'
            )

            st.markdown(
                html,
                unsafe_allow_html=True,
            )

    # ======================================================
    # RECIPE NOTES
    # ======================================================

    if recipe["notes"]:

        html = "".join(
            f'<div>{escape(note)}</div>'
            for note in recipe["notes"]
        )

        st.markdown(
            f'<div class="recipe-notes">{html}</div>',
            unsafe_allow_html=True,
        )


# ==========================================================
# LOG OUT - BOTTOM RIGHT
# ==========================================================

st.divider()

spacer, logout = st.columns(
    [6, 1],
    gap="small",
)

with logout:

    if st.button(
        "Log Out",
        key="logout",
        use_container_width=True,
    ):

        st.session_state.authenticated = False
        st.session_state.recipe = None
        st.session_state.multiplier = 1.0
        st.session_state.custom_percentage = None

        st.rerun()
