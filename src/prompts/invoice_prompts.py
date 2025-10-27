BULK_CATEGORY_PROMPT = (
    "Classify the following purchase items into one of these categories: {tags}.\n"
    "Items: \"{items}\"\n"
    "Return a dictionary mapping each item to its category."
    "Example output: {{\"item1\": \"category1\", \"item2\": \"category2\"}}"
    "Always return valid JSON ready to be parsed, without any markdown or other text around it."
)
ESSENTIALITY_PROMPT = (
    "On a scale from 0 to 10, rate how essential the purchase was. "
    "0 = not essential, 10 = very essential.\n"
    "Items: \"{items}\""
    "Guidelines:\n"
    "- If the item is unknown or unfamiliar, assign a lower essentiality.\n"
    "- If the item is food, consider if it is highly processed, expensive, or a luxury item when assigning essentiality.\n"
    "- Always return only a single number between 0 and 10.\n"
    "Do not return any additional text or explanations."
)