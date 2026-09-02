import pandas as pd


def clean_patients(patients_df, reference_date=None):

    if reference_date is None:
        reference_date = pd.Timestamp.now()

    patients_df = patients_df.copy()

    patients_df["BIRTHDATE"] = pd.to_datetime(patients_df["BIRTHDATE"], errors="coerce")
    patients_df["DEATHDATE"] = pd.to_datetime(patients_df["DEATHDATE"], errors="coerce")

    patients_df["age"] = (
        (reference_date - patients_df["BIRTHDATE"]).dt.days / 365.25
    ).round(1)

    classify = [0, 18, 40, 65, float("inf")]
    labels = ["young", "adult", "middleage", "elder"]
    patients_df["age_group"] = pd.cut(
        patients_df["age"], bins=classify, labels=labels, right=False
    )

    return patients_df


def clean_encounters(encounters_df):
    encounters_df = encounters_df.copy()

    # transform dates into datetim
    encounters_df["START"] = pd.to_datetime(encounters_df["START"], errors="coerce")
    encounters_df["STOP"] = pd.to_datetime(encounters_df["STOP"], errors="coerce")

    return encounters_df
