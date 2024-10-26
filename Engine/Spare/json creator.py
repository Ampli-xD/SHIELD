import json
from pathlib import Path


def create_empty_category_files():
    # Create CategoryBags directory if it doesn't exist
    category_dir = Path("../VectorHandler/CategoryBags")
    category_dir.mkdir(exist_ok=True)

    # List of categories
    categories = [
        "sexually_explicit_material",
        "violence_and_terrorism",
        "self_harm_and_suicide",
        "child_abuse_and_exploitation",
        "racial_slurs",
        "hate_speeches",
        "substance_abuse",
        "body_shaming",
        "homophobic_content",
        "transphobic_content",
        "sexist_content",
        "harassment",
        "cyberbullying",
        "misinformation_and_fake_news",
        "invasive_privacy_violation"
    ]

    # Create JSON files with empty arrays
    for category in categories:
        file_path = category_dir / f"{category}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=4)
        print(f"Created {category}.json")

    print(f"\nCreated {len(categories)} empty category files in {category_dir}")


if __name__ == "__main__":
    create_empty_category_files()
