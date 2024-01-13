from enum import Enum


class MessageCategory(Enum):
    """
    Enum class representing different categories of messages.
    """

    EMAIL_CONFIRMATION = 1
    PASSWORD_RESET = 2

    @staticmethod
    def is_valid_category(category):
        """
        Check if the given category is a valid MessageCategory.

        Args:
            category (int): The category to check.

        Returns:
            bool: True if the category is valid, False otherwise.
        """
        return any(
            category == item.name for item in MessageCategory.__members__.values()
        )
