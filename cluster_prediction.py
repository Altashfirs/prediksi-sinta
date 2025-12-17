"""
Cluster Prediction Module for SINTA Cluster Predictor

This module provides advanced cluster prediction logic based on SINTA scoring
and includes analysis functions for strategic planning.
"""

import streamlit as st
import pandas as pd
from data_manager import get_val, get_data_manager

# Ensure data manager is initialized at module level
data_manager = get_data_manager()
from typing import Tuple, Dict, List, Optional


class ClusterPredictor:
    """
    Advanced cluster prediction system that analyzes SINTA scores and 
    provides strategic recommendations for cluster advancement.
    """
    
    def __init__(self):
        """Initialize the cluster predictor with thresholds and weights."""
        # Standard SINTA cluster thresholds (these may be updated based on current regulations)
        self.cluster_thresholds = {
            "Cluster Pengembangan": (0, 29.99),
            "Cluster Utama": (30, 49.99),
            "Cluster Mandiri": (50, 69.99), 
            "Cluster B": (70, 84.99),
            "Cluster A": (85, 100)
        }
        
        # Weight distribution as per SINTA methodology
        self.component_weights = {
            "Publikasi": 0.25,  # 25%
            "Research": 0.15,   # 15%
            "Abdimas": 0.15,    # 15%
            "HKI": 0.10,        # 10%
            "SDM": 0.15,        # 15%
            "Kelembagaan": 0.15, # 15%
            "Pengabdian": 0.05  # 5% (sometimes treated separately)
        }
        
        # Normalization factors based on SINTA methodology
        self.normalization_factors = {
            "PUBLICATION": 1776.69,  # Based on SINTA methodology
            "RESEARCH": 261491.37,   # Based on SINTA methodology
            "ABDIMAS": 447937.99,    # Based on SINTA methodology
            "HKI": 14.7,             # Based on SINTA methodology
            "SDM": 2.443,            # Based on SINTA methodology
            "INSTITUTIONAL": 2181.33 # Based on SINTA methodology
        }
    
    def calculate_detailed_scores(self) -> Tuple[float, Dict[str, float]]:
        """
        Calculate detailed scores for all SINTA components with error handling.
        
        Returns:
            Tuple of (total_score, component_scores_dict)
        """
        try:
            # Calculate publication score
            pub_score = self._calculate_publication_score()
            
            # Calculate research score  
            res_score = self._calculate_research_score()
            
            # Calculate abdimas score
            abd_score = self._calculate_abdimas_score()
            
            # Calculate HKI score
            hki_score = self._calculate_hki_score()
            
            # Calculate SDM score
            sdm_score = self._calculate_sdm_score()
            
            # Calculate kelembagaan score
            kel_score = self._calculate_kelembagaan_score()
            
            # Apply weights and calculate total
            weighted_scores = {
                "Publikasi (25%)": pub_score * 0.25,
                "Research (15%)": res_score * 0.15,
                "Abdimas (15%)": abd_score * 0.15, 
                "HKI (10%)": hki_score * 0.10,
                "SDM (15%)": sdm_score * 0.15,
                "Kelembagaan (15%)": kel_score * 0.15
            }
            
            total_score = sum(weighted_scores.values())
            
            return total_score, {
                "Publikasi": pub_score,
                "Research": res_score, 
                "Abdimas": abd_score,
                "HKI": hki_score,
                "SDM": sdm_score,
                "Kelembagaan": kel_score
            }
            
        except Exception as e:
            st.error(f"Error in score calculation: {e}")
            return 0.0, {k: 0.0 for k in ["Publikasi", "Research", "Abdimas", "HKI", "SDM", "Kelembagaan"]}
    
    def _calculate_publication_score(self) -> float:
        """Calculate normalized publication score."""
        # Data from publikasi.py - UPN Veteran Yogyakarta values
        pub_data = [
            ("Intl", "AI1", "ARTIKEL JURNAL INTERNASIONAL Q1", 40, 0.136),
            ("Intl", "AI2", "ARTIKEL JURNAL INTERNASIONAL Q2", 35, 0.159),
            ("Intl", "AI3", "ARTIKEL JURNAL INTERNASIONAL Q3", 30, 0.147),
            ("Intl", "AI4", "ARTIKEL JURNAL INTERNASIONAL Q4", 25, 0.075),
            ("Intl", "AI5", "ARTIKEL JURNAL INTERNASIONAL NON Q", 20, 0.040),
            ("Intl", "AI6", "ARTIKEL NON JURNAL INTERNASIONAL", 15, 0.504),
            ("Intl", "AI7", "JUMLAH SITASI PUBLIKASI INTERNASIONAL", 1, 14.204),  # Updated to UPN's citation count (14,204) per author
            ("Intl", "AI8", "JUMLAH DOKUMEN PUBLIKASI INTERNASIONAL TERSITASI", 1, 1.153),  # Updated to UPN's cited documents (1,153) per author
            ("Nas", "AN1", "ARTIKEL JURNAL NASIONAL PERINGKAT 1", 25, 0.007),
            ("Nas", "AN2", "ARTIKEL JURNAL NASIONAL PERINGKAT 2", 20, 0.169),
            ("Nas", "AN3", "ARTIKEL JURNAL NASIONAL PERINGKAT 3", 15, 0.204),
            ("Nas", "AN4", "ARTIKEL JURNAL NASIONAL PERINGKAT 4", 10, 0.464),
            ("Nas", "AN5", "ARTIKEL JURNAL NASIONAL PERINGKAT 5", 5, 0.312),
            ("Nas", "AN6", "ARTIKEL JURNAL NASIONAL PERINGKAT 6", 2, 0.012),
            ("Nas", "AN8", "PROSIDING NASIONAL", 2, 0.104),
            ("Nas", "AN9", "JUMLAH SITASI PUBLIKASI NASIONAL PER DOSEN", 1, 23.79),  # Updated to UPN's citation per researcher value
            ("Other", "DGS2", "GS CITATION PER LECTURER", 1, 166.41),  # Updated to UPN's GScholar citation per lecturer
            ("Other", "B1", "BUKU AJAR", 20, 0.070),
            ("Other", "B2", "BUKU REFERENSI", 40, 0.415),
            ("Other", "B3", "BUKU MONOGRAF", 20, 0.069),
        ]

        raw_score = sum([get_val(code) * weight for _, code, _, weight, _ in pub_data])
        normalized_score = (raw_score / max(raw_score, 1776.69)) * 100 if 1776.69 > 0 else 0
        return normalized_score
    
    def _calculate_research_score(self) -> float:
        """Calculate normalized research score."""
        # Data from research.py - UPN Veteran Yogyakarta values
        res_data = [
            ("P1", "JUMLAH PENELITIAN HIBAH LUAR NEGERI (KETUA)", 40, 1.0),  # Updated for UPN
            ("P2", "JUMLAH PENELITIAN HIBAH LUAR NEGERI (ANGGOTA)", 10, 2.0),  # Updated for UPN
            ("P3", "JUMLAH PENELITIAN HIBAH EKSTERNAL (KETUA)", 30, 150.0),  # Updated for UPN
            ("P4", "JUMLAH PENELITIAN HIBAH EKSTERNAL (ANGGOTA)", 10, 75.0),  # Updated for UPN
            ("P5", "JUMLAH PENELITIAN INTERNAL INSTITUSI (KETUA)", 15, 200.0),  # Updated for UPN
            ("P6", "JUMLAH PENELITIAN INTERNAL INSTITUSI (ANGGOTA)", 5, 50.0),  # Updated for UPN
            ("P7", "JUMLAH RUPIAH PENELITIAN (JUTA RUPIAH)", 0.05, 50000.0),  # Updated for UPN
        ]

        raw_score = 0
        for code, _, weight, _ in res_data:
            if code == "P7":  # Special case for funding - no "v_" prefix
                value = get_val(code)
                raw_score += value * weight
            else:
                value = get_val(f"v_{code}")
                raw_score += value * weight

        normalized_score = (raw_score / max(raw_score, 261491.37)) * 100 if 261491.37 > 0 else 0
        return normalized_score

    def _calculate_abdimas_score(self) -> float:
        """Calculate normalized abdimas score."""
        # Data from abdimas.py - UPN Veteran Yogyakarta values
        abd_data = [
            ("PM1", "JUMLAH PENGABDIAN MASYARAKAT INTERNASIONAL (KETUA)", 40, 1.0),  # Updated for UPN
            ("PM2", "JUMLAH PENGABDIAN MASYARAKAT INTERNASIONAL (ANGGOTA)", 10, 2.0),  # Updated for UPN
            ("PM3", "JUMLAH PENGABDIAN MASYARAKAT NASIONAL/EKSTERNAL (KETUA)", 30, 25.0),  # Updated for UPN
            ("PM4", "JUMLAH PENGABDIAN MASYARAKAT NASIONAL/EKSTERNAL (ANGGOTA)", 10, 10.0),  # Updated for UPN
            ("PM5", "JUMLAH PENGABDIAN MASYARAKAT LOKAL/INTERNAL INSTITUSI (KETUA)", 15, 100.0),  # Updated for UPN
            ("PM6", "JUMLAH PENGABDIAN MASYARAKAT LOKAL/INTERNAL INSTITUSI (ANGGOTA)", 5, 15.0),  # Updated for UPN
            ("PM7", "JUMLAH RUPIAH PENGABDIAN MASYARAKAT (JUTA RUPIAH)", 0.05, 5000.0),  # Updated for UPN
        ]

        raw_score = 0
        for code, _, weight, _ in abd_data:
            if code == "PM7":  # Special case for funding - no "v_" prefix
                value = get_val(code)
                raw_score += value * weight
            else:
                value = get_val(f"v_{code}")
                raw_score += value * weight

        normalized_score = (raw_score / max(raw_score, 447937.99)) * 100 if 447937.99 > 0 else 0
        return normalized_score
    
    def _calculate_hki_score(self) -> float:
        """Calculate normalized HKI score."""
        # Data from hki.py - UPN Veteran Yogyakarta values
        hki_data = [
            ("KI1", "HKI PATEN", 40, 0.010),  # Updated for UPN
            ("KI2", "HKI PATEN SEDERHANA", 20, 0.025),  # Updated for UPN
            ("KI3", "HKI MEREK", 1, 0.010),  # Updated for UPN
            ("KI4", "HKI INDIKASI GEOGRAFIS", 10, 0.005),  # Updated for UPN
            ("KI5", "HKI DESAIN INDUSTRI", 20, 0.008),  # Updated for UPN
            ("KI6", "HKI DESAIN TATA LETAK SIRKUIT TERPADU", 20, 0.002),  # Updated for UPN
            ("KI7", "HKI RAHASIA DAGANG", 0, 0.000),  # No change (0 weight)
            ("KI8", "HKI PERLINDUNGAN VARIETAS TANAMAN", 40, 0.005),  # Updated for UPN
            ("KI9", "HKI HAK CIPTA", 1, 0.500),  # Updated for UPN
            ("KI10", "HKI SELAIN TERDAFTAR / DIBERI / DITERIMA", 1, 0.050),  # Updated for UPN
        ]

        raw_score = sum([get_val(f"v_{code}") * weight for code, _, weight, _ in hki_data])
        normalized_score = (raw_score / max(raw_score, 14.7)) * 100 if 14.7 > 0 else 0
        return normalized_score
    
    def _calculate_sdm_score(self) -> float:
        """Calculate normalized SDM score."""
        # Data from sdm.py - UPN Veteran Yogyakarta values
        sdm_data = [
            ("R1", "REVIEWER JURNAL INTERNASIONAL (ORANG)", 2, 0.0),
            ("R2", "REVIEWER JURNAL NASIONAL SINTA 1 & 2 (ORANG)", 1, 0.0),
            ("R3", "REVIEWER JURNAL NASIONAL SINTA 3 S.D. 6 (ORANG)", 0.5, 0.0),
            ("DOS1", "DOSEN PROFESSOR", 4, 0.024),
            ("DOS2", "DOSEN LEKTOR KEPALA", 3, 0.178),
            ("DOS3", "DOSEN LEKTOR", 2, 0.481),
            ("DOS4", "DOSEN ASISTEN AHLI", 1, 0.242),
            ("DOS5", "DOSEN NON JAFA", 0, 0.076),
        ]

        raw_score = sum([get_val(f"v_{code}") * weight for code, _, weight, _ in sdm_data])
        normalized_score = (raw_score / 2.443) * 100 if 2.443 > 0 else 0
        return normalized_score
    
    def _calculate_kelembagaan_score(self) -> float:
        """Calculate normalized kelembagaan score with adjustment factor."""
        # Data from kelembagaan.py
        kel_data = [
            ("Akreditasi", "APS1", "AKREDITASI PRODI A/UNGGUL/INTERNASIONAL", 40),
            ("Akreditasi", "APS2", "AKREDITASI PRODI B/BAIK SEKALI", 30),
            ("Akreditasi", "APS3", "AKREDITASI PRODI C/BAIK", 20),
            ("Akreditasi", "APS4", "AKREDITASI PRODI D/TIDAK TERAKREDITASI", 0),
            ("Jurnal", "JO1", "JUMLAH JURNAL TERAKREDITASI S1", 40),
            ("Jurnal", "JO2", "JUMLAH JURNAL TERAKREDITASI S2", 30),
            ("Jurnal", "JO3", "JUMLAH JURNAL TERAKREDITASI S3", 20),
            ("Jurnal", "JO4", "JUMLAH JURNAL TERAKREDITASI S4", 10),
            ("Jurnal", "JO5", "JUMLAH JURNAL TERAKREDITASI S5", 5),
            ("Jurnal", "JO6", "JUMLAH JURNAL TERAKREDITASI S6", 2),
        ]

        raw_score = sum([get_val(f"v_{code}") * weight for _, code, _, weight in kel_data])
        adjusted_score = raw_score * 0.30  # Apply adjustment factor
        normalized_score = (adjusted_score / max(adjusted_score, 2181.33)) * 100 if 2181.33 > 0 else 0
        return normalized_score
    
    def predict_cluster(self, score: float) -> Tuple[str, str, str]:
        """
        Predict cluster based on score.
        
        Args:
            score: The calculated SINTA score
            
        Returns:
            Tuple of (cluster_name, color, icon)
        """
        for cluster, (min_val, max_val) in self.cluster_thresholds.items():
            if min_val <= score <= max_val:
                # Assign color and icon based on cluster
                color_map = {
                    "Cluster A": "gold",
                    "Cluster B": "silver", 
                    "Cluster Mandiri": "blue",
                    "Cluster Utama": "bronze",
                    "Cluster Pengembangan": "gray"
                }
                icon_map = {
                    "Cluster A": "🏆",
                    "Cluster B": "🥈",
                    "Cluster Mandiri": "🥇",
                    "Cluster Utama": "🥉",
                    "Cluster Pengembangan": "⚠️"
                }
                return cluster, color_map.get(cluster, "gray"), icon_map.get(cluster, "❓")
        
        # Fallback
        return "Unknown", "red", "❌"
    
    def get_strategic_recommendations(self, component_scores: Dict[str, float]) -> List[str]:
        """
        Generate strategic recommendations based on component scores.
        
        Args:
            component_scores: Dictionary of component scores
            
        Returns:
            List of strategic recommendations
        """
        recommendations = []
        
        # Find the lowest scoring components
        sorted_components = sorted(component_scores.items(), key=lambda x: x[1])
        
        # Top 3 lowest scoring components need attention
        lowest_components = sorted_components[:3]
        
        for component, score in lowest_components:
            if score < 20:
                priority = "TINGGI"
                action = f"Prioritaskan pengembangan di bidang {component.lower()}. Ini adalah area kritis yang memerlukan perhatian segera."
            elif score < 50:
                priority = "SEDANG" 
                action = f"Fokuskan upaya peningkatan di bidang {component.lower()} untuk mencapai standar kompetitif."
            else:
                priority = "RENDAH"
                action = f"Bidang {component.lower()} dalam kondisi baik, pertahankan dan terus tingkatkan."
            
            recommendations.append({
                "area": component,
                "priority": priority,
                "action": action,
                "current_score": score
            })
        
        return recommendations
    
    def calculate_cluster_advancement_path(self, current_score: float) -> Dict[str, any]:
        """
        Calculate path to next cluster including required improvements.
        
        Args:
            current_score: Current SINTA score
            
        Returns:
            Dictionary with advancement path details
        """
        current_cluster, _, _ = self.predict_cluster(current_score)
        
        # Find next cluster
        next_cluster = None
        target_score = None
        
        sorted_clusters = sorted(self.cluster_thresholds.items(), 
                                key=lambda x: x[1][0])  # Sort by min threshold
        
        for cluster, (min_val, max_val) in sorted_clusters:
            if current_score < min_val:
                next_cluster = cluster
                target_score = min_val
                break
        
        if next_cluster is None:
            # Already at highest cluster
            return {
                "current_cluster": current_cluster,
                "next_cluster": "Maximum",
                "target_score": 100,
                "gap": 0,
                "message": "Anda telah mencapai cluster tertinggi!"
            }
        
        gap = target_score - current_score
        
        return {
            "current_cluster": current_cluster,
            "next_cluster": next_cluster,
            "target_score": target_score,
            "gap": gap,
            "message": f"Perlu peningkatan sebesar {gap:.2f} poin untuk mencapai {next_cluster}"
        }


# Global instance of the cluster predictor
cluster_predictor = ClusterPredictor()


def get_cluster_predictor() -> ClusterPredictor:
    """Get the global cluster predictor instance."""
    return cluster_predictor


def calculate_cluster_score() -> Tuple[float, Dict[str, float]]:
    """Convenience function to calculate cluster score."""
    return cluster_predictor.calculate_detailed_scores()


def predict_cluster_type(score: float) -> Tuple[str, str, str]:
    """Convenience function to predict cluster type."""
    return cluster_predictor.predict_cluster(score)


def get_strategic_advice(component_scores: Dict[str, float]) -> List[str]:
    """Convenience function to get strategic recommendations."""
    return cluster_predictor.get_strategic_recommendations(component_scores)


def calculate_advancement_path(current_score: float) -> Dict[str, any]:
    """Convenience function to calculate advancement path."""
    return cluster_predictor.calculate_cluster_advancement_path(current_score)