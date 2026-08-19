import pandas as pd

from src.cleaning import clean_patients

# Every test measures age against this fixed date. If we let clean_patients
# use its default (pd.Timestamp.now()) the expected values would change every
# day and the tests would eventually start failing on their own.
AS_OF = pd.Timestamp("2026-01-01")


def make_patients(birthdates):

    return pd.DataFrame(
        {
            "BIRTHDATE": birthdates,
            "DEATHDATE": [None] * len(birthdates),
        }
    )


def test_age_accounts_for_leap_years():

    patients = make_patients(
        ["1936-01-01"]
    )

    result = clean_patients(patients, reference_date=AS_OF)

    assert result.loc[0, "age"] == 90.0  # 90.1 if you divide by 365

