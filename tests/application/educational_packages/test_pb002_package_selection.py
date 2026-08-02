"""PB-002 F8 — package selection chain reaches CA-R1 / CB-R1."""

from __future__ import annotations

from app.application.educational_packages.loader import reset_educational_package_cache
from app.application.educational_packages.selection import (
    resolve_active_educational_package,
    should_suppress_topic_completed,
)


def setup_function() -> None:
    reset_educational_package_cache()


def test_alpha_chain_reaches_ca_r1() -> None:
    completed: set[str] = set()
    last = ""

    p1 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="1.1",
        completed_package_ids=completed,
        last_completed_package_id=last,
    )
    assert p1 is not None
    assert p1.package_id == "CS1-EP001-PKG-1.1-PURPOSE-FUNCTION"
    assert p1.campaign_day == "CA-D1"
    completed.add(p1.package_id)
    last = p1.package_id

    p2 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="1.2",
        completed_package_ids=completed,
        last_completed_package_id=last,
    )
    assert p2 is not None
    assert p2.package_id == "CS1-EP001-PKG-1.2-EDA-SUMMARIES"
    assert should_suppress_topic_completed(p2, completed_package_ids=completed)
    completed.add(p2.package_id)
    last = p2.package_id

    p3 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="1.2",
        completed_package_ids=completed,
        last_completed_package_id=last,
    )
    assert p3 is not None
    assert p3.package_id == "CS1-EP001-PKG-1.2-EDA-ASSOCIATION"
    assert should_suppress_topic_completed(p3, completed_package_ids=completed)
    completed.add(p3.package_id)
    last = p3.package_id

    p4 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="1.2",
        completed_package_ids=completed,
        last_completed_package_id=last,
    )
    assert p4 is not None
    assert p4.package_id == "CS1-EP001-PKG-REV-PURPOSE-EDA"
    assert p4.campaign_day == "CA-R1"
    assert p4.mode == "revision"
    assert not should_suppress_topic_completed(p4, completed_package_ids=completed)


def test_beta_chain_reaches_cb_r1() -> None:
    # Simulate Alpha terminal already done; start Beta at 2.1 discrete.
    completed = {
        "CS1-EP001-PKG-1.1-PURPOSE-FUNCTION",
        "CS1-EP001-PKG-1.2-EDA-SUMMARIES",
        "CS1-EP001-PKG-1.2-EDA-ASSOCIATION",
        "CS1-EP001-PKG-REV-PURPOSE-EDA",
    }
    last = "CS1-EP001-PKG-REV-PURPOSE-EDA"

    # CA-R1 tomorrow points at 2.1 → first uncompleted 2.1 pack
    p1 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="2.1",
        completed_package_ids=completed,
        last_completed_package_id=last,
    )
    assert p1 is not None
    assert p1.package_id == "CS1-CS1002-PKG-2.1-DISCRETE"
    completed.add(p1.package_id)
    last = p1.package_id

    p2 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="2.1",
        completed_package_ids=completed,
        last_completed_package_id=last,
    )
    assert p2 is not None
    assert p2.package_id == "CS1-CS1002-PKG-2.1-CONTINUOUS"
    assert should_suppress_topic_completed(p2, completed_package_ids=completed)
    completed.add(p2.package_id)
    last = p2.package_id

    p3 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="2.1",
        completed_package_ids=completed,
        last_completed_package_id=last,
    )
    assert p3 is not None
    assert p3.package_id == "CS1-CS1002-PKG-REV-PCA-DISTRIBUTIONS"
    assert p3.campaign_day == "CB-R1"


def test_campaign_day_parsed_on_packages() -> None:
    from app.application.educational_packages.loader import find_educational_package

    pack = find_educational_package(topic_code="1.1", subject_id="CS1")
    assert pack is not None
    assert pack.campaign_day == "CA-D1"
    rev = find_educational_package(topic_code="CA-R1", subject_id="CS1")
    assert rev is not None
    assert rev.campaign_day == "CA-R1"


def test_gamma_chain_reaches_cg_r1() -> None:
    """RO-001 — CB-R1 tomorrow_preview → CG-D1…CG-R1 joint inventory."""
    completed = {
        "CS1-EP001-PKG-1.1-PURPOSE-FUNCTION",
        "CS1-EP001-PKG-1.2-EDA-SUMMARIES",
        "CS1-EP001-PKG-1.2-EDA-ASSOCIATION",
        "CS1-EP001-PKG-REV-PURPOSE-EDA",
        "CS1-CS1002-PKG-2.1-DISCRETE",
        "CS1-CS1002-PKG-2.1-CONTINUOUS",
        "CS1-CS1002-PKG-REV-PCA-DISTRIBUTIONS",
    }
    last = "CS1-CS1002-PKG-REV-PCA-DISTRIBUTIONS"

    expected = [
        ("CS1-EP001-PKG-2.1-PROB-QUANTILES", "CG-D1"),
        ("CS1-EP001-PKG-2.1-POISSON-PROCESS", "CG-D2"),
        ("CS1-EP001-PKG-2.1-INVERSE-TRANSFORM", "CG-D3"),
        ("CS1-EP001-PKG-2.1-SOFTWARE-GENERATION", "CG-D4"),
        ("CS1-EP001-PKG-REV-DISTRIBUTIONS-GENERATION", "CG-R1"),
    ]
    for package_id, day in expected:
        pack = resolve_active_educational_package(
            subject_id="CS1",
            syllabus_topic_code="2.1",
            completed_package_ids=completed,
            last_completed_package_id=last,
        )
        assert pack is not None, f"missing successor before {day}"
        assert pack.package_id == package_id
        assert pack.campaign_day == day
        completed.add(pack.package_id)
        last = pack.package_id


def test_delta_chain_reaches_cd_r3() -> None:
    """RO-002 — Trust Front entry at 4.1 → CD-D1…CD-R3 joint inventory."""
    completed: set[str] = set()
    last = ""

    expected = [
        ("CS1-EP001-PKG-4.1-RESPONSE-EXPLANATORY", "CD-D1"),
        ("CS1-EP001-PKG-4.1-SIMPLE-MULTIPLE", "CD-D2"),
        ("CS1-EP001-PKG-4.1-LEAST-SQUARES", "CD-D3"),
        ("CS1-EP001-PKG-4.1-SOFTWARE-INFERENCE", "CD-D4"),
        ("CS1-EP001-PKG-4.1-VARIABLE-SELECTION", "CD-D5"),
        ("CS1-EP001-PKG-REV-LINEAR-MODELS", "CD-R1"),
        ("CS1-EP001-PKG-4.2-EXPONENTIAL-FAMILY", "CD-D6"),
        ("CS1-EP001-PKG-4.2-MEAN-VARIANCE", "CD-D7"),
        ("CS1-EP001-PKG-4.2-LINK-CANONICAL", "CD-D8"),
        ("CS1-EP001-PKG-4.2-FACTORS-INTERACTIONS", "CD-D9"),
        ("CS1-EP001-PKG-4.2-LINEAR-PREDICTOR", "CD-D10"),
        ("CS1-EP001-PKG-4.2-DEVIANCE-ESTIMATION", "CD-D11"),
        ("CS1-EP001-PKG-4.2-MODEL-CHOICE", "CD-D12"),
        ("CS1-EP001-PKG-4.2-RESIDUALS", "CD-D13"),
        ("CS1-EP001-PKG-4.2-GOODNESS-TESTS", "CD-D14"),
        ("CS1-EP001-PKG-4.2-FIT-INTERPRET", "CD-D15"),
        ("CS1-EP001-PKG-REV-REGRESSION-GLM", "CD-R2"),
        ("CS1-EP001-PKG-5.1-BAYES-THEOREM", "CD-D16"),
        ("CS1-EP001-PKG-5.1-PRIOR-POSTERIOR", "CD-D17"),
        ("CS1-EP001-PKG-5.1-POSTERIOR-SIMPLE", "CD-D18"),
        ("CS1-EP001-PKG-5.1-LOSS-ESTIMATORS", "CD-D19"),
        ("CS1-EP001-PKG-5.1-CREDIBLE-INTERVALS", "CD-D20"),
        ("CS1-EP001-PKG-5.1-CREDIBILITY-PREMIUM", "CD-D21"),
        ("CS1-EP001-PKG-5.1-BAYESIAN-CREDIBILITY", "CD-D22"),
        ("CS1-EP001-PKG-5.1-EMPIRICAL-BAYES", "CD-D23"),
        ("CS1-EP001-PKG-5.1-BAYES-VS-EB", "CD-D24"),
        ("CS1-EP001-PKG-REV-MIDSPINE", "CD-R3"),
    ]
    # Cold entry at mid-spine Trust Front (not Continuity Front from Gamma).
    topic = "4.1"
    for package_id, day in expected:
        pack = resolve_active_educational_package(
            subject_id="CS1",
            syllabus_topic_code=topic,
            completed_package_ids=completed,
            last_completed_package_id=last,
        )
        assert pack is not None, f"missing successor before {day}"
        assert pack.package_id == package_id, (
            f"expected {package_id} got {pack.package_id}"
        )
        assert pack.campaign_day == day
        assert pack.package_id != "CS1-EA005-PKG-4.2-GLM-STRUCTURE"
        completed.add(pack.package_id)
        last = pack.package_id
        # After first day, chain follows tomorrow_preview; keep topic for cold fallback.
        topic = pack.topic_code or topic


def test_orphan_4_2_superseded_not_selected() -> None:
    """RO-002 — EA-006 orphan must not win topic 4.2 after Delta activation."""
    from app.application.educational_packages.loader import (
        EducationalPackageLoader,
        find_package_by_id,
    )

    orphan = find_package_by_id("CS1-EA005-PKG-4.2-GLM-STRUCTURE")
    assert orphan is None

    entry = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="4.2",
        completed_package_ids=frozenset(),
        last_completed_package_id="",
    )
    assert entry is not None
    assert entry.campaign_day == "CD-D6"
    assert entry.package_id == "CS1-EP001-PKG-4.2-EXPONENTIAL-FAMILY"

    approved = EducationalPackageLoader().all_approved()
    cd = [p for p in approved if (p.campaign_day or "").startswith("CD-")]
    assert len(cd) == 27
    assert all(p.package_id != "CS1-EA005-PKG-4.2-GLM-STRUCTURE" for p in approved)


def test_epsilon_chain_reaches_ce_r1() -> None:
    """RO-003 — Continuity Front into 2.2 → CE-D1…CE-R1 joint inventory."""
    completed: set[str] = set()
    last = ""
    expected = [
        ("CS1-EP001-PKG-2.2-MARGINAL-CONDITIONAL", "CE-D1"),
        ("CS1-EP001-PKG-2.2-INDEPENDENCE", "CE-D2"),
        ("CS1-EP001-PKG-2.2-COV-CORR-EXPECTATION", "CE-D3"),
        ("CS1-EP001-PKG-2.2-LINEAR-COMBINATIONS", "CE-D4"),
        ("CS1-EP001-PKG-REV-JOINT-DISTRIBUTIONS", "CE-R1"),
    ]
    topic = "2.2"
    for package_id, day in expected:
        pack = resolve_active_educational_package(
            subject_id="CS1",
            syllabus_topic_code=topic,
            completed_package_ids=completed,
            last_completed_package_id=last,
        )
        assert pack is not None, f"missing successor before {day}"
        assert pack.package_id == package_id, (
            f"expected {package_id} got {pack.package_id}"
        )
        assert pack.campaign_day == day
        completed.add(pack.package_id)
        last = pack.package_id
        topic = pack.topic_code or topic


def test_gamma_revision_hands_off_to_epsilon() -> None:
    """RO-003 — CG-R1 tomorrow_preview 2.2 resolves to CE-D1 (not Gamma re-entry)."""
    from app.application.educational_packages.loader import EducationalPackageLoader

    gamma_ids = {
        "CS1-EP001-PKG-2.1-PROB-QUANTILES",
        "CS1-EP001-PKG-2.1-POISSON-PROCESS",
        "CS1-EP001-PKG-2.1-INVERSE-TRANSFORM",
        "CS1-EP001-PKG-2.1-SOFTWARE-GENERATION",
        "CS1-EP001-PKG-REV-DISTRIBUTIONS-GENERATION",
    }
    pack = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="2.2",
        completed_package_ids=gamma_ids,
        last_completed_package_id="CS1-EP001-PKG-REV-DISTRIBUTIONS-GENERATION",
    )
    assert pack is not None
    assert pack.campaign_day == "CE-D1"
    assert pack.package_id == "CS1-EP001-PKG-2.2-MARGINAL-CONDITIONAL"

    approved = EducationalPackageLoader().all_approved()
    ce = [p for p in approved if (p.campaign_day or "").startswith("CE-")]
    assert len(ce) == 5
    assert len(approved) == 68


def test_zeta_chain_reaches_cz_r1() -> None:
    """RO-004 — Continuity Front into 2.3 → CZ-D1…CZ-R1 joint inventory."""
    completed: set[str] = set()
    last = ""
    expected = [
        ("CS1-EP001-PKG-2.3-CONDITIONAL-EXPECTATION", "CZ-D1"),
        ("CS1-EP001-PKG-2.3-MEAN-VARIANCE-CONDITIONING", "CZ-D2"),
        ("CS1-EP001-PKG-REV-CONDITIONAL-EXPECTATIONS", "CZ-R1"),
    ]
    topic = "2.3"
    for package_id, day in expected:
        pack = resolve_active_educational_package(
            subject_id="CS1",
            syllabus_topic_code=topic,
            completed_package_ids=completed,
            last_completed_package_id=last,
        )
        assert pack is not None, f"missing successor before {day}"
        assert pack.package_id == package_id, (
            f"expected {package_id} got {pack.package_id}"
        )
        assert pack.campaign_day == day
        completed.add(pack.package_id)
        last = pack.package_id
        topic = pack.topic_code or topic


def test_epsilon_revision_hands_off_to_zeta() -> None:
    """RO-004 — CE-R1 tomorrow_preview 2.3 resolves to CZ-D1 (not Epsilon re-entry)."""
    from app.application.educational_packages.loader import EducationalPackageLoader

    epsilon_ids = {
        "CS1-EP001-PKG-2.2-MARGINAL-CONDITIONAL",
        "CS1-EP001-PKG-2.2-INDEPENDENCE",
        "CS1-EP001-PKG-2.2-COV-CORR-EXPECTATION",
        "CS1-EP001-PKG-2.2-LINEAR-COMBINATIONS",
        "CS1-EP001-PKG-REV-JOINT-DISTRIBUTIONS",
    }
    pack = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="2.3",
        completed_package_ids=epsilon_ids,
        last_completed_package_id="CS1-EP001-PKG-REV-JOINT-DISTRIBUTIONS",
    )
    assert pack is not None
    assert pack.campaign_day == "CZ-D1"
    assert pack.package_id == "CS1-EP001-PKG-2.3-CONDITIONAL-EXPECTATION"

    approved = EducationalPackageLoader().all_approved()
    cz = [p for p in approved if (p.campaign_day or "").startswith("CZ-")]
    assert len(cz) == 3
    assert len(approved) == 68


def test_eta_chain_reaches_ch_r1() -> None:
    """RO-005 — Continuity Front into 2.4 → CH-D1…CH-R1 joint inventory."""
    completed: set[str] = set()
    last = ""
    expected = [
        ("CS1-EP001-PKG-2.4-MGF-CGF", "CH-D1"),
        ("CS1-EP001-PKG-2.4-MOMENT-VIA-GF", "CH-D2"),
        ("CS1-EP001-PKG-REV-GENERATING-FUNCTIONS", "CH-R1"),
    ]
    topic = "2.4"
    for package_id, day in expected:
        pack = resolve_active_educational_package(
            subject_id="CS1",
            syllabus_topic_code=topic,
            completed_package_ids=completed,
            last_completed_package_id=last,
        )
        assert pack is not None, f"missing successor before {day}"
        assert pack.package_id == package_id, (
            f"expected {package_id} got {pack.package_id}"
        )
        assert pack.campaign_day == day
        completed.add(pack.package_id)
        last = pack.package_id
        topic = pack.topic_code or topic


def test_zeta_revision_hands_off_to_eta() -> None:
    """RO-005 — CZ-R1 tomorrow_preview 2.4 resolves to CH-D1 (not Zeta re-entry)."""
    from app.application.educational_packages.loader import EducationalPackageLoader

    zeta_ids = {
        "CS1-EP001-PKG-2.3-CONDITIONAL-EXPECTATION",
        "CS1-EP001-PKG-2.3-MEAN-VARIANCE-CONDITIONING",
        "CS1-EP001-PKG-REV-CONDITIONAL-EXPECTATIONS",
    }
    pack = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="2.4",
        completed_package_ids=zeta_ids,
        last_completed_package_id="CS1-EP001-PKG-REV-CONDITIONAL-EXPECTATIONS",
    )
    assert pack is not None
    assert pack.campaign_day == "CH-D1"
    assert pack.package_id == "CS1-EP001-PKG-2.4-MGF-CGF"

    approved = EducationalPackageLoader().all_approved()
    ch = [p for p in approved if (p.campaign_day or "").startswith("CH-")]
    assert len(ch) == 3
    assert len(approved) == 68


def test_theta_chain_reaches_ct_r1() -> None:
    """RO-006 — Continuity Front into 2.5 → CT-D1…CT-R1 joint inventory."""
    completed: set[str] = set()
    last = ""
    expected = [
        ("CS1-EP001-PKG-2.5-CLT", "CT-D1"),
        ("CS1-EP001-PKG-2.5-SIMULATED-SAMPLE-NORMAL", "CT-D2"),
        ("CS1-EP001-PKG-REV-CENTRAL-LIMIT-THEOREM", "CT-R1"),
    ]
    topic = "2.5"
    for package_id, day in expected:
        pack = resolve_active_educational_package(
            subject_id="CS1",
            syllabus_topic_code=topic,
            completed_package_ids=completed,
            last_completed_package_id=last,
        )
        assert pack is not None, f"missing successor before {day}"
        assert pack.package_id == package_id, (
            f"expected {package_id} got {pack.package_id}"
        )
        assert pack.campaign_day == day
        completed.add(pack.package_id)
        last = pack.package_id
        topic = pack.topic_code or topic


def test_eta_revision_hands_off_to_theta() -> None:
    """RO-006 — CH-R1 tomorrow_preview 2.5 resolves to CT-D1 (not Eta re-entry)."""
    from app.application.educational_packages.loader import EducationalPackageLoader

    eta_ids = {
        "CS1-EP001-PKG-2.4-MGF-CGF",
        "CS1-EP001-PKG-2.4-MOMENT-VIA-GF",
        "CS1-EP001-PKG-REV-GENERATING-FUNCTIONS",
    }
    pack = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="2.5",
        completed_package_ids=eta_ids,
        last_completed_package_id="CS1-EP001-PKG-REV-GENERATING-FUNCTIONS",
    )
    assert pack is not None
    assert pack.campaign_day == "CT-D1"
    assert pack.package_id == "CS1-EP001-PKG-2.5-CLT"

    approved = EducationalPackageLoader().all_approved()
    ct = [p for p in approved if (p.campaign_day or "").startswith("CT-")]
    assert len(ct) == 3
    assert len(approved) == 68




def test_iota_chain_reaches_ci_r1() -> None:
    """RO-007 — Continuity Front into 2.6 → CI-D1…CI-R1 joint inventory."""
    completed: set[str] = set()
    last = ""
    expected = [
        ("CS1-EP001-PKG-2.6-RANDOM-SAMPLES", "CI-D1"),
        ("CS1-EP001-PKG-2.6-SAMPLING-DISTRIBUTION-STATISTIC", "CI-D2"),
        ("CS1-EP001-PKG-2.6-MEAN-VAR-SAMPLE", "CI-D3"),
        ("CS1-EP001-PKG-2.6-NORMAL-SAMPLE-MEAN-VAR", "CI-D4"),
        ("CS1-EP001-PKG-2.6-T-STATISTIC", "CI-D5"),
        ("CS1-EP001-PKG-2.6-F-DISTRIBUTION", "CI-D6"),
        ("CS1-EP001-PKG-REV-SAMPLING-DISTRIBUTIONS", "CI-R1"),
    ]
    topic = "2.6"
    for package_id, day in expected:
        pack = resolve_active_educational_package(
            subject_id="CS1",
            syllabus_topic_code=topic,
            completed_package_ids=completed,
            last_completed_package_id=last,
        )
        assert pack is not None, f"missing successor before {day}"
        assert pack.package_id == package_id, (
            f"expected {package_id} got {pack.package_id}"
        )
        assert pack.campaign_day == day
        completed.add(pack.package_id)
        last = pack.package_id
        topic = pack.topic_code or topic


def test_theta_revision_hands_off_to_iota() -> None:
    """RO-007 — CT-R1 tomorrow_preview 2.6 resolves to CI-D1 (not Theta re-entry)."""
    from app.application.educational_packages.loader import EducationalPackageLoader

    theta_ids = {
        "CS1-EP001-PKG-2.5-CLT",
        "CS1-EP001-PKG-2.5-SIMULATED-SAMPLE-NORMAL",
        "CS1-EP001-PKG-REV-CENTRAL-LIMIT-THEOREM",
    }
    pack = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="2.6",
        completed_package_ids=theta_ids,
        last_completed_package_id="CS1-EP001-PKG-REV-CENTRAL-LIMIT-THEOREM",
    )
    assert pack is not None
    assert pack.campaign_day == "CI-D1"
    assert pack.package_id == "CS1-EP001-PKG-2.6-RANDOM-SAMPLES"

    approved = EducationalPackageLoader().all_approved()
    ci = [p for p in approved if (p.campaign_day or "").startswith("CI-")]
    assert len(ci) == 7
    assert len(approved) == 68


def test_kappa_chain_reaches_ck_r1() -> None:
    """RO-008 — Continuity Front into 3.1 → CK-D1…CK-R1 joint inventory."""
    completed: set[str] = set()
    last = ""
    expected = [
        ("CS1-EP001-PKG-3.1-METHOD-OF-MOMENTS", "CK-D1"),
        ("CS1-EP001-PKG-3.1-MAXIMUM-LIKELIHOOD", "CK-D2"),
        ("CS1-EP001-PKG-3.1-EFFICIENCY-BIAS-CONSISTENCY-MSE", "CK-D3"),
        ("CS1-EP001-PKG-3.1-COMPARISON-MSE", "CK-D4"),
        ("CS1-EP001-PKG-3.1-ASYMPTOTIC-MLE", "CK-D5"),
        ("CS1-EP001-PKG-3.1-BOOTSTRAP-ESTIMATOR", "CK-D6"),
        ("CS1-EP001-PKG-REV-ESTIMATORS", "CK-R1"),
    ]
    topic = "3.1"
    for package_id, day in expected:
        pack = resolve_active_educational_package(
            subject_id="CS1",
            syllabus_topic_code=topic,
            completed_package_ids=completed,
            last_completed_package_id=last,
        )
        assert pack is not None, f"missing successor before {day}"
        assert pack.package_id == package_id, (
            f"expected {package_id} got {pack.package_id}"
        )
        assert pack.campaign_day == day
        completed.add(pack.package_id)
        last = pack.package_id
        topic = pack.topic_code or topic


def test_iota_revision_hands_off_to_kappa() -> None:
    """RO-008 — CI-R1 tomorrow_preview 3.1 resolves to CK-D1 (not Iota re-entry)."""
    from app.application.educational_packages.loader import EducationalPackageLoader

    iota_ids = {
        "CS1-EP001-PKG-2.6-RANDOM-SAMPLES",
        "CS1-EP001-PKG-2.6-SAMPLING-DISTRIBUTION-STATISTIC",
        "CS1-EP001-PKG-2.6-MEAN-VAR-SAMPLE",
        "CS1-EP001-PKG-2.6-NORMAL-SAMPLE-MEAN-VAR",
        "CS1-EP001-PKG-2.6-T-STATISTIC",
        "CS1-EP001-PKG-2.6-F-DISTRIBUTION",
        "CS1-EP001-PKG-REV-SAMPLING-DISTRIBUTIONS",
    }
    pack = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="3.1",
        completed_package_ids=iota_ids,
        last_completed_package_id="CS1-EP001-PKG-REV-SAMPLING-DISTRIBUTIONS",
    )
    assert pack is not None
    assert pack.campaign_day == "CK-D1"
    assert pack.package_id == "CS1-EP001-PKG-3.1-METHOD-OF-MOMENTS"

    approved = EducationalPackageLoader().all_approved()
    ck = [p for p in approved if (p.campaign_day or "").startswith("CK-")]
    assert len(ck) == 7
    assert len(approved) == 68

