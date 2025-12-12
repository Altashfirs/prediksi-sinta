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
            # Default values based on actual UPN Veteran Yogyakarta SINTA data from sinta_metrics_cluster_full.json
            st.session_state["default_values"] = {
                # Publication defaults - based on actual UPN Veteran Yogyakarta SINTA data
                "AI1": 0.092, "AI2": 0.076, "AI3": 0.139, "AI4": 0.034, "AI5": 0.034,  # Q1-Q4, Non-Q, Non Journal Int
                "AI6": 0.151, "AI7": 343.01, "AI8": 0.349, # International citations and cited docs
                "AN1": 0.021, "AN2": 0.202, "AN3": 0.441, "AN4": 2.366, "AN5": 2.294, "AN6": 0.122, # National journal ranks 1-6
                "AN7": 1.483, "AN8": 0.013, "AN9": 0.0, "AN10": 0.0, # Non-accredited, proceedings, national citations
                "DGS1": 22.092, "DGS2": 2.426, "DGS3": 9.828, # Google Scholar metrics
                "B1": 0.202, "B2": 0.622, "B3": 0.025, # Books metrics

                # Research defaults - based on actual UPN Veteran Yogyakarta SINTA data
                "P1": 0.0, "P2": 0.0, "P3": 18.0, "P4": 7.0, "P5": 486.0, "P6": 10.0, "P7": 2523.96,  # Research metrics

                # Abdimas defaults - based on actual UPN Veteran Yogyakarta SINTA data
                "PM1": 0.0, "PM2": 0.0, "PM3": 6.0, "PM4": 3.0, "PM5": 476.0, "PM6": 13.0, "PM7": 793.35,  # Community service metrics

                # HKI defaults - based on actual UPN Veteran Yogyakarta SINTA data
                "KI1": 0.0, "KI2": 0.0, "KI3": 0.004, "KI4": 0.0, "KI5": 0.0, "KI6": 0.0,
                "KI7": 0.004, "KI8": 0.143, "KI9": 6.0, "KI10": 0.0,  # IPR metrics

                # SDM defaults - based on actual UPN Veteran Yogyakarta SINTA data (613 total authors)
                "R1": 0.0, "R2": 0.0, "R3": 0.0, "DOS1": 0.004, "DOS2": 0.054, "DOS3": 0.43,
                "DOS4": 0.318, "DOS5": 0.193, "REV1": 0.0,  # Staff and reviewer metrics

                # Kelembagaan defaults - based on actual UPN Veteran Yogyakarta SINTA data (35 departments)
                "APS1": 0.0, "APS2": 0.833, "APS3": 0.167, "APS4": 0.0,  # Accreditation program metrics
                "JO1": 0.0, "JO2": 0.0, "JO3": 0.0, "JO4": 4.0, "JO5": 9.0, "JO6": 1.0  # Journal accreditation metrics
            }

        # Initialize with default values if DB is empty
        if not st.session_state["SINTA_DB"]:
            st.session_state["SINTA_DB"] = st.session_state["default_values"].copy()

    def get_value(self, key: str, default: float = 0.0) -> float:
        """Get a value from the data store."""
        try:
            return float(st.session_state["SINTA_DB"].get(key, default))
        except (ValueError, TypeError):
            # If the value isn't numeric, return the default
            return float(default)

    def set_value(self, key: str, value: Any):
        """Set a value in the data store."""
        # Ensure we only store numeric values
        try:
            numeric_value = float(value)
            st.session_state["SINTA_DB"][key] = numeric_value
        except (ValueError, TypeError):
            # If it's not a valid number, store as-is but issue a warning
            st.session_state["SINTA_DB"][key] = value
            st.warning(f"Warning: Value '{value}' for key '{key}' is not numeric")

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

    def backup_current_state(self):
        """
        Create a backup of the current session state data.

        Returns:
            Backup dictionary with current data
        """
        backup = st.session_state["SINTA_DB"].copy()
        return backup

    def restore_from_backup(self, backup_data: Dict[str, Any]):
        """
        Restore data from a backup.

        Args:
            backup_data: Dictionary containing the backup data
        """
        st.session_state["SINTA_DB"] = backup_data


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


def get_sinta_db_backup():
    """Create a backup of the current SINTA data."""
    return data_manager.backup_current_state()


def restore_sinta_db(backup_data: Dict[str, Any]):
    """Restore SINTA data from a backup."""
    data_manager.restore_from_backup(backup_data)