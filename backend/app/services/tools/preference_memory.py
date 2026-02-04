"""Preference memory tool for storing and retrieving user preferences."""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.user import User, UserPreference
from app.models.base import get_db
import uuid


class PreferenceMemoryTool:
    """Tool for managing user preferences (structured memory)."""
    
    def get_preference(self, user_id: str, key: str, db: Session) -> Optional[str]:
        """
        Get a user preference by key.
        
        Args:
            user_id: User ID
            key: Preference key
            db: Database session
            
        Returns:
            Preference value or None
        """
        try:
            preference = db.query(UserPreference).filter(
                UserPreference.user_id == uuid.UUID(user_id),
                UserPreference.key == key
            ).first()
            
            return preference.value if preference else None
            
        except Exception as e:
            print(f"Error getting preference: {e}")
            return None
    
    def get_all_preferences(self, user_id: str, db: Session) -> Dict[str, str]:
        """
        Get all user preferences.
        
        Args:
            user_id: User ID
            db: Database session
            
        Returns:
            Dictionary of all preferences
        """
        try:
            preferences = db.query(UserPreference).filter(
                UserPreference.user_id == uuid.UUID(user_id)
            ).all()
            
            return {pref.key: pref.value for pref in preferences}
            
        except Exception as e:
            print(f"Error getting all preferences: {e}")
            return {}
    
    def save_preference(self, user_id: str, key: str, value: str, db: Session) -> bool:
        """
        Save or update a user preference.
        
        Args:
            user_id: User ID
            key: Preference key
            value: Preference value
            db: Database session
            
        Returns:
            True if successful
        """
        try:
            # Check if preference exists
            preference = db.query(UserPreference).filter(
                UserPreference.user_id == uuid.UUID(user_id),
                UserPreference.key == key
            ).first()
            
            if preference:
                # Update existing
                preference.value = value
            else:
                # Create new
                preference = UserPreference(
                    user_id=uuid.UUID(user_id),
                    key=key,
                    value=value
                )
                db.add(preference)
            
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            print(f"Error saving preference: {e}")
            return False
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """Get tool definition for Claude function calling."""
        return {
            "name": "get_preference",
            "description": "Retrieve a stored user preference or personal information. Use this to recall information the user has previously shared about themselves.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "The preference key to retrieve (e.g., 'name', 'profession', 'location', 'interests')"
                    }
                },
                "required": ["key"]
            }
        }
    
    def get_save_tool_definition(self) -> Dict[str, Any]:
        """Get tool definition for saving preferences."""
        return {
            "name": "save_preference",
            "description": "Save or update a user preference or personal information. Use this when the user explicitly shares information about themselves that should be remembered for future conversations.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "The preference key (e.g., 'name', 'profession', 'location', 'interests')"
                    },
                    "value": {
                        "type": "string",
                        "description": "The preference value to store"
                    }
                },
                "required": ["key", "value"]
            }
        }

