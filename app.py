
import streamlit as st
import hmac
from decimal import Decimal

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

# ==========================================================
# RECIPE DATA
#
# Ingredients are entered as:
# Ingredient name | Base quantity | Unit
#
# Separate ingredients with semicolons.
# Separate preparation steps with ~
#
# A question mark means the amount is not specified.
# ==========================================================

RECIPES = {}


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


SAUCE = CATEGORIES[0]
MAIN = CATEGORIES[1]
SALAD = CATEGORIES[2]

# ==========================================================
# SAUCES + DRESSINGS
# ==========================================================

add(
    "BULGOGI SAUCE", SAUCE,
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
    Dashida (Beef Stock Powder)|5|g;
    Black Pepper|3|g
    """,
    """
    Grind garlic and ginger finely with mirin in the Vitamix.~
    Mix everything together.~
    Bring to a boil, then let cool.
    """
)

add(
    "CHOJANG", SAUCE,
    """
    Gochujang Sauce|6300|g;
    Sugar|3700|g;
    Rice Vinegar|3300|g;
    Brown Sugar|500|g;
    Salt|250|g;
    Hon Dashi (Fish Stock Powder)|130|g
    """,
    """
    Whisk sugars, salt and Hon Dashi into rice vinegar.~
    Add Gochujang last.~
    Whisk until Hon Dashi and sugars dissolve.
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
    Rice Vinegar|560|g;
    Carrots|540|g;
    Canola Oil|320|g;
    Onions|280|g;
    Sugar|120|g;
    Ginger|68|g;
    Miso|32|g;
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
    "IMPORTANT: Original specifies making two separate 5X batches for 10X. "
    "Original method says white vinegar, while ingredients say rice vinegar. "
    "Confirm which is correct before production."
)

add(
    "HOUSE MAYO", SAUCE,
    """
    Hellman's Mayo|5000|g;
    Lemon Juice|500|g;
    Dashida / Mushroom Powder|100|g
    """,
    """
    Mix Dashida or mushroom powder into lemon juice until dissolved.~
    Whisk mixture into mayo.
    """,
    "Original recipe makes approximately 6 L. Use a 15 L container."
)

add(
    "KANG JEONG", SAUCE,
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
    "MISO GLAZE", SAUCE,
    """
    Teriyaki|100|g;
    Miso Paste|15|g;
    Cornstarch Slurry|?|to taste
    """,
    """
    Whisk together teriyaki and miso paste.~
    Gently heat until simmering.~
    Make a cornstarch slurry with cold water.~
    Whisk in slurry slowly and simmer for one minute.
    """,
    "Cornstarch slurry has no fixed quantity in the original."
)

add(
    "SEASONED SOY (GF)", SAUCE,
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
    "Original recipe makes approximately 5 L."
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
    "TENTSUYU", SAUCE,
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
    "TERIYAKI SAUCE", SAUCE,
    """
    Tamari Soy Sauce|4000|g;
    Sugar|3000|g;
    Mirin|4000|g;
    Sake|4000|g;
    Garlic (Crushed)|300|g;
    Ginger (Crushed)|100|g;
    Water|130|g;
    Cornstarch|130|g
    """,
    """
    Combine soy, sugar, garlic and ginger.~
    Simmer for 30 minutes until flavors are infused.~
    Remove garlic and ginger.~
    Reduce by one quarter or until desired consistency.~
    Create a slurry with cornstarch and water if needed.~
    Whisk in slurry slowly and simmer for one minute.~
    Cool down.
    """,
    "Original recipe makes approximately 12 L."
)

add(
    "YUZU GARLIC SAUCE", SAUCE,
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
    Whisk in cornstarch slurry slowly and continue boiling for one minute.
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
    """,
    "Brisket quantity is not specified in the original recipe."
)

add(
    "CHICKEN BATTER", MAIN,
    """
    All Purpose Flour|205|g;
    Soy Sauce|10|g;
    Salt|3|g;
    Club Soda|1|can
    """,
    "Whisk all ingredients together until no lumps remain.",
    "The original does not specify the volume of the club soda can."
)

add(
    "CHICKEN BRINE", MAIN,
    """
    Water|2000|g;
    Soy Sauce|100|g;
    Salt|50|g;
    Sugar|20|g;
    Garlic (Crushed)|15|g;
    Ginger (Crushed)|15|g
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
    Preheat combi oven to steam at 212°F.~
    Put one layer of eggs on a perforated hotel pan.~
    Steam eggs for eight minutes.~
    Immediately shock eggs in cold running water until cool, then peel.~
    Combine marinade ingredients, bring to a boil and let cool.~
    Place peeled eggs into cold marinade and leave overnight.
    """,
    "Original notes: Use a 5.7 L Cambro for the base batch."
)

add(
    "GARLIC SHRIMP", MAIN,
    """
    Green Onion|200|g;
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
    Salt|?|10-15 g to taste (base batch);
    Dashida / Mushroom Powder|10|g;
    Sesame Oil|?|to taste;
    Dashi|?|1.5-2 L (base batch)
    """,
    "",
    "Original method not provided. Salt and dashi are ranges, "
    "so these quantities are displayed without automatic scaling."
)

add(
    "MISO MARINADE", MAIN,
    """
    Miso|1000|g;
    Sugar|600|g;
    Water|400|g;
    Mirin|200|g;
    Soy|150|g
    """,
    "Whisk all ingredients together."
)

add(
    "MISO SOUP", MAIN,
    """
    Miso|?|not provided;
    Water|?|not provided
    """,
    "",
    "INCOMPLETE RECIPE: The original has no measurements "
    "or preparation method. Do not use until completed."
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
    Depending on size, cut into thirds or quarters to fit vacuum bags.~
    Mix together mirin and sesame oil.~
    In a separate bowl, mix salt and sugar.~
    Rub pork belly with mirin and sesame oil first.~
    Generously rub with salt and sugar mixture.~
    Put each cut slab in a vacuum bag with ginger and garlic.~
    Vacuum seal.~
    Sous vide at 80°C for eight hours or 75°C for eleven hours.
    """,
    "Original lists ginger and garlic per vacuum bag. "
    "Quantities may need to be adjusted to the number of bags."
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
    Discard starchy water regularly, with at least three washes.~
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
    Discard starchy water regularly, with at least three washes.~
    Completely drain before putting rice in the rice cooker.~
    Add water and cook.
    """,
    "Original provides white-rice and brown-rice ratios. "
    "These should be treated as separate alternatives."
)

add(
    "TOFU MARINADE", MAIN,
    """
    Miso Bean Paste|300|g;
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
    Marinate tofu for at least one hour before use.
    """,
    "REVIEW REQUIRED: The original lists 'Tofu 70 g' and "
    "'Marinate 30 g'. Confirm what these entries represent."
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
    Steam bean sprouts in Rational for two minutes at 211°F.~
    Strain bean sprouts and shock in ice water until cool.~
    In a separate bowl, mix fish sauce, garlic and sesame oil.~
    Add bean sprouts and mix thoroughly.~
    Check daily and adjust salt.
    """,
    "Base uses the original 5,000 g bean sprout version "
    "(approximately 7 L). Original also contains a 9,000 g "
    "version with different ingredient ratios. Review before use."
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
    Cut chives into two-inch pieces.~
    Combine all ingredients except chives into a paste.~
    Massage paste into chives.~
    Leave at room temperature or a warm spot for two hours to ferment.~
    Refrigerate; original says store up to two weeks.
    """,
    "Food-safety review required for fermentation and storage instructions."
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
    Mix together sliced kimchi and cabbage.
    """,
    "Original marks these quantities X20 and approximately "
    "40 L. Treat this as the recorded base recipe, not X1."
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
    "Original contains X1, X4 and X8 variants with slightly "
    "different ratios. Multipliers here use the X1 recipe."
)

add(
    "PICKLED JALAPENO", SALAD,
    """
    Jalapeno|1800|g;
    Sugar|500|g;
    Tamari|500|g;
    Water|500|g;
    White Vinegar|500|g;
    Salt|20|g;
    Garlic Cloves|10|pcs
    """,
    """
    REVIEW REQUIRED: The method in the original refers to "
    "carrots, onion and ginger rather than the listed jalapeno "
    "ingredients. Confirm the correct procedure.
    """,
    "DO NOT USE without confirming preparation instructions."
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
    Steam broccoli in oven at 212°F for three minutes.~
    Cool in water bath.~
    Strain well and season broccoli.
    """,
    "Original notes: Approximately four heads of broccoli."
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
    Whisk wasabi and vinegar together until dissolved.~
    Pour liquid over cucumbers and cure overnight.~
    Rotate cucumbers for the next two days as wasabi powder sinks.
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


def go_back():
    st.session_state.recipe = None
    st.session_state.multiplier = 1


def format_amount(amount, unit, multiplier):
    if amount == "?":
        return unit

    result = Decimal(amount) * Decimal(str(multiplier))

    if result == result.to_integral_value():
        number = f"{int(result):,}"
    else:
        number = f"{result:,.3f}".rstrip("0").rstrip(".")

    return f"{number} {unit}"


# ==========================================================
# STYLING
# ==========================================================

st.markdown("""
<style>

/* Medium-bold fonts throughout the app */
.stApp,
.stApp * {
    font-weight: 600 !important;
}
/* General layout */
.stApp {
    background: #f7f7f7;
    color: #111111;
}
/* Make RESET and all multiplier buttons identical */
div[class*="st-key-reset_multiplier"] button,
div[class*="st-key-mult_"] button {
    width: 100% !important;
    min-width: 0 !important;
    max-width: none !important;

    height: 72px !important;
    min-height: 72px !important;
    max-height: 72px !important;

    padding: 2px !important;
    margin: 0 !important;

    border: 4px solid #a4a4a4;
    border-radius: 7px;

    font-size: 14px !important;
    line-height: 1.1 !important;
    white-space: pre-line !important;
    text-align: center !important;
}

/* Let RESET text wrap onto two lines */
div[class*="st-key-reset_multiplier"] button p {
    white-space: pre-line !important;
    overflow-wrap: normal !important;
}
/* RESET button: match multiplier button dimensions */
div[class*="st-key-reset_multiplier"] button {
    width: 100% !important;
    height: 72px !important;
    min-height: 72px !important;
    max-width: none !important;
    padding: 4px 1px !important;
    font-size: 14px !important;
    line-height: 1.1 !important;
    white-space: pre-line !important;
    text-align: center !important;
    border-width: 4px !important;
}
/* Square RESET 1X button */
div[class*="st-key-reset_multiplier"] button {
    width: 85px !important;
    height: 85px !important;
    min-height: 85px !important;
    padding: 5px !important;
    font-size: 24px !important;
    line-height: 1.2 !important;
    white-space: pre-line !important;
    text-align: center !important;
}

.block-container {
    max-width: 1500px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

/* Hide unnecessary Streamlit interface elements */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Brand logo */
.brand-logo {
    text-align: center;
    font-family: Arial, Helvetica, sans-serif;
    font-size: clamp(42px, 5vw, 72px);
    font-weight: 800;
    letter-spacing: -3px;
    color: #ed2227;
    margin: 4px 0 28px 0;
}

/* All main buttons */
.stButton > button {
    width: 100%;
    min-height: 95px;
    padding: 12px 7px;

    background:
        linear-gradient(
            to bottom,
            #ffaaaa 0%,
            #ff5555 7%,
            #ed2227 16%,
            #ed2227 82%,
            #d7080d 100%
        );

    color: white !important;

    border: 6px solid #a4a4a4;
    border-radius: 7px;

    box-shadow:
        0 3px 1px rgba(0,0,0,0.16),
        inset 0 2px 2px rgba(255,255,255,0.45);

    font-family: Arial, Helvetica, sans-serif;
    font-size: clamp(15px, 2.1vw, 29px);
    font-weight: 800;
    line-height: 1.1;
    text-transform: uppercase;
    white-space: normal;

    transition: border-color 0.1s ease;
}

/* Prevent default hover colors */
.stButton > button:hover,
.stButton > button:focus,
.stButton > button:active {
    color: white !important;
    background:
        linear-gradient(
            to bottom,
            #ffaaaa 0%,
            #ff5555 7%,
            #ed2227 16%,
            #ed2227 82%,
            #d7080d 100%
        ) !important;
}

/* Category buttons */
div[class*="st-key-cat_"] button {
    min-height: 72px;
    height: 72px;
    font-size: clamp(18px, 2.5vw, 37px);
}

/* Recipe selection buttons */
div[class*="st-key-recipe_"] button {
    min-height: 105px;
}

/* Multiplier buttons */
div[class*="st-key-mult_"] button {
    min-height: 72px;
    padding: 4px 1px;
    border-width: 4px;
    font-size: clamp(12px, 1.6vw, 23px);
}

/* Back/reset buttons */
div[class*="st-key-back_"] button,
div[class*="st-key-reset_"] button {
    min-height: 48px;
    max-width: 240px;
    font-size: 15px;
}

/* Recipe panel */
.recipe-title {
    font-size: clamp(28px, 3vw, 42px);
    font-weight: 850;
    margin: 0 0 15px 0;
    text-transform: uppercase;
}

.section-title {
    font-size: clamp(22px, 2.5vw, 32px);
    font-weight: 850;
    margin: 5px 0 20px 0;
    text-transform: uppercase;
}

.recipe-banner {
    background: #ed2227;
    border: 6px solid #aaa;
    border-radius: 6px;
    text-align: center;
    padding: 17px 10px;
    color: white;
    font-size: clamp(24px, 3vw, 43px);
    font-weight: 800;
    margin-bottom: 22px;
}

.ingredient-row {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    border-bottom: 1px solid #dddddd;
    padding: 10px 0;
    font-size: clamp(16px, 1.9vw, 24px);
}

.ingredient-name {
    font-weight: 650;
    overflow-wrap: anywhere;
}

.ingredient-amount {
    font-weight: 800;
    text-align: right;
    white-space: nowrap;
}

.step-block {
    margin-bottom: 22px;
    font-size: clamp(17px, 1.9vw, 24px);
    line-height: 1.4;
}

.step-number {
    font-weight: 850;
    margin-bottom: 5px;
}

.vertical-divider {
    border-left: 5px solid #ed2227;
    padding-left: 24px;
}

.batch-label {
    text-align: center;
    color: #555555;
    font-size: 18px;
    font-weight: 750;
    margin-bottom: 12px;
}

/* Password field */
.stTextInput input {
    font-size: 20px;
}

/* Smaller screen adjustments */
@media (max-width: 900px) {

    .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }

    div[class*="st-key-cat_"] button {
    min-height: 54px;
    height: 54px;
    }

    div[class*="st-key-recipe_"] button {
        min-height: 88px;
    }

    div[class*="st-key-mult_"] button {
        min-height: 65px;
    }

    .vertical-divider {
        padding-left: 12px;
        border-left-width: 3px;
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
            border-color: #4af000 !important;
            box-shadow:
                0 0 0 2px #4af000,
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
        unsafe_allow_html=True
    )

    st.markdown("### STAFF RECIPE BOOK")
    st.write("Enter the staff password to access recipes.")

    try:
        correct_password = st.secrets["STAFF_PASSWORD"]
    except Exception:
        st.error(
            "Staff password has not been configured. "
            "Set STAFF_PASSWORD in Streamlit Secrets."
        )
        st.stop()

    with st.form("login_form"):
        entered = st.text_input(
            "Staff password",
            type="password"
        )

        submit = st.form_submit_button("LOG IN")

    if submit:
        if hmac.compare_digest(
            entered,
            str(correct_password)
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
    unsafe_allow_html=True
)

# ==========================================================
# LOGO + BACK BUTTON
# ==========================================================

top_left, top_center, top_right = st.columns([1, 2, 1])

with top_left:
    if st.session_state.recipe is not None:
        st.button(
            "← BACK TO RECIPES",
            key="back_to_recipes",
            on_click=go_back,
            use_container_width=True,
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

    # Display 4 recipe buttons per row
    for start in range(0, len(recipes), 4):
        row = st.columns(4, gap="medium")

        for index, name in enumerate(recipes[start:start + 4]):
            with row[index]:
                st.button(
                    name,
                    key=f"recipe_{start + index}",
                    use_container_width=True,
                    on_click=select_recipe,
                    args=(name,),
                )

        st.write("")

    # Stop here until a recipe is selected
    st.stop()


# ==========================================================
# RECIPE DETAIL PAGE
# ==========================================================

recipe_name = st.session_state.recipe
recipe = RECIPES[recipe_name]

st.write("")


# ==========================================================
# MULTIPLIER BUTTONS
# ==========================================================

st.markdown(
    '<div class="batch-label">SELECT BATCH MULTIPLIER</div>',
    unsafe_allow_html=True,
)
# 13 equally sized buttons in one row
with st.container(key="multiplier_row"):
    multiplier_columns = st.columns(13, gap="small")

    with multiplier_columns[0]:
        st.button(
            "RESET\n1X",
            key="reset_multiplier",
            use_container_width=True,
            on_click=select_multiplier,
            args=(1,),
        )

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

st.write("")

factor = st.session_state.multiplier

st.markdown(
    f"""
    <div class="batch-label">
        CURRENT BATCH: {factor:g}X
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# INGREDIENTS + PREPARATION STEPS
# ==========================================================

left, right = st.columns([1, 1], gap="large")

with left:

    st.markdown(
        '<div class="section-title">RECIPE NAME:</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="recipe-banner">{recipe_name}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### INGREDIENTS")

    for ingredient in recipe["ingredients"]:

        quantity = format_amount(
            ingredient["amount"],
            ingredient["unit"],
            factor,
        )

        st.markdown(
            f"""
            <div class="ingredient-row">
                <span class="ingredient-name">
                    {ingredient["name"]}
                </span>
                <span class="ingredient-amount">
                    {quantity}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )


with right:

    st.markdown(
        '<div class="section-title">PREPARATION STEPS:</div>',
        unsafe_allow_html=True,
    )

    if recipe["steps"]:

        for index, step in enumerate(recipe["steps"], 1):

            st.markdown(
                f"""
                <div class="step-block">
                    <div class="step-number">
                        STEP #{index}:
                    </div>
                    <div>{step}</div>
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
    st.warning(recipe["notes"])


# ==========================================================
# LOG OUT
# ==========================================================

st.divider()

if st.button("LOG OUT", key="logout"):
    st.session_state.authenticated = False
    st.session_state.recipe = None
    st.session_state.multiplier = 1
    st.rerun()
