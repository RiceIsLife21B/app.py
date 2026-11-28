
import streamlit as st
import hmac
import re
from decimal import Decimal, InvalidOperation
from html import escape

from remembered_sessions import COOKIE_NAME, TTL_SECONDS, RememberedSessions

# ==========================================================
# RICE IS LIFE - STAFF RECIPE BOOK
# COMPLETE APP - LARGE MULTIPLIER LABEL FIX
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

STAFF_PASSWORD = "aburi"

BACKGROUND = "#030303"
BUTTON_BG = "#393939"
WHITE = "#FFFFFF"
GOLD = "#C6A057"
MULTIPLIER_COLOR = "#0097B2"

CATEGORIES = [
    "Sauces + Dressings",
    "Mains + Marinades",
    "Salads + Pickles",
]

SAUCE, MAIN, SALAD = CATEGORIES

CATEGORY_COLORS = {
    SAUCE: "#D48A55",
    MAIN: "#ED555A",
    SALAD: "#81C568",
}

MULTIPLIERS = [
    1, 1.5, 2, 3, 4, 5, 6, 7,
    8, 9, 10, 13, 20, 30,
]

RECIPES = {}


# ==========================================================
# RECIPE PARSER
# ==========================================================

def R(name, category, ingredients, steps, notes=""):
    parsed = []

    for entry in ingredients.split(";"):
        if not entry.strip():
            continue

        parts = [p.strip() for p in entry.split("|")]

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
    "White Sugar|150|g;"
    "Mirin|150|g;"
    "House Soy Sauce|150|g;"
    "Water|20|g;"
    "Sesame Oil|30|g;"
    "Garlic|20|g;"
    "White Vinegar|15|g;"
    "Corn Starch|20|g;"
    "Ginger|10|g;"
    "Dashida|5|g;"
    "Black Pepper|3|g",
    "Grind garlic, ginger finely with mirin in Vitamix.~"
    "Mix together garlic, ginger and mirin with all other ingredients.~"
    "Bring to a boil, add the mix of corn starch and water.~"
    "Simmer 1-2 minutes and let cool.",
    "20x: fits in 12L cambro"
)

R(
    "CHOJANG (PORK BELLY)", SAUCE,
    "Gochujang Paste|6300|g;"
    "White Sugar|3700|g;"
    "Rice Vinegar|3300|g;"
    "Brown Sugar|500|g;"
    "Kosher Salt|250|g;"
    "Hon Dashi|130|g",
    "Whisk sugars, salt and hon dashi into rice vinegar.~"
    "Whisk at low heat until hon dashi and sugars are dissolved.~"
    "Add Gochujang paste last.",
    "Final product: every 500g add 20g of brown sugar.~"
    "1x: fits 22L cambro"
)

R(
    "HOT MAYO MUSTARD", SAUCE,
    "House Mayo|800|g;"
    "Dijon Mustard|440|g;"
    "Lemon Juice|120|g;"
    "Mirin|100|g;"
    "Rice Vinegar|80|g;"
    "White Sugar|60|g",
    "Whisk all ingredients together until sugar is dissolved."
)

R(
    "HOT SAUCE", SAUCE,
    "Habanero Peppers|2000|g;"
    "Sherry Vinegar|1200|g;"
    "Water|700|g;"
    "Bell Peppers|500|g;"
    "White Sugar|100|g;"
    "Kosher Salt|100|g;"
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
    "Rice Vinegar|600|g;"
    "Carrots|540|g;"
    "Canola Oil|320|g;"
    "Onions|280|g;"
    "White Sugar|120|g;"
    "Ginger|68|g;"
    "Miso Paste|32|g;"
    "Kosher Salt|24|g;"
    "Sesame Oil|20|g;"
    "Black Pepper|4|g",
    "Peel carrots, onions and ginger.~"
    "Cut into small chunks.~"
    "Blend carrots, onions and ginger with rice vinegar in Vitamix until smooth.~"
    "Combine blended vegetables with remaining ingredients and whisk until smooth.",
    "IMPORTANT: Original specifies making two separate 5X batches for 10X, NOT a 10X batch.~"
    "5X: fits in 12L cambro"
)

R(
    "HOUSE MAYO", SAUCE,
    "Hellman's Mayo|5000|g;"
    "Lemon Juice|500|g;"
    "Mushroom Powder|100|g",
    "Mix mushroom powder into lemon juice until dissolved.~"
    "Whisk mixture into mayo.",
    "3x: fits in 22L cambro"
)

R(
    "KANG JEONG(KFC)", SAUCE,
    "Corn Syrup|2500|g;"
    "Ketchup|1500|g;"
    "Gochujang Paste|500|g;"
    "Minced Garlic|300|g;"
    "MSG|10|g;"
    "House Soy Sauce|200|g;"
    "Mushroom Powder|10|g",
    "Mix all ingredients together.",
    "1x: fits in 5L cambro"
)

R(
    "MISO GLAZE(SALMON)", SAUCE,
    "House Teriyaki Sauce|100|g;"
    "Water|50|g;"
    "Corn Starch|50|g;"
    "Aka Miso Paste|15|g",
    "Whisk the miso paste into the teriyaki.~"
    "Make the cornstarch slurry with cold water.~"
    "Slowly whisk in slurry and simmer for one minute.",
    "Gently heat, do not let boil."
)

R(
    "SEASONED SOY(GF)", SAUCE,
    "House Soy Sauce|2000|g;"
    "Water|1000|g;"
    "Mirin|900|g;"
    "Sake|600|g;"
    "Kombu|50|g;"
    "Bonito|25|g",
    "Combine everything in a pot and bring to a boil.~"
    "Cool and infuse overnight, then strain.",
    "Original recipe makes approximately 5L.~"
    "5x: fits 22L cambro"
)

R(
    "SPICY MAYO", SAUCE,
    "House Mayo|400|g;"
    "Gochujang Paste|40|g;"
    "House Hot Sauce|40|g",
    "Mix all ingredients together."
)

R(
    "SUSHI SU", SAUCE,
    "Mizkan Yamabuki Vinegar|4000|g;"
    "White Sugar|1750|g;"
    "Aka Su|600|g;"
    "Kosher Salt|600|g;"
    "Kombu|30|g",
    "Whisk all ingredients at low temperasture until sugar and salt dissolve.",
    "Cool it down in ice bath. Do not let boil.~"
    "3x: fits 22L cambro"
)

R(
    "TENTSUYU(TOFU)", SAUCE,
    "Water|400|g;"
    "House Soy Sauce|200|g;"
    "Mirin|160|g;"
    "White Sugar|20|g;"
    "Mushroom Powder|8|g",
    "Whisk all ingredients until dissolved."
)

R(
    "TERIYAKI SAUCE(CHICKEN)", SAUCE,
    "House Soy Sauce|4000|g;"
    "Sake|4000|g;"
    "Mirin|4000|g;"
    "White Sugar|3000|g;"
    "Garlic(Crushed)|300|g;"
    "Water|130|g;"
    "Cornstarch|130|g;"
    "Ginger(Crushed)|100|g",
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
    "Garlic|1100|g;"
    "White Sugar|1000|g;"
    "Lemon Juice|825|g;"
    "Honey|500|g;"
    "Corn Syrup|500|g;"
    "Canola Oil|500|g;"
    "Yuzu|300|g;"
    "Yuzu Kosho|160|g;"
    "Water|50|g;"
    "Corn Starch|50|g;"
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
    "Kosher Salt|600|g;"
    "Black Pepper|400|g;"
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
    "All Purpose Flour|205|g;"
    "House Soy Sauce|10|g;"
    "Kosher Salt|3|g;"
    "Can of Club Soda|355|ml",
    "Whisk all ingredients together until no lumps remain."
)

R(
    "CHICKEN BRINE", MAIN,
    "Water|2000|g;"
    "House Soy Sauce|100|g;"
    "Kosher Salt|50|g;"
    "White Sugar|20|g;"
    "Garlic(Crushed)|15|g;"
    "Ginger(Crushed)|15|g",
    "Whisk all ingredients together until sugar dissolved.~"
    "Brine chicken for 24 hours."
)

R(
    "DASHI", MAIN,
    "Water|20|L;"
    "Roasted Salmon Head|1|pc;"
    "Daikon|1000|g;"
    "Mirin|190|g;"
    "Whole Green Onions|150|g;"
    "Kombu|70|g;"
    "Kosher Salt|50|g;"
    "Katsuo Bushi|40|g;"
    "Dried Shiitake Mushroom|30|g;"
    "Hon Dashi|4|g",
    "Roast Salmon Head at 460°C at 50% Humidity for 15-20 minutes.~"
    "Slice Daikon in 1 inch thickness.~"
    "Bring all ingredients to boil in pot.~"
    "Skim surface, and simmer for 40 minutes.~"
    "After simmering, strain while still hot.~"
    "Then cool in ice water bath."
)

R(
    "DASHI EGG MARINADE", MAIN,
    "Water|2000|g;"
    "House Soy Sauce|300|g;"
    "White Sugar|100|g;"
    "Mirin|100|g;"
    "Kosher Salt|25|g;"
    "Hon Dashi|24|g;"
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
    "Green Onion Whites|200|g;"
    "Canola Oil|150|g;"
    "Garlic|100|g;"
    "White Vinegar|20|g;"
    "Ginger|20|g;"
    "Kosher Salt|5|g;"
    "Black Pepper|2|g",
    "slice the green onion whites, garlic and ginger.~"
    "Mix all ingredients together."
)

R(
    "JAPANESE CURRY", MAIN,
    "Dashi|1.5|L;"
    "Curry Powder|??|g;"
    "Onions|600|g;"
    "Carrots|450|g;"
    "Potatoes|300|g;"
    "Kosher Salt|10|g;"
    "Mushroom Powder|10|g;"
    "Sesame Oil|5|ml to taste",
    "Dice potato and keep in cold water for service.~"
    "Dry them off prior to deep frying for 90 seconds.~"
    "Mix into curry and serve."
)

R(
    "MISO MARINADE", MAIN,
    "Miso Paste|1000|g;"
    "White Sugar|600|g;"
    "Water|400|g;"
    "Mirin|200|g;"
    "House Soy Sauce|150|g",
    "Whisk all ingredients together until dissolved."
)

R(
    "MISO SOUP", MAIN,
    "Dashi|4|L;"
    "Aka Miso Paste|200|g;"
    "Hon Dashi|4|g;"
    "Kosher Salt|1|g",
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
    "White Sugar|20|g;"
    "Ginger|20|g;"
    "Kombu|10|g",
    "Soak shiitake mushroom in water overnight.~"
    "Combine everything in a pot and simmer mushrooms for 30 minutes with a cartouche."
)

R(
    "PORK BELLY", MAIN,
    "Pork Belly|1|slab;"
    "Mirin|200|g;"
    "Kosher Salt|125|g;"
    "Sesame Oil|100|g;"
    "White Sugar|50|g;"
    "Ginger (Sliced)|2|pc;"
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
    "Sekka Rice|1100|g;"
    "Water|1080|g;"
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
    "Sekka Rice|2740|g;"
    "Water (White Rice)|2740|g;"
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
    "House Soy Sauce|30|g;"
    "Dashida / Mushroom Powder|10|g;"
    "Gochugaru|10|g;"
    "Black Pepper|3|g",
    "Mix all ingredients together.~"
    "Brush all 6 sides of cut tofu with marinade."
)


# ==========================================================
# SALADS + PICKLES
# ==========================================================

R(
    "BEAN SPROUTS", SALAD,
    "Raw Bean Sprouts|3000|g;"
    "Fish Sauce|118.8|g;"
    "Sesame Oil|79.2|g;"
    "Garlic (Blitzed)|66|g;"
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
    "House Soy Sauce|100|g;"
    "White Sugar|50|g;"
    "Gochujang Paste|40|g;"
    "Rice Flour|30|g;"
    "Gochugaru|20|g",
    "Cut chives into 2 inch pieces.~"
    "Combine all ingredients except chives into a paste.~"
    "Massage paste into chives.~"
    "Leave at room temperature or a warm spot for 2 hours to ferment.~"
    "Refrigerate; original says store up to two weeks."
)

R(
    "KIMCHI COLESLAW", SALAD,
    "Green Cabbage|20000|g;"
    "Kimchi|10000|g;"
    "White Sugar|2000|g;"
    "Lemon Juice|2000|g;"
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
    "Daikon|1000|g;"
    "Water|600|g;"
    "Rice Vinegar|400|g;"
    "White Sugar|340|g;"
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
    "Jalapeño|1800|g;"
    "White Sugar|500|g;"
    "House Soy Sauce|500|g;"
    "Water|500|g;"
    "White Vinegar|500|g;"
    "Kosher Salt|20|g;"
    "Garlic Cloves|10|pcs",
    "Wash, halve, clean and julienne jalapeño peppers.~"
    "Mix all other ingredients in a pot and bring to a boil.~"
    "Pour over julienned jalapeños and let sit for 24 hours.",
    "Confirm preparation instructions with Leo."
)

R(
    "SESAME BROCCOLI", SALAD,
    "Broccoli|300|g;"
    "Garlic (Blitzed)|7.2|g;"
    "House Soy Sauce|6|g;"
    "Sesame Oil|4.8|g;"
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
    "Cucumber|1560|g;"
    "White Sugar|187|g;"
    "White Vinegar|125|g;"
    "Kosher Salt|47|g;"
    "Wasabi Powder|8|g",
    "Slice cucumbers 1/8th thickness using Robot Coupe or mandolin.~"
    "Add sugar and salt, mix well, then let sit 20 minutes.~"
    "Drain liquid.~"
    "Whisk wasabi into vinegar until dissolved.~"
    "Pour over cucumbers and cure overnight.~"
    "Rotate cucumbers for the next 2 days as wasabi powder sinks."
)


# ==========================================================
# PICKLED DAIKON SPECIAL AMOUNTS
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
# SAFE INGREDIENT MULTIPLIER
# ==========================================================

def format_amount(
    amount,
    unit,
    multiplier,
    recipe_name=None,
    ingredient_name=None,
):
    amount = "" if amount is None else str(amount).strip()
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
        value = Decimal(amount) * Decimal(str(multiplier))

        if not value.is_finite():
            raise InvalidOperation

    except (InvalidOperation, ValueError, TypeError):
        return f"{amount} {unit}".strip()

    if value == value.to_integral_value():
        text = f"{int(value):,}"
    else:
        text = f"{value:,.3f}".rstrip("0").rstrip(".")

    return f"{text} {unit}"


def fmt_factor(factor):
    return f"{factor:g}X"


# ==========================================================
# CONTAINER GUIDE NOTES
# ==========================================================

def split_recipe_notes(notes):
    container_notes = []
    general_notes = []

    pattern = re.compile(
        r"^\s*\d+(?:\.\d+)?\s*x\s*:\s*fits\b",
        re.IGNORECASE,
    )

    for note in notes:
        if pattern.search(note):
            container_notes.append(note)
        else:
            general_notes.append(note)

    return container_notes, general_notes


# ==========================================================
# APPLICATION STATE
# ==========================================================

@st.cache_resource(show_spinner=False)
def remembered_sessions():
    return RememberedSessions()


remember_cookie = st.components.v2.component(
    "omai_remember_cookie",
    js="""
    export default function ({ data, setTriggerValue }) {
        const { name, token, maxAge } = data;
        const saved = () => document.cookie.split('; ').includes(`${name}=${token}`);
        try {
            if (maxAge === 0 && !saved()) return;  // Preserve a newer token from another tab.
            const value = maxAge > 0 ? token : '';
            document.cookie = `${name}=${value}; Max-Age=${maxAge}; Path=/; Secure; SameSite=Lax`;
            if (maxAge > 0 && !saved()) setTriggerValue('blocked', true);
        } catch {
            if (maxAge > 0) setTriggerValue('blocked', true);
        }
    }
    """,
)


if "authenticated" not in st.session_state:
    # The cookie is a browser credential, not proof of login by itself.
    token = st.context.cookies.get(COOKIE_NAME)
    st.session_state.authenticated = remembered_sessions().is_valid(token)
    st.session_state.remembered_token = token if st.session_state.authenticated else None

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
        str(percent_text)
        .strip()
        .replace("%", "")
        .replace(",", ".")
    )

    try:
        value = Decimal(clean)
    except (InvalidOperation, ValueError):
        return "Enter a valid percentage such as 75 or 125."

    if not value.is_finite() or value <= 0 or value > 10000:
        return "Choose a percentage above 0 and up to 10000."

    st.session_state.custom_percentage = float(value)
    st.session_state.multiplier = float(value / Decimal(100))

    return None


# ==========================================================
# STYLESHEET
# ==========================================================

st.markdown("""
<style>

/* PAGE */

html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section[data-testid="stMain"] {
    background: #030303 !important;
    color: #FFFFFF !important;
}

.block-container {
    max-width: 1480px;
    padding: 48px 12px 35px !important;
}

#MainMenu,
footer {
    visibility: hidden;
}

.stApp,
.stApp p,
.stApp label,
.stApp h1,
.stApp h2,
.stApp h3 {
    color: #FFFFFF;
}

/* BRAND */

.brand-logo {
    color: #ED2227 !important;
    font-family: Arial, Helvetica, sans-serif;
    font-size: clamp(36px, 4.5vw, 58px);
    font-weight: 800;
    letter-spacing: -1.5px;
    text-align: center;
    line-height: 1.1;
    margin: 0 0 8px;
}

.brand-subtitle {
    color: #B4B4B4 !important;
    text-align: center;
    font: 600 11px Arial, Helvetica, sans-serif;
    letter-spacing: .20em;
    margin-bottom: 15px;
}

/* ALL BUTTONS - SOFT GLOW */

.stButton > button,
[data-testid="stPopover"] button,
[data-testid="stFormSubmitButton"] button {
    background: #393939 !important;
    color: #FFFFFF !important;
    border: 2px solid #686868 !important;
    border-radius: 9px !important;

    box-shadow:
        0 4px 12px rgba(0, 0, 0, .70),
        0 0 12px rgba(255, 255, 255, .16),
        0 0 23px rgba(255, 255, 255, .07)
        !important;

    font-family: Arial, Helvetica, sans-serif;
    font-weight: 600 !important;
    transition: background .16s ease, box-shadow .16s ease;
}

.stButton > button:hover,
[data-testid="stPopover"] button:hover,
[data-testid="stFormSubmitButton"] button:hover {
    background: #474747 !important;

    box-shadow:
        0 6px 16px rgba(0, 0, 0, .75),
        0 0 18px rgba(255, 255, 255, .23),
        0 0 28px rgba(255, 255, 255, .10)
        !important;
}

.stButton > button p,
[data-testid="stPopover"] button p,
[data-testid="stFormSubmitButton"] button p {
    color: inherit !important;
}

/* CATEGORY BUTTONS */

.st-key-cat_0 button,
.st-key-cat_1 button,
.st-key-cat_2 button {
    background: #030303 !important;
    min-height: 66px !important;
    width: 100%;
    font-size: clamp(13px, 1.35vw, 18px) !important;
    font-weight: 700 !important;
}

.st-key-cat_0 button,
.st-key-cat_0 button p {
    color: #D48A55 !important;
}

.st-key-cat_1 button,
.st-key-cat_1 button p {
    color: #ED555A !important;
}

.st-key-cat_2 button,
.st-key-cat_2 button p {
    color: #81C568 !important;
}

/* RECIPE BUTTONS */

div[class*="st-key-recipe_"] button {
    background: #393939 !important;
    min-height: 86px !important;
    padding: 14px 16px !important;

    font-size: clamp(13px, 1.3vw, 17px) !important;
    font-weight: 700 !important;

    text-align: left !important;
    border: 2px solid !important;

    box-shadow:
        0 5px 14px rgba(0, 0, 0, .74),
        0 0 12px rgba(255, 255, 255, .13),
        0 0 23px rgba(255, 255, 255, .055)
        !important;
}

.st-key-recipe_grid_sauce
div[class*="st-key-recipe_"] button {
    border-color: #D48A55 !important;
    color: #D48A55 !important;
}

.st-key-recipe_grid_sauce
div[class*="st-key-recipe_"] button p {
    color: #D48A55 !important;
}

.st-key-recipe_grid_main
div[class*="st-key-recipe_"] button {
    border-color: #ED555A !important;
    color: #ED555A !important;
}

.st-key-recipe_grid_main
div[class*="st-key-recipe_"] button p {
    color: #ED555A !important;
}

.st-key-recipe_grid_salad
div[class*="st-key-recipe_"] button {
    border-color: #81C568 !important;
    color: #81C568 !important;
}

.st-key-recipe_grid_salad
div[class*="st-key-recipe_"] button p {
    color: #81C568 !important;
}

/* ======================================================
   MULTIPLIER ROW - 15 SQUARE BUTTONS
   ====================================================== */

.st-key-multiplier_row [data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-wrap: nowrap !important;
    gap: 3px !important;
    width: 100% !important;
    min-width: 0 !important;
    padding: 12px 3px 20px !important;
    overflow: visible !important;
}

.st-key-multiplier_row [data-testid="stColumn"] {
    flex: 1 1 0 !important;
    min-width: 0 !important;
    width: 0 !important;
    max-width: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

.st-key-multiplier_row .stButton,
.st-key-multiplier_row [data-testid="stPopover"] {
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
}

/* Button size and solid blue color */

.st-key-multiplier_row .stButton > button,
.st-key-multiplier_row [data-testid="stPopover"] > button,
.st-key-multiplier_row [data-testid="stPopover"] button {
    width: 100% !important;
    aspect-ratio: 1 / 1 !important;

    min-width: 0 !important;
    max-width: 100% !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;

    padding: 0 !important;
    margin: 0 !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    box-sizing: border-box !important;
    overflow: hidden !important;

    background: #0097B2 !important;
    color: #FFFFFF !important;

    border: 2px solid #0097B2 !important;
    border-radius: 0 !important;

    box-shadow:
        0 4px 10px rgba(0, 0, 0, .70),
        0 0 12px rgba(0, 151, 178, .48),
        0 0 22px rgba(0, 151, 178, .24)
        !important;
}

/* ======================================================
   ACTUAL STREAMLIT BUTTON LABEL FIX

   Apply size to the markdown container AND its text.
   Unlike previous attempts, no text scaling/compression.
   ====================================================== */

/* Preset buttons use st-key-mult_0 etc.
   This is deliberately independent of container styling. */

div[class*="st-key-mult_"] button {
    font-size: clamp(24px, 2.8vw, 36px) !important;
    font-weight: 900 !important;
}

div[class*="st-key-mult_"] button
[data-testid="stMarkdownContainer"],

div[class*="st-key-mult_"] button
[data-testid="stMarkdownContainer"] p,

div[class*="st-key-mult_"] button p,

div[class*="st-key-mult_"] button span {
    font-size: clamp(24px, 2.8vw, 36px) !important;
    font-weight: 900 !important;
    line-height: 1 !important;
    letter-spacing: -1px !important;

    color: #FFFFFF !important;
    white-space: nowrap !important;

    transform: none !important;
    zoom: 1 !important;
    font-stretch: normal !important;

    width: auto !important;
    max-width: none !important;

    margin: 0 !important;
    padding: 0 !important;
}

/* Slightly smaller for the longest label 1.5X
   so it fits within the same square. */

.st-key-mult_1 button,
.st-key-mult_1 button p,
.st-key-mult_1 button span,
.st-key-mult_1 button [data-testid="stMarkdownContainer"] {
    font-size: clamp(21px, 2.45vw, 30px) !important;
    letter-spacing: -1.5px !important;
}

/* Custom % button label */

.st-key-multiplier_row
[data-testid="stPopover"] button {
    font-size: clamp(24px, 2.8vw, 36px) !important;
    font-weight: 900 !important;
}

.st-key-multiplier_row
[data-testid="stPopover"] button p,

.st-key-multiplier_row
[data-testid="stPopover"] button span,

.st-key-multiplier_row
[data-testid="stPopover"] button
[data-testid="stMarkdownContainer"] {
    font-size: clamp(24px, 2.8vw, 36px) !important;
    font-weight: 900 !important;
    line-height: 1 !important;

    color: #FFFFFF !important;
    transform: none !important;
    zoom: 1 !important;
}

/* Selected preset glow and hover */

.st-key-multiplier_row button:hover {
    background: #0AABC6 !important;
    border-color: #0AABC6 !important;
}

/* CURRENT BATCH */

.current-batch {
    color: #FFFFFF !important;
    font: 700 clamp(18px, 1.8vw, 24px)/1.3 Arial, sans-serif;
    padding: 10px 0 6px;
    margin-bottom: 5px;
}

/* CONTAINER GUIDE */

.container-guide {
    background: #141414 !important;
    border: 1px solid #484848;
    border-left: 3px solid #C6A057;
    border-radius: 8px;
    padding: 13px 17px;
    margin: 0 0 14px;
    min-height: 64px;
}

.container-guide-label {
    color: #C6A057 !important;
    font: 800 11px Arial, sans-serif;
    letter-spacing: .12em;
    margin-bottom: 7px;
}

.container-guide-value {
    color: #FFFFFF !important;
    font: 600 clamp(14px, 1.35vw, 18px)/1.45 Arial, sans-serif;
}

.container-guide-value + .container-guide-value {
    margin-top: 6px;
}

/* RECIPE TITLE */

.recipe-card-heading {
    background: #030303 !important;
    color: var(--recipe-accent, #FFFFFF) !important;

    font: 700 clamp(19px, 1.9vw, 26px)/1.2 Arial, sans-serif;

    border: 2px solid var(--recipe-accent, #FFFFFF);
    border-radius: 9px;

    padding: 15px 18px;
    min-height: 64px;

    display: flex;
    align-items: center;
    overflow-wrap: anywhere;
}

/* SECTION HEADINGS */

.section-title {
    color: var(--category-accent, #FFFFFF) !important;
    font: 800 17px Arial, sans-serif;
    letter-spacing: .08em;
    margin: 10px 0 12px;
}

/* INGREDIENTS WITH DOTTED LEADERS */

.ingredient-row {
    display: flex;
    align-items: baseline;
    gap: 14px;

    border-bottom: 1px solid #292929;
    padding: 9px 0;

    color: #FFFFFF !important;
    font: 500 clamp(15px, 1.5vw, 19px)/1.35 Arial, sans-serif;
}

.ingredient-name {
    color: #FFFFFF !important;
    overflow-wrap: anywhere;
    flex: 0 1 auto;
    order: 1;
}

.ingredient-row::after {
    content: "";
    flex: 1 1 auto;
    min-width: 10px;
    border-bottom: 2px dotted #727272;
    transform: translateY(-3px);
    order: 2;
}

.ingredient-amount {
    color: #FFFFFF !important;
    font-weight: 700;
    text-align: right;
    white-space: nowrap;
    font-variant-numeric: tabular-nums;
    flex: 0 0 auto;
    order: 3;
}

/* PREPARATION STEPS */

.step-block {
    color: #FFFFFF !important;
    border-bottom: 1px solid #292929;
    padding-bottom: 14px;
    margin-bottom: 14px;

    font: 500 clamp(15px, 1.5vw, 19px)/1.5 Arial, sans-serif;
}

.step-number {
    color: #545454 !important;
    font: 800 13px Arial, sans-serif;
    letter-spacing: .07em;
    margin-bottom: 7px;
}

.step-instruction {
    color: #FFFFFF !important;
}

/* NOTES */

.recipe-notes {
    background: #111111 !important;
    border: 1px solid #383838;
    border-left: 3px solid #C6A057;
    border-radius: 8px;
    padding: 14px 18px;
    margin-top: 18px;

    color: #FFFFFF !important;
    font-size: 15px;
    line-height: 1.5;
}

.recipe-notes div {
    color: #FFFFFF !important;
}

.recipe-notes div + div {
    margin-top: 8px;
}

/* LOGIN */

.login-error {
    background: #2D1117;
    border: 1px solid #A9454D;
    border-radius: 9px;
    color: #FF8088 !important;
    font-weight: 600;
    padding: .75rem 1rem;
    text-align: center;
}

.login-heading {
    color: #FFFFFF !important;
    font: 700 24px Arial, sans-serif;
}

.login-instruction {
    color: #FFFFFF !important;
    font: 16px Arial, sans-serif;
}

[data-testid="stForm"] {
    background: #030303 !important;
    border: 1px solid #383838 !important;
    border-radius: 12px !important;
    padding: 18px;
}

[data-testid="stTextInput"]
[data-baseweb="input"] {
    background: #030303 !important;
    border: 1px solid #555555 !important;
    border-radius: 8px !important;
}

[data-testid="stTextInput"] input {
    background: #030303 !important;
    color: #FFFFFF !important;
    caret-color: #FFFFFF !important;
    font-size: 18px !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: #999999 !important;
}

[data-testid="stTextInput"] button,
[data-testid="stTextInput"] button:hover {
    background: #030303 !important;
    color: #FFFFFF !important;
    border: none !important;
}

[data-testid="stTextInput"] button svg {
    stroke: #FFFFFF !important;
}

/* CUSTOM PERCENTAGE POPOVER */

[data-testid="stPopoverBody"],
[data-testid="stPopoverContent"],
div[data-baseweb="popover"] > div {
    background: #111111 !important;
    color: #FFFFFF !important;
    border-color: #383838 !important;
}

[data-testid="stPopoverBody"] p,
[data-testid="stPopoverBody"] label {
    color: #FFFFFF !important;
}

[data-testid="stPopoverBody"]
[data-testid="stForm"] {
    background: #111111 !important;
}

[data-testid="stPopoverBody"]
[data-testid="stFormSubmitButton"] button {
    background: #393939 !important;
    color: #FFFFFF !important;
    border: 1px solid #C6A057 !important;
    min-height: 44px !important;
}

/* LOG OUT */

.st-key-logout button {
    background: #393939 !important;
    color: #FFFFFF !important;
    min-height: 48px !important;
    width: 100% !important;
}

/* ======================================================
   RESPONSIVE
   ====================================================== */

@media (max-width: 900px) {

    .block-container {
        padding-left: 8px !important;
        padding-right: 8px !important;
    }

    .st-key-cat_0 button,
    .st-key-cat_1 button,
    .st-key-cat_2 button {
        min-height: 58px !important;
        font-size: 12px !important;
    }

    div[class*="st-key-recipe_"] button {
        min-height: 78px !important;
        padding: 9px !important;
        font-size: 12px !important;
    }

    div[class*="st-key-mult_"] button,
    div[class*="st-key-mult_"] button p,
    div[class*="st-key-mult_"] button span {
        font-size: clamp(20px, 3vw, 27px) !important;
    }

    .st-key-mult_1 button,
    .st-key-mult_1 button p,
    .st-key-mult_1 button span {
        font-size: clamp(17px, 2.5vw, 23px) !important;
    }

    .recipe-card-heading {
        font-size: 17px;
        padding: 12px 10px;
    }

    .ingredient-row {
        padding: 7px 0;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# SELECTED CATEGORY STYLING
# ==========================================================

def highlight_category(index):
    color = CATEGORY_COLORS[CATEGORIES[index]]

    st.markdown(
        '<style>'
        f'.st-key-cat_{index} button {{'
        f'border:3px solid {color} !important;'
        f'box-shadow:0 0 0 1px {color},'
        f'0 0 15px {color}55 !important;'
        'background:#111111 !important;'
        '}'
        '</style>',
        unsafe_allow_html=True,
    )


# ==========================================================
# SELECTED MULTIPLIER STYLING
# ==========================================================

def highlight_multiplier(key):
    st.markdown(
        '<style>'
        f'.st-key-{key} button {{'
        'background:#0097B2 !important;'
        'border:3px solid #C6A057 !important;'
        'box-shadow:0 0 0 1px #C6A057,'
        '0 0 18px rgba(0,151,178,.55) !important;'
        '}'
        '</style>',
        unsafe_allow_html=True,
    )


# ==========================================================
# PASSWORD PROTECTION
# ==========================================================

def show_login_error(message):
    st.markdown(
        f'<div class="login-error" role="alert">{escape(message)}</div>',
        unsafe_allow_html=True,
    )


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

    with st.form("login_form"):
        entered = st.text_input(
            "Staff password",
            type="password",
            placeholder="Enter password",
        )
        remember_device = st.checkbox(
            "Remember this device",
            help="Stay signed in for up to 24 hours, unless the app restarts.",
        )
        submit = st.form_submit_button("Log In")

    if submit:
        if hmac.compare_digest(entered, STAFF_PASSWORD):
            st.session_state.authenticated = True
            if remember_device:
                token = remembered_sessions().issue()
                st.session_state.remembered_token = token
                st.session_state.remember_cookie_update = (token, TTL_SECONDS)
            st.rerun()
        else:
            show_login_error("Incorrect password.")

    st.stop()


def end_login():
    token = st.session_state.pop("remembered_token", None)
    if token is not None:
        remembered_sessions().revoke(token)
        st.session_state.remember_cookie_update = (token, 0)
    st.session_state.authenticated = False
    st.session_state.recipe = None
    st.session_state.multiplier = 1.0
    st.session_state.custom_percentage = None
    st.session_state.pop("remember_cookie_blocked", None)


def remember_cookie_blocked():
    remembered_sessions().revoke(st.session_state.pop("remembered_token", None))
    st.session_state.remember_cookie_blocked = True


# Recheck remembered logins so expired or revoked tokens lose access on rerun.
active_token = st.session_state.get("remembered_token")
if active_token is not None and not remembered_sessions().is_valid(active_token):
    end_login()

cookie_update = st.session_state.pop("remember_cookie_update", None)
if cookie_update is not None:
    token, max_age = cookie_update
    remember_cookie(
        data={"name": COOKIE_NAME, "token": token, "maxAge": max_age},
        on_blocked_change=remember_cookie_blocked,
    )

if st.session_state.get("remember_cookie_blocked"):
    show_login_error(
        "This browser could not save the sign-in cookie. "
        "Use HTTPS and allow cookies to stay signed in after a refresh."
    )

if not st.session_state.authenticated:
    login_screen()


def render_logout():
    st.divider()
    _, logout = st.columns([6, 1], gap="small")
    with logout:
        st.button(
            "Log Out",
            key="logout",
            use_container_width=True,
            on_click=end_login,
        )


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
                highlight_category(index)


# ==========================================================
# RECIPE SELECTION PAGE
# ==========================================================

if st.session_state.recipe is None:
    current = st.session_state.category

    names = [
        name
        for name, data in RECIPES.items()
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

            for index, name in enumerate(names[start:start + 4]):
                with cols[index]:
                    st.button(
                        name,
                        key=f"recipe_{start + index}",
                        use_container_width=True,
                        on_click=select_recipe,
                        args=(name,),
                    )

    render_logout()
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

container_notes, general_notes = split_recipe_notes(
    recipe["notes"]
)


with st.container(key="recipe_detail"):

    # ======================================================
    # MULTIPLIER ROW - % FIRST
    # ======================================================

    with st.container(key="multiplier_row"):
        cols = st.columns(15, gap=None)

        # CUSTOM PERCENTAGE BUTTON

        with cols[0]:
            with st.popover("%", use_container_width=True):
                st.markdown("**Custom batch percentage**")

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
                    error = set_custom_percent(percentage)

                    if error:
                        st.error(error)
                    else:
                        st.rerun()

        # PRESET MULTIPLIERS

        for index, factor in enumerate(MULTIPLIERS):
            with cols[index + 1]:
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
                    highlight_multiplier(f"mult_{index}")

    # ======================================================
    # CURRENT BATCH
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

    st.markdown(
        '<div class="current-batch">'
        f'{escape(batch_text)}'
        '</div>',
        unsafe_allow_html=True,
    )

    # ======================================================
    # TWO-COLUMN RECIPE LAYOUT
    # ======================================================

    left, right = st.columns(
        [1, 1],
        gap="large",
    )

    # LEFT COLUMN

    with left:
        if container_notes:
            container_html = "".join(
                '<div class="container-guide-value">'
                f'{escape(note)}'
                '</div>'
                for note in container_notes
            )
        else:
            container_html = (
                '<div class="container-guide-value">'
                'No container size specified'
                '</div>'
            )

        st.markdown(
            '<div class="container-guide">'
            '<div class="container-guide-label">'
            'CONTAINER GUIDE'
            '</div>'
            f'{container_html}'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="section-title" '
            f'style="--category-accent:{color};">'
            'PREPARATION STEPS'
            '</div>',
            unsafe_allow_html=True,
        )

        if recipe["steps"]:
            for number, step in enumerate(recipe["steps"], 1):
                html = (
                    '<div class="step-block">'
                    '<div class="step-number">'
                    f'STEP #{number}'
                    '</div>'
                    '<div class="step-instruction">'
                    f'{escape(step)}'
                    '</div>'
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

    # RIGHT COLUMN

    with right:
        st.markdown(
            f'<div class="recipe-card-heading" '
            f'style="--recipe-accent:{color};">'
            f'{escape(recipe_name)}'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="section-title" '
            f'style="--category-accent:{color};">'
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

            ingredient_html = (
                '<div class="ingredient-row">'
                '<span class="ingredient-name">'
                f'{escape(ingredient["name"])}'
                '</span>'
                '<span class="ingredient-amount">'
                f'{escape(amount)}'
                '</span>'
                '</div>'
            )

            st.markdown(
                ingredient_html,
                unsafe_allow_html=True,
            )

    # GENERAL NOTES

    if general_notes:
        notes_html = "".join(
            f'<div>{escape(note)}</div>'
            for note in general_notes
        )

        st.markdown(
            '<div class="recipe-notes">'
            f'{notes_html}'
            '</div>',
            unsafe_allow_html=True,
        )


# ==========================================================
# LOG OUT
# ==========================================================

render_logout()
