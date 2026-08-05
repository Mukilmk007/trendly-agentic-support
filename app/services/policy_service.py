from pathlib import Path


class PolicyService:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

        # Complete markdown
        self.policy_text = ""

        # Parsed sections
        self.policy_sections = {}

    def load_policy(self):
        """Load the markdown policy file."""

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.policy_text = file.read()

        except FileNotFoundError:
            raise FileNotFoundError(
                f"Policy file not found: {self.file_path}"
            )

    def parse_sections(self):
        """
        Parse the markdown into sections.

        We never modify the content.
        We only organize it.
        """

        section_map = {
            "Shipping": "shipping",
            "Returns": "returns",
            "Refunds": "refunds",
            "Exchanges": "exchanges",
            "Return pickup": "return_pickup",
            "Damaged or wrong items": "damaged_or_wrong_items",
            "What the assistant must not do": "assistant_restrictions",
        }

        current_key = None
        buffer = []

        for line in self.policy_text.splitlines():

            line = line.rstrip()

            if line.startswith("## "):

                # Save previous section
                if current_key:
                    self.policy_sections[current_key] = "\n".join(buffer).strip()

                buffer = []

                heading = line.replace("## ", "")
                heading = heading.split(".", 1)[-1].strip()

                current_key = section_map.get(heading)

                if current_key:
                    buffer.append(line)

            else:
                if current_key:
                    buffer.append(line)

        if current_key:
            self.policy_sections[current_key] = "\n".join(buffer).strip()

    def initialize(self):
        """Load and parse the policy."""

        self.load_policy()
        self.parse_sections()

    def get_section(self, section_name: str):
        """Return a section exactly as stored."""

        return self.policy_sections.get(section_name)

    def has_section(self, section_name: str):
        """Check whether a section exists."""

        return section_name in self.policy_sections

    def list_sections(self):
        """Return all available sections."""

        return list(self.policy_sections.keys())