from phase0.geo import (
    auth_matches,
    auth_location_display,
    country_label,
    looks_like_place,
    split_auth_location,
)


def test_ng_and_nigeria_are_the_same_for_the_gate():
    assert country_label("NG") == "Nigeria"
    assert country_label("nigeria") == "Nigeria"
    assert auth_matches(["Nigeria"], ["NG", "ANY"])
    assert auth_matches(["NG"], ["Nigeria"])
    assert not auth_matches(["Nigeria"], ["US"])


def test_bio_is_not_a_place():
    assert not looks_like_place(
        "Results-driven IT professional, with 8 years delivering network solutions."
    )
    assert looks_like_place("Lagos, Nigeria")
    assert not looks_like_place("B.Sc Computer Science, University of Lagos, 2014")


def test_auth_location_prefers_full_country_name():
    labels, loc = split_auth_location("Lagos, Nigeria")
    assert labels == ["Nigeria"]
    assert "Lagos" in loc
    shown = auth_location_display(
        {"location": "Lagos, Nigeria", "work_authorization": ["NG"]}
    )
    assert shown == "Lagos, Nigeria"
    assert "NG" not in shown
    muddled = auth_location_display(
        {
            "location": "Results-driven IT professional, with eight years in networking.",
            "work_authorization": ["Nigeria"],
        }
    )
    assert muddled == "Nigeria"
    assert "Results-driven" not in muddled
