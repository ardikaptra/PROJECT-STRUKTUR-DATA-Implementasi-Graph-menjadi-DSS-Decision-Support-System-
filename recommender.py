# ==========================================================
# recommender.py
# DSS Beach Club Bali
# Multi Criteria Decision Making
# ==========================================================

import pandas as pd


class BeachClubRecommender:

    def __init__(self, dataframe):

        self.df = dataframe.copy()

    # ======================================================
    # NORMALIZATION
    # ======================================================

    def normalize_column(self, column):

        min_value = self.df[column].min()
        max_value = self.df[column].max()

        if max_value == min_value:
            return 1

        return (
            (self.df[column] - min_value)
            /
            (max_value - min_value)
        )

    # ======================================================
    # DSS SCORING
    # ======================================================

    def calculate_scores(
        self,
        weight_rating=0.4,
        weight_popularity=0.3,
        weight_facility=0.2,
        weight_price=0.1
    ):

        result = self.df.copy()

        # ==========================
        # BENEFIT CRITERIA
        # semakin besar semakin baik
        # ==========================

        result["rating_norm"] = self.normalize_column(
            "Rating"
        )

        result["popularity_norm"] = self.normalize_column(
            "Popularitas"
        )

        result["facility_norm"] = self.normalize_column(
            "Fasilitas"
        )

        # ==========================
        # COST CRITERIA
        # semakin murah semakin baik
        # ==========================

        price_norm = self.normalize_column(
            "Harga"
        )

        result["price_norm"] = 1 - price_norm

        # ==========================
        # FINAL SCORE
        # ==========================

        result["Score"] = (

            result["rating_norm"]
            * weight_rating

            +

            result["popularity_norm"]
            * weight_popularity

            +

            result["facility_norm"]
            * weight_facility

            +

            result["price_norm"]
            * weight_price

        )

        result = result.sort_values(
            by="Score",
            ascending=False
        )

        result = result.reset_index(
            drop=True
        )

        return result

    # ======================================================
    # TOP RECOMMENDATION
    # ======================================================

    def get_best_recommendation(
        self,
        weight_rating=0.4,
        weight_popularity=0.3,
        weight_facility=0.2,
        weight_price=0.1
    ):

        ranked = self.calculate_scores(
            weight_rating,
            weight_popularity,
            weight_facility,
            weight_price
        )

        return ranked.iloc[0]

    # ======================================================
    # TOP N
    # ======================================================

    def top_n(
        self,
        n=5,
        weight_rating=0.4,
        weight_popularity=0.3,
        weight_facility=0.2,
        weight_price=0.1
    ):

        ranked = self.calculate_scores(
            weight_rating,
            weight_popularity,
            weight_facility,
            weight_price
        )

        return ranked.head(n)

    # ======================================================
    # FILTER BY LOCATION
    # ======================================================

    def filter_location(
        self,
        location
    ):

        filtered = self.df[
            self.df["Lokasi"] == location
        ]

        return filtered

    # ======================================================
    # FILTER BY PRICE
    # ======================================================

    def filter_price(
        self,
        max_price
    ):

        filtered = self.df[
            self.df["Harga"] <= max_price
        ]

        return filtered
