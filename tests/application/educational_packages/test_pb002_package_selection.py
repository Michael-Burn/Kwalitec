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
    assert len(approved) == 120


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
    assert len(approved) == 120


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
    assert len(approved) == 120


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
    assert len(approved) == 120




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
    assert len(approved) == 120


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
    assert len(approved) == 120


def test_lambda_chain_reaches_cl_r1() -> None:
    """RO-009 — Continuity Front into 3.2 → CL-D1…CL-R1 joint inventory."""
    completed: set[str] = set()
    last = ""
    expected = [
        ("CS1-EP001-PKG-3.2-CONFIDENCE-INTERVAL-PARAMETER", "CL-D1"),
        ("CS1-EP001-PKG-3.2-PREDICTION-INTERVAL", "CL-D2"),
        ("CS1-EP001-PKG-3.2-CI-GIVEN-SAMPLING-DISTRIBUTION", "CL-D3"),
        ("CS1-EP001-PKG-3.2-CI-NORMAL-MEAN-VARIANCE", "CL-D4"),
        ("CS1-EP001-PKG-3.2-CI-BINOMIAL-POISSON", "CL-D5"),
        ("CS1-EP001-PKG-3.2-CI-TWO-SAMPLE", "CL-D6"),
        ("CS1-EP001-PKG-3.2-CI-PAIRED-MEANS", "CL-D7"),
        ("CS1-EP001-PKG-3.2-BOOTSTRAP-CONFIDENCE-INTERVAL", "CL-D8"),
        ("CS1-EP001-PKG-REV-CONFIDENCE-INTERVALS", "CL-R1"),
    ]
    topic = "3.2"
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


def test_kappa_revision_hands_off_to_lambda() -> None:
    """RO-009 — CK-R1 tomorrow_preview 3.2 resolves to CL-D1 (not Kappa re-entry)."""
    from app.application.educational_packages.loader import EducationalPackageLoader

    kappa_ids = {
        "CS1-EP001-PKG-3.1-METHOD-OF-MOMENTS",
        "CS1-EP001-PKG-3.1-MAXIMUM-LIKELIHOOD",
        "CS1-EP001-PKG-3.1-EFFICIENCY-BIAS-CONSISTENCY-MSE",
        "CS1-EP001-PKG-3.1-COMPARISON-MSE",
        "CS1-EP001-PKG-3.1-ASYMPTOTIC-MLE",
        "CS1-EP001-PKG-3.1-BOOTSTRAP-ESTIMATOR",
        "CS1-EP001-PKG-REV-ESTIMATORS",
    }
    pack = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="3.2",
        completed_package_ids=kappa_ids,
        last_completed_package_id="CS1-EP001-PKG-REV-ESTIMATORS",
    )
    assert pack is not None
    assert pack.campaign_day == "CL-D1"
    assert pack.package_id == "CS1-EP001-PKG-3.2-CONFIDENCE-INTERVAL-PARAMETER"

    approved = EducationalPackageLoader().all_approved()
    cl = [p for p in approved if (p.campaign_day or "").startswith("CL-")]
    assert len(cl) == 9
    assert len(approved) == 120


def test_mu_chain_reaches_cm_r1() -> None:
    """RO-010 — Continuity Front into 3.3 → CM-D1…CM-R1 joint inventory."""
    completed: set[str] = set()
    last = ""
    expected = [
        ("CS1-EP001-PKG-3.3-HYPOTHESIS-CONCEPTS", "CM-D1"),
        ("CS1-EP001-PKG-3.3-BASIC-TESTS", "CM-D2"),
        ("CS1-EP001-PKG-3.3-PERMUTATION-TESTS", "CM-D3"),
        ("CS1-EP001-PKG-3.3-CHI-SQUARE-GOF", "CM-D4"),
        ("CS1-EP001-PKG-3.3-CONTINGENCY-INDEPENDENCE", "CM-D5"),
        ("CS1-EP001-PKG-REV-HYPOTHESIS-TESTING", "CM-R1"),
    ]
    topic = "3.3"
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


def test_lambda_revision_hands_off_to_mu() -> None:
    """RO-010 — CL-R1 tomorrow_preview 3.3 resolves to CM-D1 (not Lambda re-entry)."""
    from app.application.educational_packages.loader import EducationalPackageLoader

    lambda_ids = {
        "CS1-EP001-PKG-3.2-CONFIDENCE-INTERVAL-PARAMETER",
        "CS1-EP001-PKG-3.2-PREDICTION-INTERVAL",
        "CS1-EP001-PKG-3.2-CI-GIVEN-SAMPLING-DISTRIBUTION",
        "CS1-EP001-PKG-3.2-CI-NORMAL-MEAN-VARIANCE",
        "CS1-EP001-PKG-3.2-CI-BINOMIAL-POISSON",
        "CS1-EP001-PKG-3.2-CI-TWO-SAMPLE",
        "CS1-EP001-PKG-3.2-CI-PAIRED-MEANS",
        "CS1-EP001-PKG-3.2-BOOTSTRAP-CONFIDENCE-INTERVAL",
        "CS1-EP001-PKG-REV-CONFIDENCE-INTERVALS",
    }
    pack = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="3.3",
        completed_package_ids=lambda_ids,
        last_completed_package_id="CS1-EP001-PKG-REV-CONFIDENCE-INTERVALS",
    )
    assert pack is not None
    assert pack.campaign_day == "CM-D1"
    assert pack.package_id == "CS1-EP001-PKG-3.3-HYPOTHESIS-CONCEPTS"

    approved = EducationalPackageLoader().all_approved()
    cm = [p for p in approved if (p.campaign_day or "").startswith("CM-")]
    assert len(cm) == 6
    assert len(approved) == 120


def test_nu_chain_reaches_cn_r1() -> None:
    """RO-011 — Continuity Front join into 4.1 → CN-D1…CN-R1 joint inventory."""
    expected = [
        ("CS1-EP001-PKG-CN-4.1-RESPONSE-EXPLANATORY", "CN-D1"),
        ("CS1-EP001-PKG-CN-4.1-SIMPLE-MULTIPLE", "CN-D2"),
        ("CS1-EP001-PKG-CN-4.1-LEAST-SQUARES", "CN-D3"),
        ("CS1-EP001-PKG-CN-4.1-SOFTWARE-FIT", "CN-D4"),
        ("CS1-EP001-PKG-CN-4.1-VARIABLE-SELECTION", "CN-D5"),
        ("CS1-EP001-PKG-REV-LINEAR-REGRESSION-NU", "CN-R1"),
    ]
    topic = "4.1"
    # Seed journey as after CM-R1 so Nu+Delta coexistence prefers CN chain.
    last = "CS1-EP001-PKG-REV-HYPOTHESIS-TESTING"
    completed: set[str] = {last}
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


def test_mu_revision_hands_off_to_nu() -> None:
    """RO-011 — CM-R1 tomorrow_preview CN-D1 resolves to Nu (not Trust Front CD-D1)."""
    from app.application.educational_packages.loader import EducationalPackageLoader

    mu_ids = {
        "CS1-EP001-PKG-3.3-HYPOTHESIS-CONCEPTS",
        "CS1-EP001-PKG-3.3-BASIC-TESTS",
        "CS1-EP001-PKG-3.3-PERMUTATION-TESTS",
        "CS1-EP001-PKG-3.3-CHI-SQUARE-GOF",
        "CS1-EP001-PKG-3.3-CONTINGENCY-INDEPENDENCE",
        "CS1-EP001-PKG-REV-HYPOTHESIS-TESTING",
    }
    pack = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="4.1",
        completed_package_ids=mu_ids,
        last_completed_package_id="CS1-EP001-PKG-REV-HYPOTHESIS-TESTING",
    )
    assert pack is not None
    assert pack.campaign_day == "CN-D1"
    assert pack.package_id == "CS1-EP001-PKG-CN-4.1-RESPONSE-EXPLANATORY"

    # Trust Front cold entry at 4.1 remains Delta CD-D1.
    cold = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="4.1",
        completed_package_ids=frozenset(),
        last_completed_package_id="",
    )
    assert cold is not None
    assert cold.campaign_day == "CD-D1"
    assert cold.package_id == "CS1-EP001-PKG-4.1-RESPONSE-EXPLANATORY"

    approved = EducationalPackageLoader().all_approved()
    cn = [p for p in approved if (p.campaign_day or "").startswith("CN-")]
    assert len(cn) == 6
    assert len(approved) == 120



def test_xi_chain_reaches_cx_r1() -> None:
    """RO-012 — Continuity Front join into 4.2 → CX-D1…CX-R1 joint inventory."""
    expected = [
        ("CS1-EP001-PKG-CX-4.2-EXPONENTIAL-FAMILY", "CX-D1"),
        ("CS1-EP001-PKG-CX-4.2-MEAN-VARIANCE", "CX-D2"),
        ("CS1-EP001-PKG-CX-4.2-LINK-CANONICAL", "CX-D3"),
        ("CS1-EP001-PKG-CX-4.2-FACTORS-INTERACTIONS", "CX-D4"),
        ("CS1-EP001-PKG-CX-4.2-LINEAR-PREDICTOR", "CX-D5"),
        ("CS1-EP001-PKG-CX-4.2-DEVIANCE-ESTIMATION", "CX-D6"),
        ("CS1-EP001-PKG-CX-4.2-MODEL-CHOICE", "CX-D7"),
        ("CS1-EP001-PKG-CX-4.2-RESIDUALS", "CX-D8"),
        ("CS1-EP001-PKG-CX-4.2-GOODNESS-TESTS", "CX-D9"),
        ("CS1-EP001-PKG-CX-4.2-FIT-INTERPRET", "CX-D10"),
        ("CS1-EP001-PKG-REV-GLM-XI", "CX-R1"),
    ]
    topic = "4.2"
    # Seed journey as after CN-R1 so Xi+Delta coexistence prefers CX chain.
    last = "CS1-EP001-PKG-REV-LINEAR-REGRESSION-NU"
    completed: set[str] = {last}
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


def test_nu_revision_hands_off_to_xi() -> None:
    """RO-012 — CN-R1 tomorrow_preview CX-D1 resolves to Xi (not Trust Front CD-D6)."""
    from app.application.educational_packages.loader import EducationalPackageLoader

    nu_ids = {
        "CS1-EP001-PKG-CN-4.1-RESPONSE-EXPLANATORY",
        "CS1-EP001-PKG-CN-4.1-SIMPLE-MULTIPLE",
        "CS1-EP001-PKG-CN-4.1-LEAST-SQUARES",
        "CS1-EP001-PKG-CN-4.1-SOFTWARE-FIT",
        "CS1-EP001-PKG-CN-4.1-VARIABLE-SELECTION",
        "CS1-EP001-PKG-REV-LINEAR-REGRESSION-NU",
    }
    pack = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="4.2",
        completed_package_ids=nu_ids,
        last_completed_package_id="CS1-EP001-PKG-REV-LINEAR-REGRESSION-NU",
    )
    assert pack is not None
    assert pack.campaign_day == "CX-D1"
    assert pack.package_id == "CS1-EP001-PKG-CX-4.2-EXPONENTIAL-FAMILY"

    # Trust Front cold entry at 4.2 remains Delta CD-D6.
    cold = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="4.2",
        completed_package_ids=frozenset(),
        last_completed_package_id="",
    )
    assert cold is not None
    assert cold.campaign_day == "CD-D6"
    assert cold.package_id == "CS1-EP001-PKG-4.2-EXPONENTIAL-FAMILY"

    # Trust Front cold entry at 4.1 remains Delta CD-D1.
    cold41 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="4.1",
        completed_package_ids=frozenset(),
        last_completed_package_id="",
    )
    assert cold41 is not None
    assert cold41.campaign_day == "CD-D1"

    approved = EducationalPackageLoader().all_approved()
    cx = [p for p in approved if (p.campaign_day or "").startswith("CX-")]
    assert len(cx) == 11
    assert len(approved) == 120


def test_omicron_chain_reaches_co_r1() -> None:
    """RO-013 — Continuity Front join into 5.1 → CO-D1…CO-R1 joint inventory."""
    expected = [
        ("CS1-EP001-PKG-CO-5.1-BAYES-THEOREM", "CO-D1"),
        ("CS1-EP001-PKG-CO-5.1-PRIOR-POSTERIOR", "CO-D2"),
        ("CS1-EP001-PKG-CO-5.1-POSTERIOR-SIMPLE", "CO-D3"),
        ("CS1-EP001-PKG-CO-5.1-LOSS-ESTIMATORS", "CO-D4"),
        ("CS1-EP001-PKG-CO-5.1-CREDIBLE-INTERVALS", "CO-D5"),
        ("CS1-EP001-PKG-CO-5.1-CREDIBILITY-PREMIUM", "CO-D6"),
        ("CS1-EP001-PKG-CO-5.1-BAYESIAN-CREDIBILITY", "CO-D7"),
        ("CS1-EP001-PKG-CO-5.1-EMPIRICAL-BAYES", "CO-D8"),
        ("CS1-EP001-PKG-CO-5.1-BAYES-VS-EB", "CO-D9"),
        ("CS1-EP001-PKG-REV-BAYESIAN-OMICRON", "CO-R1"),
    ]
    topic = "5.1"
    # Seed journey as after CX-R1 so Omicron+Delta coexistence prefers CO chain.
    last = "CS1-EP001-PKG-REV-GLM-XI"
    completed: set[str] = {last}
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


def test_xi_revision_hands_off_to_omicron() -> None:
    """RO-013 — CX-R1 tomorrow_preview CO-D1 resolves to Omicron (not Trust Front CD-D16)."""
    from app.application.educational_packages.loader import EducationalPackageLoader

    xi_ids = {
        "CS1-EP001-PKG-CX-4.2-EXPONENTIAL-FAMILY",
        "CS1-EP001-PKG-CX-4.2-MEAN-VARIANCE",
        "CS1-EP001-PKG-CX-4.2-LINK-CANONICAL",
        "CS1-EP001-PKG-CX-4.2-FACTORS-INTERACTIONS",
        "CS1-EP001-PKG-CX-4.2-LINEAR-PREDICTOR",
        "CS1-EP001-PKG-CX-4.2-DEVIANCE-ESTIMATION",
        "CS1-EP001-PKG-CX-4.2-MODEL-CHOICE",
        "CS1-EP001-PKG-CX-4.2-RESIDUALS",
        "CS1-EP001-PKG-CX-4.2-GOODNESS-TESTS",
        "CS1-EP001-PKG-CX-4.2-FIT-INTERPRET",
        "CS1-EP001-PKG-REV-GLM-XI",
    }
    pack = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="5.1",
        completed_package_ids=xi_ids,
        last_completed_package_id="CS1-EP001-PKG-REV-GLM-XI",
    )
    assert pack is not None
    assert pack.campaign_day == "CO-D1"
    assert pack.package_id == "CS1-EP001-PKG-CO-5.1-BAYES-THEOREM"

    # Trust Front cold entry at 5.1 remains Delta CD-D16.
    cold = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="5.1",
        completed_package_ids=frozenset(),
        last_completed_package_id="",
    )
    assert cold is not None
    assert cold.campaign_day == "CD-D16"
    assert cold.package_id == "CS1-EP001-PKG-5.1-BAYES-THEOREM"

    # Trust Front cold entry at 4.2 remains Delta CD-D6.
    cold42 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="4.2",
        completed_package_ids=frozenset(),
        last_completed_package_id="",
    )
    assert cold42 is not None
    assert cold42.campaign_day == "CD-D6"
    assert cold42.package_id == "CS1-EP001-PKG-4.2-EXPONENTIAL-FAMILY"

    approved = EducationalPackageLoader().all_approved()
    co = [p for p in approved if (p.campaign_day or "").startswith("CO-")]
    assert len(co) == 10
    assert len(approved) == 120


def test_pi_chain_reaches_cp_r1() -> None:
    """RO-014 — Memory Front spine re-audit → CP-D1…CP-R1 joint inventory."""
    expected = [
        ("CS1-EP001-PKG-CP-2.1-PROB-QUANTILES", "CP-D1"),
        ("CS1-EP001-PKG-CP-2.2-MARGINAL-CONDITIONAL", "CP-D2"),
        ("CS1-EP001-PKG-CP-2.5-CLT", "CP-D3"),
        ("CS1-EP001-PKG-CP-2.6-RANDOM-SAMPLES", "CP-D4"),
        ("CS1-EP001-PKG-CP-3.1-ESTIMATORS", "CP-D5"),
        ("CS1-EP001-PKG-CP-3.2-CI-SAMPLE", "CP-D6"),
        ("CS1-EP001-PKG-CP-3.3-HYPOTHESIS-TESTING", "CP-D7"),
        ("CS1-EP001-PKG-CP-4.1-LINEAR-REGRESSION", "CP-D8"),
        ("CS1-EP001-PKG-CP-5.1-BAYES-THEOREM", "CP-D9"),
        ("CS1-EP001-PKG-REV-SPINE-MEMORY-PI", "CP-R1"),
    ]
    topic = "2.1"
    # Seed journey as after CO-R1 so Pi+Opening/Trust coexistence prefers CP.
    last = "CS1-EP001-PKG-REV-BAYESIAN-OMICRON"
    completed: set[str] = {last}
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


def test_omicron_revision_hands_off_to_pi() -> None:
    """RO-014 — CO-R1 tomorrow_preview CP-D1 resolves to Pi (not Opening Front)."""
    from app.application.educational_packages.loader import EducationalPackageLoader

    omicron_ids = {
        "CS1-EP001-PKG-CO-5.1-BAYES-THEOREM",
        "CS1-EP001-PKG-CO-5.1-PRIOR-POSTERIOR",
        "CS1-EP001-PKG-CO-5.1-POSTERIOR-SIMPLE",
        "CS1-EP001-PKG-CO-5.1-LOSS-ESTIMATORS",
        "CS1-EP001-PKG-CO-5.1-CREDIBLE-INTERVALS",
        "CS1-EP001-PKG-CO-5.1-CREDIBILITY-PREMIUM",
        "CS1-EP001-PKG-CO-5.1-BAYESIAN-CREDIBILITY",
        "CS1-EP001-PKG-CO-5.1-EMPIRICAL-BAYES",
        "CS1-EP001-PKG-CO-5.1-BAYES-VS-EB",
        "CS1-EP001-PKG-REV-BAYESIAN-OMICRON",
    }
    pack = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="2.1",
        completed_package_ids=omicron_ids,
        last_completed_package_id="CS1-EP001-PKG-REV-BAYESIAN-OMICRON",
    )
    assert pack is not None
    assert pack.campaign_day == "CP-D1"
    assert pack.package_id == "CS1-EP001-PKG-CP-2.1-PROB-QUANTILES"

    # Opening Front cold entry at 2.1 remains early inventory (not Pi Memory Front).
    cold = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="2.1",
        completed_package_ids=frozenset(),
        last_completed_package_id="",
    )
    assert cold is not None
    assert not (cold.campaign_day or "").startswith("CP-")
    assert cold.package_id != "CS1-EP001-PKG-CP-2.1-PROB-QUANTILES"

    # Trust Front cold entry at 5.1 remains Delta CD-D16.
    cold51 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="5.1",
        completed_package_ids=frozenset(),
        last_completed_package_id="",
    )
    assert cold51 is not None
    assert cold51.campaign_day == "CD-D16"

    # Trust Front cold entry at 4.2 remains Delta CD-D6.
    cold42 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="4.2",
        completed_package_ids=frozenset(),
        last_completed_package_id="",
    )
    assert cold42 is not None
    assert cold42.campaign_day == "CD-D6"

    approved = EducationalPackageLoader().all_approved()
    cp = [p for p in approved if (p.campaign_day or "").startswith("CP-")]
    assert len(cp) == 10
    assert len(approved) == 120
