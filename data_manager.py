"""
Data Manager Module for SINTA Cluster Predictor

This module manages data persistence and provides utility functions for
handling SINTA score calculations and data validation.
"""

import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional


class SintaDataManager:
    """
    Manages data persistence for the SINTA cluster predictor application.
    Handles data storage, retrieval, and validation.
    """
    
    def __init__(self):
        """Initialize the data manager and ensure session state is set up."""
        self._ensure_session_state()
        
    def _ensure_session_state(self):
        """Ensure required session state variables are initialized."""
        if "SINTA_DB" not in st.session_state:
            st.session_state["SINTA_DB"] = {}
            
        if "default_values" not in st.session_state:
            # Default values based on UPN Veteran Yogyakarta SINTA data
            st.session_state["default_values"] = {
                # Publication defaults - based on UPN Veteran Yogyakarta data from SINTA
                "AI1": 0.136, "AI2": 0.159, "AI3": 0.147, "AI4": 0.075, "AI5": 0.040,
                "AI6": 0.504, "AI7": 14.204, "AI8": 1.153, "AN1": 0.007, "AN2": 0.169,  # Updated citations to 14,204 and cited docs to 1,153
                "AN3": 0.204, "AN4": 0.464, "AN5": 0.312, "AN6": 0.012, "AN8": 0.104,  # Using scaled values based on 613 authors
                "AN9": 0.000, "DGS2": 166.41, "B1": 0.070, "B2": 0.415, "B3": 0.069,  # Updated Google Scholar citation per lecturer to 166.41

                # Research defaults - based on UPN Veteran Yogyakarta data from SINTA
                "P1": 0.0, "P2": 0.0, "P3": 51.0, "P4": 25.0, "P5": 523.0, "P6": 32.0, "P7": 37077.71,

                # Abdimas defaults - based on UPN Veteran Yogyakarta data
                "PM1": 0.0, "PM2": 0.0, "PM3": 9.0, "PM4": 0.0, "PM5": 96.0, "PM6": 8.0, "PM7": 3351.79,

                # HKI defaults - based on UPN Veteran Yogyakarta data
                "KI1": 0.0, "KI2": 0.015, "KI3": 0.005, "KI4": 0.0, "KI5": 0.0, "KI6": 0.0,
                "KI7": 0.0, "KI8": 0.003, "KI9": 0.409, "KI10": 0.0,

                # SDM defaults - based on UPN Veteran Yogyakarta data (613 total authors)
                "R1": 0.0, "R2": 0.0, "R3": 0.0, "DOS1": 0.024, "DOS2": 0.178, "DOS3": 0.481,
                "DOS4": 0.242, "DOS5": 0.076,

                # Kelembagaan defaults - based on UPN Veteran Yogyakarta data (35 departments, 16 journals)
                "APS1": 0.514, "APS2": 0.343, "APS3": 0.114, "APS4": 0.029, "JO1": 0.0, "JO2": 2.0,
                "JO3": 2.0, "JO4": 10.0, "JO5": 2.0, "JO6": 0.0
            }
        
        # Initialize with default values if DB is empty
        if not st.session_state["SINTA_DB"]:
            st.session_state["SINTA_DB"] = st.session_state["default_values"].copy()
    
    def get_value(self, key: str, default: float = 0.0) -> float:
        """Get a value from the data store."""
        return st.session_state["SINTA_DB"].get(key, default)
    
    def set_value(self, key: str, value: Any):
        """Set a value in the data store."""
        st.session_state["SINTA_DB"][key] = value
    
    def get_all_values(self) -> Dict[str, Any]:
        """Get all values from the data store."""
        return st.session_state["SINTA_DB"].copy()
    
    def reset_data(self):
        """Reset all data to default values."""
        st.session_state["SINTA_DB"] = st.session_state["default_values"].copy()
    
    def save_to_file(self, filename: str = None) -> bool:
        """
        Save current data to a JSON file.
        
        Args:
            filename: Optional filename to save to. If None, uses a timestamped name.
        
        Returns:
            True if successful, False otherwise.
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"sinta_data_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(st.session_state["SINTA_DB"], f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            st.error(f"Error saving data: {e}")
            return False
    
    def load_from_file(self, filename: str) -> bool:
        """
        Load data from a JSON file.
        
        Args:
            filename: Path to the JSON file to load.
        
        Returns:
            True if successful, False otherwise.
        """
        try:
            if not os.path.exists(filename):
                st.error(f"File not found: {filename}")
                return False
            
            with open(filename, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
            
            # Update the session state while preserving structure
            st.session_state["SINTA_DB"].update(loaded_data)
            return True
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return False
    
    def validate_data(self) -> Dict[str, str]:
        """
        Validate the current data and return any issues found.
        
        Returns:
            Dictionary with field names as keys and error messages as values.
        """
        errors = {}
        
        # Ensure all required fields exist
        required_fields = list(st.session_state["default_values"].keys())
        for field in required_fields:
            if field not in st.session_state["SINTA_DB"]:
                errors[field] = f"Missing field: {field}"
        
        # Validate that all values are numeric and non-negative
        for key, value in st.session_state["SINTA_DB"].items():
            try:
                num_value = float(value)
                if num_value < 0:
                    errors[key] = f"Value must be non-negative: {key} = {value}"
            except (ValueError, TypeError):
                errors[key] = f"Value must be numeric: {key} = {value}"
        
        return errors
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current data state.
        
        Returns:
            Dictionary with summary information.
        """
        data = st.session_state["SINTA_DB"]
        return {
            "total_fields": len(data),
            "non_zero_fields": len([k for k, v in data.items() if float(v) > 0]),
            "last_modified": datetime.now().isoformat(),
            "total_value": sum(float(v) for v in data.values() if isinstance(v, (int, float, str)) and str(v).replace('.', '').replace('-', '').isdigit())
        }


# Global instance of the data manager
data_manager = SintaDataManager()


def get_data_manager() -> SintaDataManager:
    """Get the global data manager instance."""
    return data_manager


def get_val(key: str, default: float = 0.0) -> float:
    """Convenience function to get a value from the data store."""
    return data_manager.get_value(key, default)


def set_val(key: str, value: Any):
    """Convenience function to set a value in the data store."""
    data_manager.set_value(key, value)


def reset_sinta_data():
    """Reset all SINTA data to default values."""
    data_manager.reset_data()


def validate_sinta_data() -> bool:
    """Validate current SINTA data and show errors if any."""
    errors = data_manager.validate_data()
    if errors:
        st.error("Validation errors found:")
        for field, error in errors.items():
            st.error(f"- {error}")
        return False
    return True